"""
Seed the SND database with demo data.

Run with: python migrations/seed.py  (from the project root inside the api container)
Reads connection config from environment variables (same as the API).

Creates:
  - 3 users  (admin / editor / guest)
  - 4 military units
  - 12 persons of varying types and statuses
"""
import asyncio
import datetime
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "api"))

from motor import motor_asyncio
from odmantic import AIOEngine
from passlib.context import CryptContext

# ── connection ────────────────────────────────────────────────────────────────
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = int(os.getenv("DATABASE_PORT", 27017))
DATABASE_NAME = os.getenv("DATABASE_NAME", "snd")
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME", "")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "")

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], default="pbkdf2_sha256", pbkdf2_sha256__default_rounds=30000)


def get_engine():
    if DATABASE_USERNAME:
        uri = f"mongodb://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
        client = motor_asyncio.AsyncIOMotorClient(uri)
    else:
        client = motor_asyncio.AsyncIOMotorClient(DATABASE_HOST, DATABASE_PORT)
    client.get_io_loop = asyncio.get_running_loop
    return client, AIOEngine(motor_client=client, database=DATABASE_NAME)


# ── helpers ───────────────────────────────────────────────────────────────────
def d(year, month, day):
    return datetime.date(year, month, day)


def dt(year, month, day):
    return datetime.datetime(year, month, day)


def hash_pw(raw):
    return pwd_context.encrypt(raw)


def score(person):
    """Re-implement the scoring logic from services/person.py without importing the whole app."""
    from constants.person import PersonStatus
    s = 0
    if person.status == PersonStatus.SND:
        s += 1000
    if person.photo:
        s += 50
    if person.birthday:
        s += 5
    if person.phones:
        s += 5 * len(person.phones)
    if person.addresses:
        s += 5 * len(person.addresses)
    if person.passport:
        s += 3
    if person.relatives:
        s += len(person.relatives)
        for rel in person.relatives:
            if rel.photo:
                s += 5
            if rel.phones:
                s += 3 * len(rel.phones)
            if rel.address:
                s += 3
    return s


def make_code(last, first, middle, birthday):
    from transliterate import translit
    dob = birthday.strftime("%d%m%Y") if birthday else None
    raw = "_".join(filter(None, (last, first, middle, dob))).lower()
    return translit(raw, "ru", reversed=True)


# ── seed data ─────────────────────────────────────────────────────────────────
async def seed_users(engine):
    from models.user import User, Roles

    users = [
        User(
            email="admin@snd.local",
            name="Admin User",
            password=hash_pw("Admin1234!"),
            role=Roles.ADMIN,
            verified=True,
        ),
        User(
            email="editor@snd.local",
            name="Editor User",
            password=hash_pw("Editor1234!"),
            role=Roles.EDITOR,
            verified=True,
        ),
        User(
            email="guest@snd.local",
            name="Guest User",
            password=hash_pw("Guest1234!"),
            role=Roles.GUEST,
            verified=True,
        ),
    ]

    created = 0
    for u in users:
        existing = await engine.find_one(User, User.email == u.email)
        if existing:
            print(f"  [SKIP] user {u.email}")
            continue
        await engine.save(u)
        print(f"  [OK]   user {u.email}  (role={u.role.name})")
        created += 1
    return created


async def seed_units(engine):
    from models.military_unit import MilitaryUnit

    units_data = [
        dict(name="64-я отдельная мотострелковая бригада",   number="64",  address="Хабаровский край, Хабаровск", phones=[74212345678], disbanded=False),
        dict(name="200-я отдельная общевойсковая армия",      number="200", address="Мурманская обл., Печенга",    phones=[78152345678], disbanded=False),
        dict(name="58-я общевойсковая армия",                 number="58",  address="Северная Осетия, Владикавказ",phones=[78672345678], disbanded=False),
        dict(name="Черноморский флот",                        number="ЧФ",  address="Севастополь",                 phones=[78692345678], disbanded=False),
    ]

    unit_ids = {}
    for data in units_data:
        existing = await engine.find_one(MilitaryUnit, MilitaryUnit.number == data["number"])
        if existing:
            print(f"  [SKIP] unit №{data['number']}")
            unit_ids[data["number"]] = existing.id
            continue
        unit = MilitaryUnit(**data)
        await engine.save(unit)
        unit_ids[data["number"]] = unit.id
        print(f"  [OK]   unit №{data['number']} — {data['name']}")
    return unit_ids


