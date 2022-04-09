from schemas.response import ResponseModel


class Token(ResponseModel):
    id: str = None
    access_token: str = None
    token_type: str = None
