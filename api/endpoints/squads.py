from bson import ObjectId
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from starlette import status
from typing import List

from base.database import database
from models.squad import Squad
from models.user import User
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
    summary="Get squads by ids"
)
async def all_squads_by_ids_endpoint(ids: List[str] = Query(None)):
    squad_ids = [
        ObjectId(squad_id)
        for squad_id in ids
        if ObjectId.is_valid(squad_id)
    ]
    squads = {
        str(squad.id): SquadResponse(**squad.dict())
        for squad in await database.find(Squad, Squad.id.in_(squad_ids))
    }

    return SquadByIdListResponse(
        squads=squads,
    )
