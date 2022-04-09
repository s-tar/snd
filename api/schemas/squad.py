from typing import Dict

from schemas.base import BaseModel
from schemas.fields import NotEmptyString
from schemas.response import ResponseModel


class Squad(BaseModel):
    name: NotEmptyString
    unit_number: str = None
    address: str = None


class AddSquadRequest(Squad):
    pass


class SquadIdResponse(ResponseModel):
    id: str


class SquadResponse(Squad):
    pass


class SquadByIdListResponse(ResponseModel):
    squads: Dict[str, SquadResponse]
