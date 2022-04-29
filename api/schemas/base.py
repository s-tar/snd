import json

import pydantic
from bson import ObjectId

from schemas.fields import MongoId


class BaseModel(pydantic.BaseModel):
    class Config:
        use_enum_values = True
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str,
            MongoId: str,
        }


class JsonRequestModel(BaseModel):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
