from trip_planner.datastructs import Place
from trip_planner.helpers import DB
from trip_planner.queries import *
from trip_planner.utils import (
    calculate_distance,
    forget,
)


def setup_database():
    with DB() as cur:
        cur.execute(CREATE_STMT)


def add_place(place: Place):
    vals = tuple(forget(place._asdict(), "id").values())
    with DB() as cur:
        cur.execute(
            INSERT_STMT,
            vals,
        )


def update_place(place_id: int, **kwargs):
    with DB() as cur:
        cur.execute(
            SELECT_SINGLE_STMT,
            (place_id,),
        )
        result = cur.fetchone()
        if not result:
            return False
        else:
            result = Place(*result)
            kwargs.update({
                "name": result.name,
                "location": result.location,
                "latitude": result.latitude,
                "longitude": result.longitude,
            })

        cur.execute(
            UPDATE_STMT,
            (
                tuple(kwargs.values())
                + (result.id,)
            ),
        )
        return True


def list_places():
    with DB() as cur:
        cur.execute(SELECT_ALL_STMT)
        places = cur.fetchall()
        return [
            Place.from_tuple(place)
            for place
            in places
        ]


def clear_places():
    with DB() as cur:
        cur.execute(DELETE_ALL_STMT)
