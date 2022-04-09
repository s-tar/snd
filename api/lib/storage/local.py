import os
import pathlib

from aiofile import async_open

from lib.storage.base import Storage


class LocalStorage(Storage):
    def __init__(self, storage_url, base_path=''):
        self.storage_url = storage_url
        self.base_path = base_path

    async def save(self, path, content):
        file_path = os.path.join(self.base_path, path)
        folder_path = pathlib.Path(os.path.dirname(file_path))
        folder_path.mkdir(parents=True, exist_ok=True)
        async with async_open(file_path, "wb+") as file:
            await file.write(content)

    def get_url(self, path):
        url_part = [self.storage_url]
        if self.base_path:
            url_part.append(self.base_path)
        url_part.append(str(path))
        return "/".join(part.rstrip("/") for part in url_part)
