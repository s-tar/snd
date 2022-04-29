from enum import IntEnum
from typing import Optional

from odmantic import EmbeddedModel
from odmantic import Model
from pydantic.networks import EmailStr


class Roles(IntEnum):
    GUEST = 1
    EDITOR = 2
    MODERATOR = 3
    ADMIN = 4


class UserVerification(EmbeddedModel):
    code: int
    retries: int = 5


class User(Model):
    email: EmailStr
    name: str
    password: str
    role: Optional[Roles] = Roles.GUEST
    slava_ukraini: Optional[str] = None

    verification: Optional[UserVerification] = None
    verified: bool = False

    class Config:
        collection = "users"
