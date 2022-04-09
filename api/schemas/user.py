import re

from pydantic import BaseModel
from pydantic import validator
from pydantic.networks import EmailStr

from schemas.fields import MongoId
from schemas.fields import NotEmptyString
from schemas.response import ResponseModel


class UserResponse(ResponseModel):
    id: MongoId
    name: str
    email: EmailStr


class UserWithTokenResponse(UserResponse):
    access_token: str = ""
    token_type: str = ""


class CreateUserRequest(BaseModel):
    name: NotEmptyString
    email: EmailStr
    password: NotEmptyString
    repassword: NotEmptyString

    @validator('password')
    def password_strength(cls, v):
        """
            Verify the strength of 'password'
            A password is considered strong if:
                8 characters length or more
                1 digit or more
                1 uppercase letter or more
                1 lowercase letter or more
        """
        if len(v) < 8:
            raise ValueError("Password should be at least 8 symbols")

        if not re.search(r"\d", v):
            raise ValueError("Password should contain at least one number")

        if v.lower() == v:
            raise ValueError(
                "Password should contain at least one uppercase letter"
            )

        if v.upper() == v:
            raise ValueError(
                "Password should contain at least one lowercase letter"
            )

        return v

    @validator('repassword')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v


class VerifyUserRequest(BaseModel):
    id: NotEmptyString
    code: NotEmptyString
