from enum import Enum

from typing import List

from schemas.base import BaseModel


class Status(str, Enum):
    OK = "ok"
    FAIL = "fail"
    DATA_VALIDATION_FAILED = "data_validation_failed"
    USER_IS_NOT_VERIFIED = "user_is_not_verified"


class ResponseModel(BaseModel):
    status: Status = Status.OK


class ValidationFailError(BaseModel):
    field: str
    error: str


class ValidationFailResponse(ResponseModel):
    status: Status = Status.DATA_VALIDATION_FAILED
    errors: List[ValidationFailError]
