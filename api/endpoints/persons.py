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
from schemas.response import ResponseModel
from schemas.response import Status
from services.person import get_person_code
from services.person import save_person
from services.person import save_person
from services.person import get_score
from services.user import get_admin
from services.user import get_editor

router = APIRouter()


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
        unit.id: unit
        for unit in await database.find(
            MilitaryUnit,
            MilitaryUnit.id.in_(list(unit_ids))
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
            code=get_person_code(person_data)
        )
        person.score = get_score(person)
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
        sort=(Person.score.desc(), Person.id.desc())
    )

    return PersonListResponse(
        status=Status.OK,
        page=persons_page.page,
        per_page=persons_page.per_page,
        max_page=persons_page.max_page,
        total=persons_page.total,
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
async def get_person_by_code_endpoint(person_code: str):
    person = await database.find_one(Person, {"code": person_code})
    if not person:
        raise FieldValidationError("code", "Person not found")

    return PersonResponse(
        status=Status.OK,
        person=PersonPublicData(**person.dict()),
    )


@router.post(
    "/rescore",
    status_code=status.HTTP_200_OK,
    response_model=ResponseModel,
    responses={
        status.HTTP_403_FORBIDDEN: {"description": "Operation forbidden"},
    },
    summary="Recalculate person scores"
)
async def rescore_persons_endpoint(
    admin: User = Depends(get_admin),
):
    last_id = None
    while True:
        query = {}
        if last_id:
            query = Person.id > last_id

        persons = await database.find(Person, query, limit=50)
        if not persons:
            break

        for person in persons:
            person.score = get_score(person)

        await database.save_all(persons)
        last_id = persons[-1].id

    return ResponseModel(
        status=Status.OK
    )
