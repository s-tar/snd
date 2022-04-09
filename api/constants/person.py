from enum import IntEnum


class PersonType(IntEnum):
    HUYLO = 1
    MILITARY = 2
    BETRAYER = 3


class PersonStatus(IntEnum):
    DEAD = 1
    ALIVE = 2
    POW = 3
    PRISONED = 4


class Relationship(IntEnum):
    SON = 1
    DAUGHTER = 2
    WIFE: 3
    HUSBAND: 4

    MOTHER = 5
    FATHER = 6
    BROTHER = 7
    SISTER = 8

    GRANDMOTHER = 9
    GRANDFATHER = 10
    COUSIN = 11
    AUNT = 12
    UNCLE = 13
