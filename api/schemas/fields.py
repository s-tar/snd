import datetime
import re

from bson import ObjectId
from pydantic import BaseModel


class MongoId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class NotEmptyString(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        value = v.strip()
        if not value:
            raise TypeError('Can not be empty.')
        return cls(value)


class Code(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        value = v.strip()
        if not value:
            raise TypeError('Can not be empty.')
        if not re.match("^[A-Za-z0-9_-]*$", value):
            raise TypeError(
                'Code can contain only english letters, underscore or dash'
            )

        return cls(value)


class Date(datetime.datetime):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        return datetime.datetime(v.year, v.month, v.day)


class PhotoContainer(BaseModel):
    width: int
    height: int
    left: int
    top: int
