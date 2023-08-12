from collections import deque
from dataclasses import (
    asdict,
    dataclass,
    field,
)
from typing import List, TypedDict

from trip_planner.utils import forget


class PlaceDict(TypedDict):
    id: int
    name: str
    location: str
    latitude: float
    longitude: float
    distance: float


@dataclass
class PlaceDC:
    name: str
    location: str
    latitude: float
    longitude: float
    id: int = field(default=None)

    @classmethod
    def from_tuple(cls, tup):
        if isinstance(tup[0], int):
            return cls(*tup[1:], tup[0])
        else:
            return cls(*tup)

    def as_tuple(self, for_update=False):
        fields = list(self.__dataclass_fields__.keys())
        if not for_update:
            fields = deque(fields, maxlen=len(fields))
            fields.rotate(1)
            fields = list(fields)
        vals = [
            getattr(self, field)
            for field
            in fields
        ]
        return tuple(vals)

    def dict(self, *excludes):
        ret = asdict(self)
        if excludes:
            ret = forget(ret, *excludes)
        return ret

    def __post_init__(self):
        self.distance = None


ListOfPlaces = List[PlaceDict]