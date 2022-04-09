from enum import Enum
from functools import lru_cache

from base.settings import get_settings
from lib.storage.local import LocalStorage
setting = get_settings()


class StorageType(str, Enum):
    LOCAL = "local"


@lru_cache()
def get_storage():
    storage_type = StorageType(setting.storage_type)
    if storage_type == StorageType.LOCAL:
        return LocalStorage(
            storage_url=setting.storage_url,
            base_path=setting.storage_base_folder,
        )
