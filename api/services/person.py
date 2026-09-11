from bson import ObjectId
from transliterate import translit

from base.database import database
from constants.person import PersonStatus
from lib.exceptions import FieldValidationError
from models.person import Person


def create_person_code(first_name, middle_name, last_name, birthday):
    dob = None
    if birthday:
        dob = birthday.strftime("%d%m%Y")
    code = "_".join(
        filter(None, (last_name, first_name, middle_name, dob))
    ).lower()
    return translit(code, "ru", reversed=True)


async def get_person_or_fail(
    id_: str,
) -> Person:
    if not ObjectId.is_valid(id_):
        raise FieldValidationError("_id", f"Invalid id")

    person = await database.find_one(Person, Person.id == ObjectId(id_))
    if not person:
        raise FieldValidationError("_id", f"Person not found")

    return person


def get_score(person):
    score = 0
    if person.status == PersonStatus.SND:
        score += 1000

    if person.photo:
        score += 50

    if person.birthday:
        score += 5

    if person.phones:
        score += 5 * len(person.phones)

    if person.addresses:
        score += 5 * len(person.addresses)

    if person.passport:
        score += 3

    if person.relatives:
        score += len(person.relatives)
        for rel in person.relatives:
            if rel.photo:
                score += 5

            if rel.phones:
                score += 3 * len(rel.phones)

            if rel.address:
                score += 3

    return score


async def save_person(data, person_id=None, photo=None):
    setting = get_settings()
    update_data = data.dict(exclude_unset=True)
    if "photo" in update_data:
        del update_data["photo"]

    if person_id:
        person = await database.find_one(Person, Person.id == person_id)
        if not person:
            raise FieldValidationError("id", "Person not found")
        person = Person(**merge(person.dict(exclude_none=True), update_data))
    else:
        person = Person(**merge({}, update_data), code='')

    person.code = get_person_code(person)
    person.score = get_score(person)
    check_code_person = (
        await database.find_one(Person, Person.code == person.code)
    )

    if check_code_person and check_code_person.id != person.id:
        return None, ("first_name", f"Person already exist")

    await database.save(person)

    if photo and data.photo:
        upload_folder = f"{setting.file_upload_folder}/person/{str(person.id)}"
        previous_photo = None
        if person.photo:
            name, hex, _ = person.photo.rsplit(".", 2)
            previous_photo = f"{name}.{hex}"

        hex = uuid4().hex
        await save_image(
            file=photo,
            name=f"photo.{hex}",
            upload_folder=upload_folder,
            size=(1024, 1024),
            fill=FILL.CONTAINS,
        )
        thumbnail_name = await save_image(
            file=photo,
            name=f"photo.{hex}.100x100",
            upload_folder=upload_folder,
            size=(100, 100),
            crop=(
                data.photo.left,
                data.photo.top,
                data.photo.left + data.photo.width,
                data.photo.top + data.photo.height,
            ),
            fill=FILL.COVER,
        )
        if thumbnail_name:
            person.photo = thumbnail_name
            await database.save(person)
            if previous_photo:
                remove_by_name(upload_folder, "photo", exclude=f"photo.{hex}")

    return person


def get_person_code(person):
    return create_person_code(
        first_name=person.first_name,
        middle_name=person.middle_name,
        last_name=person.last_name,
        birthday=person.birthday,
    )
