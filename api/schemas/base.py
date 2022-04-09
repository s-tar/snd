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
