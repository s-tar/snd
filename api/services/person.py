from bson import ObjectId
from transliterate import translit

from base.database import database
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
