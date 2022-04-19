from fastapi import Depends
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from starlette.requests import Request
from starlette.responses import JSONResponse

from base import routing
from base.database import database
from base.email import email
from base.settings import get_settings
from starlette.middleware.cors import CORSMiddleware

from schemas.response import Status

settings = get_settings()
app = FastAPI(
    title=settings.app_title,
    root_path=settings.app_root_path,
    docs_url=settings.docs_path,
    redoc_url=None,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database.init(
    host=settings.database_host,
    port=settings.database_port,
    user=settings.database_username,
    password=settings.database_password,
    dbname=settings.database_name,
)
email.init(
    host=settings.email_host,
    port=settings.email_port,
    ssl=settings.email_ssl,
    tls=settings.email_tls,
    user=settings.email_user,
    password=settings.email_password,
    default_sender=settings.email_default_sender,
)

routing.init(app)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=200,
        content={
            "status": Status.DATA_VALIDATION_FAILED,
            "detail": exc.errors(),
        }
    )


def init_documentation(app):
    from models.user import User
    from services.user import get_current_user

    @app.get("/openapi.json")
    async def get_open_api_endpoint():
        return JSONResponse(
            get_openapi(title="FastAPI", version="1.0.0", routes=app.routes)
        )

    @app.get("/documentation")
    async def get_documentation(current_user: User = Depends(get_current_user)):
        return get_swagger_ui_html(openapi_url="/api/openapi.json", title="docs")


init_documentation(app)
