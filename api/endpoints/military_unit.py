from bson import ObjectId
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from starlette import status
from typing import List

from base.database import database
from lib.pagination import paginate
from models.military_unit import MilitaryUnit
from models.user import User
from schemas.military_unit import AddManyMilitaryUnitsRequest
from schemas.person import AddManyPersonRequest
from schemas.response import Status
from schemas.military_unit import AddMultipleResponse
from schemas.military_unit import AddMilitaryUnitRequest
from schemas.military_unit import MilitaryUnitByNumberListResponse
from schemas.military_unit import MilitaryUnitIdResponse
from schemas.military_unit import MilitaryUnitResponse
from services.user import get_editor

router = APIRouter()


@router.post(
    "/add",
    status_code=status.HTTP_200_OK,
    response_model=MilitaryUnitIdResponse,
    responses={
        status.HTTP_403_FORBIDDEN: {"description": "Operation forbidden"},
    },
    summary="Add military init"
)
async def add_military_unit_endpoint(
    data: AddMilitaryUnitRequest,
    editor: User = Depends(get_editor),
):
    unit = MilitaryUnit(**data.dict(exclude_none=True))
    await database.save(unit)

    return MilitaryUnitIdResponse(id=str(unit.id))


@router.post(
    "/add_many",
    status_code=status.HTTP_200_OK,
    response_model=AddMultipleResponse,
    responses={
        status.HTTP_403_FORBIDDEN: {"description": "Operation forbidden"},
    },
    summary="Add multiple military units"
)
async def add_many_military_units_endpoint(
    data: AddManyMilitaryUnitsRequest,
    editor: User = Depends(get_editor),
):
    units = []
    fails = {}
    for i, unit_data in enumerate(data.units):
        if not unit_data.name and not unit_data.number:
            fails[i] = "Name or unit number is not found"
            continue

        unit = MilitaryUnit(**unit_data.dict(exclude_unset=True))
        units.append(unit)

    if units:
        await database.save_all(units)

    return AddMultipleResponse(fails=fails)


@router.get(
    "/get",
    status_code=status.HTTP_200_OK,
    response_model=MilitaryUnitByNumberListResponse,
    summary="Get military units"
)
async def get_military_units_by_number_endpoint(
    page: int = 1,
    per_page: int = 20,
    ids: List[str] = Query(None),
):
    query = {}
    if ids:
        query = MilitaryUnit.id.in_([
            ObjectId(unit_id)
            for unit_id in ids
        ])

    page = await paginate(
        entity=MilitaryUnit,
        query=query,
        page=page,
        per_page=per_page,
    )

    return MilitaryUnitByNumberListResponse(
        status=Status.OK,
        page=page.page,
        per_page=page.per_page,
        max_page=page.max_page,
        total=page.total,
        items=[
            MilitaryUnitResponse(**item.dict())
            for item in page.items
        ],
    )


@router.get(
    "/search",
    status_code=status.HTTP_200_OK,
    response_model=MilitaryUnitByNumberListResponse,
    summary="Search military units"
)
async def search_military_units_endpoint(
    page: int = 1,
    per_page: int = 20,
    s: str = None,
):
    query = {}
    if s:
        search = '"' + '" "'.join(s.split()) + '"'
        query = {"$text": {"$search": search}}

    page = await paginate(
        entity=MilitaryUnit,
        query=query,
        page=page,
        per_page=per_page,
    )

    return MilitaryUnitByNumberListResponse(
        status=Status.OK,
        page=page.page,
        per_page=page.per_page,
        max_page=page.max_page,
        total=page.total,
        items=[
            MilitaryUnitResponse(**item.dict())
            for item in page.items
        ],
    )
