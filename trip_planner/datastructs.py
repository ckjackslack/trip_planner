import json
from dataclasses import (
    asdict,
    dataclass,
    field,
    is_dataclass,
)
from functools import partial

from trip_planner.settings import ORIGIN
from trip_planner.utils import calculate_distance


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if is_dataclass(o):
            return asdict(o)
        return super().default(o)


@dataclass
class Place:
    name: str
    location: str
    latitude: float
    longitude: float
    id: int = field(default=None)
    distance: float = field(init=False)

    def get_coords(self):
        return (self.latitude, self.longitude)

    def __post_init__(self):
        self.distance = calculate_distance(
            ORIGIN[-2:],
            self.get_coords(),
        )

    @classmethod
    def from_tuple(cls, row):
        row_id, *rest = row
        return cls(*rest, row_id)


json_dumps = partial(json.dumps, cls=EnhancedJSONEncoder)