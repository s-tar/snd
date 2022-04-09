from hashlib import md5
from random import randint

from bson import ObjectId
from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from base.database import database
from base.settings import Settings
from base.settings import get_settings
from jose import JWTError, jwt

from models.user import Roles
from models.user import User


class Permissions:
    READ = 0b001
    EDIT = 0b010
    APPROVE = 0b100


RolePermissions = {
    Roles.GUEST: Permissions.READ,
    Roles.EDITOR: Permissions.READ | Permissions.EDIT,
    Roles.MODERATOR: (
        Permissions.READ | Permissions.EDIT | Permissions.APPROVE
    ),
    Roles.ADMIN: (
        Permissions.READ | Permissions.EDIT | Permissions.APPROVE
    )
}


OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="auth/login")
CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

PERMISSIONS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User don't have permissions",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_verification_code():
    return randint(100000, 999999)


async def get_current_user(
    token: str = Depends(OAUTH2_SCHEME),
    setting: Settings = Depends(get_settings)
):
    try:
        payload = jwt.decode(
            token,
            setting.token_secret_key,
            algorithms=[setting.token_algorithm]
        )

        user_id: str = payload.get("sub")
        password_hash: str = payload.get("hash")
        if not (user_id and password_hash):
            raise CREDENTIALS_EXCEPTION

        user = await database.find_one(User, User.id == ObjectId(user_id))
        if (
            user and
            user.password and
            md5(user.password.encode()).hexdigest() == password_hash
        ):
            return user

        raise CREDENTIALS_EXCEPTION
    except JWTError:
        raise CREDENTIALS_EXCEPTION


async def get_editor(
    user: User = Depends(get_current_user)
):
    if has_permissions(user, Permissions.EDIT):
        return user

    raise PERMISSIONS_EXCEPTION


def has_permissions(user, permissions):
    return bool(RolePermissions.get(user.role, 0) & permissions)
