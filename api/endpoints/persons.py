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
from models.squad import Squad
from models.user import User
from schemas.person import AddManyPersonRequest
from schemas.person import PersonIdResponse
from schemas.person import AddMultipleResponse
from schemas.person import PersonListResponse
from schemas.person import PersonResponse
from schemas.person import SavePersonRequest
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
    squad_ids = {
        ObjectId(person.military.squad)
        for person in data.persons
        if person.military and person.military.squad
    }
    squads = {
        squad.id: squad
        for squad in await database.find(Squad, Squad.id.in_(list(squad_ids)))
    }

    persons = []
    person_codes = []
    for person_data in data.persons:
        if person_data.military and person_data.military.squad not in squads:
            raise FieldValidationError("military.squad", "Squad not found")

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
    "/save",
    status_code=status.HTTP_200_OK,
    response_model=PersonIdResponse,
    responses={
        status.HTTP_403_FORBIDDEN: {"description": "Operation forbidden"},
    },
    summary="Save person to blacklist"
)
async def save_person_endpoint(
    data: SavePersonRequest,
    setting: Settings = Depends(get_settings),
    photo: UploadFile = File(None),
    editor: User = Depends(get_editor),
):
    if data.id:
        person = await database.find_one(Person, Person.id == data.id)
        if not person:
            raise FieldValidationError("id", "Person not found")

        person = Person(**merge(
            person.dict(exclude_none=True),
            data.dict(exclude_unset=True)
        ))
    else:
        person = Person(**data.dict(exclude_unset=True), code='')

    person.code = get_code(person)
    check_code_person = await database.find_one(Person, Person.code == person.code)
    if check_code_person and check_code_person.id != person.id:
        return None, ("first_name", f"Person already exist")

    await database.save(person)

    if photo:
        upload_folder = f"{setting.file_upload_folder}/person/{str(person.id)}"
        previous_photo = None
        if person.photo:
            name, hex, _ = person.photo.rsplit(".", 2)
            previous_photo = f"{name}.{hex}"

        hex = uuid4().hex
        await save_image(
            file=photo,
            name="photo",
            hex=hex,
            upload_folder=upload_folder,
        )
        thumbnail_name = await save_image(
            file=photo,
            name="photo",
            hex=hex,
            upload_folder=upload_folder,
            size=(100, 100),
            fill=FILL.COVER,
        )
        if thumbnail_name:
            person.photo = thumbnail_name
            await database.save(person)
            if previous_photo:
                remove_by_name(upload_folder, "photo", exclude=f"photo.{hex}")

    return PersonIdResponse(id=str(person.id))


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
            PersonResponse(**item.dict())
            for item in persons_page.items
        ],
    )