async def seed_persons(engine, unit_ids):
    from models.person import Person, Military, Social, Doc, Relative
    from constants.person import PersonType, PersonStatus, Relationship
    from constants.countries import CountryCodes

    u64  = unit_ids.get("64")
    u200 = unit_ids.get("200")
    u58  = unit_ids.get("58")
    uchf = unit_ids.get("ЧФ")

    persons_data = [
        # ── High-value targets (SND status) ──────────────────────────────────
        Person(
            code=make_code("Иванов", "Сергей", "Николаевич", d(1975, 3, 12)),
            first_name="Сергей", last_name="Иванов", middle_name="Николаевич",
            type=PersonType.MILITARY, country=CountryCodes.RU,
            birthday=d(1975, 3, 12), city_of_birth="Москва",
            addresses=["г. Москва, ул. Ленина 12, кв. 45", "г. Ростов-на-Дону, пр. Мира 7"],
            phones=[79161234567, 79031234567],
            military=Military(rank="GF15", post="Командир бригады", unit=u64, number="A123456"),
            social=Social(vk="https://vk.com/ivanov_s", ok="https://ok.ru/ivanovs75"),
            passport=Doc(number="4512 678901", date=d(2015, 6, 20), authority="ОВД Центрального р-на г. Москвы"),
            status=PersonStatus.SND,
            tags=["командир", "64 бригада", "военные преступления"],
            sources=["https://myrotvorets.center/criminal/ivanov-sergei/", "https://t.me/some_channel/123"],
        ),
        Person(
            code=make_code("Петров", "Александр", "Викторович", d(1980, 7, 25)),
            first_name="Александр", last_name="Петров", middle_name="Викторович",
            type=PersonType.MILITARY, country=CountryCodes.RU,
            birthday=d(1980, 7, 25), city_of_birth="Санкт-Петербург",
            addresses=["г. Санкт-Петербург, Невский пр. 34, кв. 12"],
            phones=[79211234567],
            military=Military(rank="GF14", post="Заместитель командира", unit=u64),
            social=Social(vk="https://vk.com/petrov_av"),
            status=PersonStatus.SND,
            tags=["64 бригада", "Буча"],
            sources=["https://myrotvorets.center/criminal/petrov-alexander/"],
        ),
        # ── Dead ─────────────────────────────────────────────────────────────
        Person(
            code=make_code("Сидоров", "Дмитрий", "Олегович", d(1990, 11, 5)),
            first_name="Дмитрий", last_name="Сидоров", middle_name="Олегович",
            type=PersonType.MILITARY, country=CountryCodes.RU,
            birthday=d(1990, 11, 5), city_of_birth="Екатеринбург",
            addresses=["г. Екатеринбург, ул. Победы 3, кв. 8"],
            phones=[79343456789],
            military=Military(rank="GF12", post="Командир роты", unit=u200),
            status=PersonStatus.DEAD,
            tags=["200 армия"],
            sources=["https://t.me/losses_ru/5432"],
        ),
        Person(
            code=make_code("Кузнецов", "Игорь", "Михайлович", d(1985, 4, 18)),
            first_name="Игорь", last_name="Кузнецов", middle_name="Михайлович",
            type=PersonType.MILITARY, country=CountryCodes.RU,
            birthday=d(1985, 4, 18),
            phones=[79521234567],
            military=Military(rank="GF11", post="Старший лейтенант", unit=u200),
            status=PersonStatus.DEAD,
            tags=["200 армия"],
            sources=[],
        ),
        # ── Prisoner of War ───────────────────────────────────────────────────
        Person(
            code=make_code("Морозов", "Алексей", "Павлович", d(1993, 8, 30)),
            first_name="Алексей", last_name="Морозов", middle_name="Павлович",
            type=PersonType.MILITARY, country=CountryCodes.RU,
            birthday=d(1993, 8, 30), city_of_birth="Новосибирск",
            addresses=["г. Новосибирск, ул. Советская 56, кв. 22"],
            phones=[79134567890],
            military=Military(rank="GF4", post="Сержант", unit=u58),
            status=PersonStatus.POW,
            tags=["58 армия", "пленный"],
            sources=["https://t.me/pows_ru/234"],
        ),
        Person(
            code=make_code("Волков", "Николай", "Андреевич", d(1998, 1, 14)),
            first_name="Николай", last_name="Волков", middle_name="Андреевич",
            type=PersonType.MILITARY, country=CountryCodes.RU,
            birthday=d(1998, 1, 14),
            military=Military(rank="GF1", post="Рядовой", unit=u58),
            status=PersonStatus.POW,
            tags=["58 армия", "пленный"],
            sources=[],
        ),
        # ── Alive ─────────────────────────────────────────────────────────────
        Person(
            code=make_code("Громов", "Виктор", "Сергеевич", d(1978, 6, 9)),
            first_name="Виктор", last_name="Громов", middle_name="Сергеевич",
            type=PersonType.MILITARY, country=CountryCodes.RU,
            birthday=d(1978, 6, 9), city_of_birth="Краснодар",
            addresses=["г. Краснодар, ул. Красная 78"],
            phones=[79614321098],
            military=Military(rank="N15", post="Капитан 1 ранга", unit=uchf),
            social=Social(vk="https://vk.com/gromov.v"),
            status=PersonStatus.ALIVE,
            tags=["Черноморский флот", "ЧФ"],
            sources=["https://myrotvorets.center/criminal/gromov-viktor/"],
        ),
        Person(
            code=make_code("Белов", "Олег", "Игоревич", d(1982, 9, 23)),
            first_name="Олег", last_name="Белов", middle_name="Игоревич",
            type=PersonType.MILITARY, country=CountryCodes.RU,
            birthday=d(1982, 9, 23),
            phones=[79771234567, 79162345678],
            military=Military(rank="GF13", post="Майор", unit=u58),
            status=PersonStatus.ALIVE,
            tags=["58 армия"],
            sources=[],
        ),
        # ── HUYLO (political) ─────────────────────────────────────────────────
        Person(
            code=make_code("Захаров", "Руслан", "Феликсович", d(1965, 12, 1)),
            first_name="Руслан", last_name="Захаров", middle_name="Феликсович",
            type=PersonType.HUYLO, country=CountryCodes.RU,
            birthday=d(1965, 12, 1), city_of_birth="Москва",
            addresses=["г. Москва, Рублёво-Успенское ш. 101", "Монако, Монте-Карло, ул. Принцессы 3"],
            phones=[74991234567],
            passport=Doc(number="7700 123456", date=d(2010, 3, 5), authority="УФМС г. Москвы"),
            social=Social(vk="https://vk.com/zakharov_rf", fb="https://facebook.com/zakharov"),
            status=PersonStatus.ALIVE,
            tags=["пропаганда", "депутат", "Государственная Дума"],
            sources=["https://myrotvorets.center/criminal/zakharov-ruslan/"],
            relatives=[
                Relative(
                    name="Захарова Елена Викторовна",
                    relationship=Relationship.WIFE,
                    birthday=d(1970, 5, 15),
                    phones=[74991234568],
                    address="г. Монако, Монте-Карло, ул. Принцессы 3",
                ),
            ],
        ),
        Person(
            code=make_code("Орлов", "Геннадий", "Борисович", d(1958, 2, 28)),
            first_name="Геннадий", last_name="Орлов", middle_name="Борисович",
            type=PersonType.HUYLO, country=CountryCodes.RU,
            birthday=d(1958, 2, 28), city_of_birth="Ленинград",
            addresses=["г. Санкт-Петербург, Каменноостровский пр. 5"],
            phones=[78121234567],
            status=PersonStatus.ALIVE,
            tags=["губернатор", "пропаганда"],
            sources=[],
        ),
        # ── Betrayers ─────────────────────────────────────────────────────────
        Person(
            code=make_code("Коваленко", "Андрій", "Олексійович", d(1987, 5, 17)),
            first_name="Андрій", last_name="Коваленко", middle_name="Олексійович",
            type=PersonType.BETRAYER, country=CountryCodes.UA,
            birthday=d(1987, 5, 17), city_of_birth="Донецьк",
            addresses=["м. Донецьк, вул. Артема 12, кв. 5"],
            phones=[79491234567],
            social=Social(vk="https://vk.com/kovalenko.a"),
            status=PersonStatus.ALIVE,
            tags=["колаборант", "Донецька область"],
            sources=["https://t.me/collaborants/789"],
        ),
        Person(
            code=make_code("Ткаченко", "Василь", "Петрович", d(1979, 10, 3)),
            first_name="Василь", last_name="Ткаченко", middle_name="Петрович",
            type=PersonType.BETRAYER, country=CountryCodes.UA,
            birthday=d(1979, 10, 3),
            addresses=["м. Луганськ, вул. Радянська 45"],
            phones=[79591234567],
            status=PersonStatus.PRISONED,
            tags=["колаборант", "Луганська область"],
            sources=[],
        ),
    ]

    created = 0
    for p in persons_data:
        existing = await engine.find_one(Person, Person.code == p.code)
        if existing:
            print(f"  [SKIP] person {p.code}")
            continue
        p.score = score(p)
        await engine.save(p)
        print(f"  [OK]   person {p.code}  (type={p.type.name}, status={p.status.name}, score={p.score})")
        created += 1
    return created


async def run():
    client, engine = get_engine()
    print(f"Connecting to MongoDB at {DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}\n")

    print("── Users ─────────────────────────────────────────────────────────")
    u_count = await seed_users(engine)

    print("\n── Military Units ────────────────────────────────────────────────")
    unit_ids = await seed_units(engine)

    print("\n── Persons ───────────────────────────────────────────────────────")
    p_count = await seed_persons(engine, unit_ids)

    print(f"\nDone. Created {u_count} user(s), {len(unit_ids)} unit(s), {p_count} person(s).")
    client.close()


if __name__ == "__main__":
    asyncio.run(run())
