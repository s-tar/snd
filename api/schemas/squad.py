from typing import Dict

from typing import List

from schemas.base import BaseModel
from schemas.fields import MongoId
from schemas.fields import NotEmptyString
from schemas.pagination import Pagination
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
    id: MongoId


class SquadByIdListResponse(ResponseModel, Pagination):
    items: List[SquadResponse]
