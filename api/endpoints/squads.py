from bson import ObjectId
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from starlette import status
from typing import List

from base.database import database
from lib.pagination import paginate
from models.squad import Squad
from models.user import User
from schemas.response import Status
from schemas.squad import AddSquadRequest
from schemas.squad import SquadByIdListResponse
from schemas.squad import SquadIdResponse
from schemas.squad import SquadResponse
from services.user import get_editor

router = APIRouter()


@router.post(
    "/add",
    status_code=status.HTTP_200_OK,
    response_model=SquadIdResponse,
    responses={
        status.HTTP_403_FORBIDDEN: {"description": "Operation forbidden"},
    },
    summary="Add squad"
)
async def add_squad_endpoint(
    data: AddSquadRequest,
    editor: User = Depends(get_editor),
):
    squad = Squad(**data.dict(exclude_none=True))
    await database.save(squad)

    return SquadIdResponse(id=str(squad.id))


@router.get(
    "/get",
    status_code=status.HTTP_200_OK,
    response_model=SquadByIdListResponse,
    summary="Get squads"
)
async def get_squads_by_ids_endpoint(
    page: int = 1,
    per_page: int = 20,
    ids: List[str] = Query(None),
):
    query = {}
    if ids:
        query = Squad.id.in_([
            ObjectId(squad_id)
            for squad_id in ids
            if ObjectId.is_valid(squad_id)
        ])

    squad_page = await paginate(
        entity=Squad,
        query=query,
        page=page,
        per_page=per_page,
    )

    return SquadByIdListResponse(
        status=Status.OK,
        page=squad_page.page,
        per_page=squad_page.per_page,
        max_page=squad_page.max_page,
        items=[
            SquadResponse(**item.dict())
            for item in squad_page.items
        ],
    )
