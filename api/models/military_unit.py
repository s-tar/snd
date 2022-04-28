from typing import Optional

from odmantic import Model
from typing import List


class MilitaryUnit(Model):
    name: Optional[str]
    number: Optional[str]
    address: Optional[str]
    phones: Optional[List[int]]
    photo: Optional[str]
    disbanded: bool = True
