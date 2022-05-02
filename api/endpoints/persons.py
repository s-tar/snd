from uuid import uuid4

from bson import ObjectId
from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import UploadFile
from starlette import status

from base.database import database
from base.settings import Settings
from base.settings import get_settings
from lib.dict import merge
from lib.exceptions import FieldValidationError
from lib.files import FILL
from lib.files import remove_by_name
from lib.files import save_image
from lib.pagination import paginate
from models.person import Person
from models.military_unit import MilitaryUnit
from models.user import User
from schemas.person import AddManyPersonRequest
from schemas.person import AddPersonRequest
from schemas.person import PersonIdResponse
from schemas.person import AddMultipleResponse
from schemas.person import PersonListResponse
from schemas.person import PersonPublicData
from schemas.person import PersonResponse
from schemas.person import UpdatePersonRequest
from schemas.response import Status
from services.person import create_person_code
from services.user import get_editor

router = APIRouter()


def get_code(person):
    return create_person_code(
        first_name=person.first_name,
        middle_name=person.middle_name,
        last_name=person.last_name,
        birthday=person.birthday,
    )


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

    person.code = get_code(person)
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


@router.post(
    "/add_many",
    status_code=status.HTTP_200_OK,
    response_model=AddMultipleResponse,
    responses={
        status.HTTP_403_FORBIDDEN: {"description": "Operation forbidden"},
    },
    summary="Add multiple persons to blacklist"
)
async def add_many_person_endpoint(
    data: AddManyPersonRequest,
    editor: User = Depends(get_editor),
):
    unit_ids = {
        person.military.unit
        for person in data.persons
        if person.military and person.military.unit
    }
    units = {
        unit.number: unit
        for unit in await database.find(
            MilitaryUnit,
            MilitaryUnit.number.in_(list(unit_ids))
        )
    }

    persons = []
    person_codes = []
    for person_data in data.persons:
        if person_data.military and person_data.military.unit not in units:
            raise FieldValidationError(
                "military.unit", "Military unit not found"
            )

        person = Person(
            **person_data.dict(exclude_unset=True),
            code=get_code(person_data)
        )
        persons.append(person)
        person_codes.append(person.code)

    existed_codes = {
        person.code
        for person in await database.find(Person, Person.code.in_(person_codes))
    }

    fails = {
        i: (
            f"{person.last_name} {person.first_name} {person.middle_name} "
            "already exists"
        )
        for i, person in enumerate(persons)
        if person.code in existed_codes
    }
    await database.save_all(
        person for person in persons if person.code not in existed_codes
    )
    return AddMultipleResponse(fails=fails)


@router.post(
    "/add",
    status_code=status.HTTP_200_OK,
    response_model=PersonIdResponse,
    responses={
        status.HTTP_403_FORBIDDEN: {"description": "Operation forbidden"},
    },
    summary="Add person to blacklist"
)
async def add_person_endpoint(
    data: AddPersonRequest,
    photo: UploadFile = File(None),
    editor: User = Depends(get_editor),
):
    person = await save_person(data, photo=photo)
    return PersonIdResponse(id=str(person.id), code=person.code)


@router.post(
    "/update",
    status_code=status.HTTP_200_OK,
    response_model=PersonIdResponse,
    responses={
        status.HTTP_403_FORBIDDEN: {"description": "Operation forbidden"},
    },
    summary="Update person to blacklist"
)
async def update_person_endpoint(
    data: UpdatePersonRequest,
    photo: UploadFile = File(None),
    editor: User = Depends(get_editor),
):
    person = await save_person(data, person_id=data.id, photo=photo)
    return PersonIdResponse(id=str(person.id), code=person.code)


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    response_model=PersonListResponse,
    summary="List all persons"
)
async def all_persons_endpoint(
    page: int = 1,
    per_page: int = 20,
    s: str = None,
):
    query = {}
    if s:
        search = '"'+'" "'.join(s.split())+'"'
        query = {"$text": {"$search": search}}

    persons_page = await paginate(
        entity=Person,
        query=query,
        page=page,
        per_page=per_page,
        sort=Person.id.desc(),
    )

    return PersonListResponse(
        status=Status.OK,
        page=persons_page.page,
        per_page=persons_page.per_page,
        max_page=persons_page.max_page,
        items=[
            PersonPublicData(**item.dict())
            for item in persons_page.items
        ],
    )


@router.get(
    "/{person_code}",
    status_code=status.HTTP_200_OK,
    response_model=PersonResponse,
    summary="Get person by code"
)
async def all_persons_endpoint(person_code: str):
    person = await database.find_one(Person, {"code": person_code})
    if not person:
        raise FieldValidationError("code", "Person not found")

    return PersonResponse(
        status=Status.OK,
        person=PersonPublicData(**person.dict()),
    )
