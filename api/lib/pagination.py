from collections import namedtuple
from math import ceil

from base.database import database

MAX_PER_PAGE = 50
Page = namedtuple("Page", ["items", "page", "per_page", "max_page"])


async def paginate(
    entity,
    query,
    page: int = 1,
    per_page: int = 10,
):
    per_page = min(MAX_PER_PAGE, per_page)
    total = await database.count(entity, query)
    skip_count = per_page * (page - 1 if page > 1 else 0)
    items = await database.find(entity, query, limit=per_page, skip=skip_count)

    return Page(
        items=items,
        page=page,
        per_page=per_page,
        max_page=ceil(total / per_page),
    )
