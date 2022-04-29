from typing import Dict

from typing import List

from schemas.base import BaseModel
from schemas.fields import MongoId
from schemas.pagination import Pagination
from schemas.response import ResponseModel


class MilitaryUnit(BaseModel):
    name: str = None
    number: str = None
    address: str = None
    phones: List[int] = None
    photo: str = None


class AddMilitaryUnitRequest(MilitaryUnit):
    pass


class MilitaryUnitIdResponse(ResponseModel):
    id: str


class MilitaryUnitResponse(MilitaryUnit):
    id: MongoId


class MilitaryUnitByNumberListResponse(ResponseModel, Pagination):
    items: List[MilitaryUnitResponse]


class AddManyMilitaryUnitsRequest(BaseModel):
    units: List[MilitaryUnit]


class AddMultipleResponse(ResponseModel):
    fails: Dict[int, str]
