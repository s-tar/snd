from datetime import datetime
from datetime import timedelta
from hashlib import md5
from typing import Optional

from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from base.database import database
from base.settings import get_settings
from passlib.context import CryptContext

from jose import jwt

from models.user import User

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000
)

DEFAULT_EXPIRES_MINUTES = 24 * 60
AUTHENTICATION_ERROR = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)


def encrypt_password(password: str) -> str:
    return pwd_context.encrypt(password)


def check_encrypted_password(password: str, hashed: str) -> str:
    return pwd_context.verify(password, hashed)


def create_access_token(
    data: dict,
    secret_key: str,
    algorithm: str,
    expires: Optional[int] = None,
) -> str:
    to_encode = data.copy()
    exp = expires or DEFAULT_EXPIRES_MINUTES
    to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=exp)})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm)

    return encoded_jwt


async def authenticate_user(
    auth_data: OAuth2PasswordRequestForm = Depends(),
) -> User:
    user = await database.find_one(User, User.email == auth_data.username)
    if not user:
        raise AUTHENTICATION_ERROR

    if not check_encrypted_password(auth_data.password, user.password):
        raise AUTHENTICATION_ERROR

    return user


def get_access_token(
    user_id,
    user_password_hash,
):
    settings = get_settings()
    return create_access_token(
        data={
            "sub": str(user_id),
            "hash": md5(user_password_hash.encode()).hexdigest(),
        },
        secret_key=settings.token_secret_key,
        algorithm=settings.token_algorithm,
        expires=settings.token_expire_minutes,
    )
