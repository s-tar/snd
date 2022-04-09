from typing import Any
from typing import List

from schemas.base import BaseModel


class Pagination(BaseModel):
    items: List[Any]
    page: int
    per_page: int
    max_page: int
