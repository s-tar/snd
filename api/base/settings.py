from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_root_path: str
    app_title: str

    docs_path: str

    database_protocol: str
    database_host: str
    database_username: str
    database_password: str
    database_port: int
    database_name: str

    token_secret_key: str
    token_algorithm: str
    token_expire_minutes: int

    storage_type: str = ""
    storage_url: str = ""
    storage_base_folder: str = ""

    file_upload_folder: str = "upload"

    email_host: str = ""
    email_port: int = 25
    email_tls: bool = False
    email_ssl: bool = False
    email_user: str = ""
    email_password: str = ""
    email_default_sender: str = ""


@lru_cache()
def get_settings():
    return Settings()
