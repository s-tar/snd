from typing import Optional

from odmantic import Model


class Squad(Model):
    name: str
    unit_number: Optional[str]
    address: Optional[str]
