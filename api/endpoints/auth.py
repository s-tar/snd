from fastapi import APIRouter
from fastapi.params import Depends

from models.user import User
from schemas.response import Status
from schemas.token import Token

from services.auth import authenticate_user

from services.auth import get_access_token

router = APIRouter()


@router.post("/login", response_model=Token, response_model_exclude_none=True)
async def get_access_token_endpoint(
    user: User = Depends(authenticate_user),
):
    if not user.verified:
        return Token(id=str(user.id), status=Status.USER_IS_NOT_VERIFIED)

    access_token = get_access_token(user.id, user.password)
    return Token(
        id=str(user.id), access_token=access_token, token_type="bearer"
    )
