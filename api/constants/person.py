from enum import IntEnum


class PersonType(IntEnum):
    HUYLO = 1
    MILITARY = 2
    BETRAYER = 3


class PersonStatus(IntEnum):
    ALIVE = 1
    DEAD = 2
    POW = 3
    PRISONED = 4
    SND = 5


class Relationship(IntEnum):
    SON = 1
    DAUGHTER = 2
    WIFE = 3
    HUSBAND = 4

    MOTHER = 5
    FATHER = 6
    BROTHER = 7
    SISTER = 8

    GRANDMOTHER = 9
    GRANDFATHER = 10
    COUSIN_BROTHER = 11
    COUSIN_SISTER = 12
    AUNT = 13
    UNCLE = 14

    STEPFATHER = 15
    STEPMOTHER = 16
