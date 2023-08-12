from dataclasses import (
    asdict,
    dataclass,
    field,
)
from typing import List, TypedDict


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
    id: int = field(init=False, default=None)

    @classmethod
    def from_tuple(cls, tup):
        return cls(*tup)

    def dict(self):
        value = asdict(self)
        del value["id"]
        return value

    def __post_init__(self):
        self.distance = None


ListOfPlaces = List[PlaceDict]