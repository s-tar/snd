import datetime
from typing import Optional

from odmantic import EmbeddedModel
from odmantic import Field
from odmantic import Model
from odmantic import ObjectId
from typing import List

from constants.countries import CountryCodes
from constants.person import PersonStatus
from constants.person import PersonType
from constants.person import Relationship
from schemas.fields import Date


class Social(EmbeddedModel):
    vk: Optional[str]
    ok: Optional[str]
    fb: Optional[str]


class Doc(EmbeddedModel):
    number: str
    date: Optional[Date]
    authority: Optional[str]


class Military(EmbeddedModel):
    number: Optional[str]
    ticket: Optional[Doc]
    rank: Optional[str]
    post: Optional[str]
    unit: Optional[ObjectId]


class Relative(EmbeddedModel):
    name: str
    relationship: Relationship
    photo: Optional[str]
    birthday: Optional[Date]
    address: Optional[str]
    phones: Optional[List[int]]
    social: Optional[Social]
    passport: Optional[Doc]


class Person(Model):
    code: str
    first_name: str
    last_name: str
    middle_name: Optional[str]

    type: PersonType

    country: CountryCodes

    photo: Optional[str]
    birthday: Optional[Date]
    city_of_birth: Optional[str]
    addresses: Optional[List[str]]

    passport: Optional[Doc]
    identification_number: Optional[str]
    insurance_number: Optional[str]

    phones: Optional[List[int]]
    email: Optional[str]

    social: Optional[Social]

    military: Optional[Military]

    relatives: Optional[List[Relative]]

    status: Optional[PersonStatus] = PersonStatus.ALIVE

    tags: Optional[List[str]]

    extra: Optional[str]

    sources: Optional[List[str]]

    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    deleted_at: Optional[datetime.datetime]
