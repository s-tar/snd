import datetime
import json

from typing import List

from typing import Dict
from typing import Optional

from constants.countries import CountryCodes
from constants.person import PersonStatus
from constants.person import PersonType
from constants.person import Relationship
from constants.ranks import Rank
from schemas.base import BaseModel
from schemas.fields import MongoId
from schemas.fields import NotEmptyString
from schemas.pagination import Pagination
from schemas.response import ResponseModel


class Social(BaseModel):
    ok: str = None
    vk: str = None
    fb: str = None


class Doc(BaseModel):
    number: str
    date: datetime.date = None
    authority: str = None


class Military(BaseModel):
    number: str = None
    ticket: Doc = None
    rank: Rank = None
    post: str = None
    unit: MongoId = None


class Relative(BaseModel):
    name: str
    relationship: Relationship
    photo: Optional[str]
    birthday: Optional[datetime.date]
    address: Optional[str]
    phones: Optional[List[int]]
    social: Optional[Social]
    passport: Optional[Doc]


class Person(BaseModel):
    first_name: NotEmptyString
    last_name: NotEmptyString
    middle_name: str = None

    type: PersonType = PersonType.MILITARY

    country: CountryCodes = None
    addresses: Optional[List[str]] = None
    photo: str = None
    birthday: datetime.date = None
    city_of_birth: str = None

    passport: Doc = None
    identification_number: str = None
    insurance_number: str = None

    phones: Optional[List[int]]
    email: str = None

    social: Social = None

    military: Military = None

    relatives: Optional[List[Relative]]

    status: PersonStatus = PersonStatus.ALIVE

    extra: str = None

    tags: Optional[List[str]]

    sources: Optional[List[str]]


class SavePersonRequest(Person):
    id: MongoId = None
    first_name: str = None
    last_name: str = None
    middle_name: str = None

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class UpdatePersonRequest(Person):
    pass


class AddManyPersonRequest(BaseModel):
    persons: List[Person]


class PersonPublicData(Person):
    id: MongoId
    code: str


class PersonListResponse(Pagination, ResponseModel):
    items: List[PersonPublicData]


class PersonIdResponse(ResponseModel):
    id: str


class AddMultipleResponse(ResponseModel):
    fails: Dict[int, str]


class PersonResponse(ResponseModel):
    person: PersonPublicData
