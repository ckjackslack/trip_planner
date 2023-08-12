from trip_planner.datastructs import PlaceDC
from trip_planner.helpers import DB
from trip_planner.queries import *


def which_db():
    with DB() as cur:
        db_path = tuple(cur.execute("PRAGMA database_list").fetchone())[-1]
        print(db_path)


def setup_database():
    with DB() as cur:
        cur.execute(CREATE_STMT)


def add_place(place: PlaceDC):
    vals = tuple(place.dict("id").values())
    with DB() as cur:
        cur.execute(
            INSERT_STMT,
            vals,
        )


def find_place(place_id: int):
    with DB() as cur:
        cur.execute(
            SELECT_SINGLE_STMT,
            (place_id,),
        )
        return cur.fetchone()


def update_place(place: PlaceDC):
    existing = find_place(place.id)
    if not existing:
        return False

    existing = PlaceDC.from_tuple(tuple(existing))

    data = existing.dict() | place.dict()
    del data["id"]

    data = PlaceDC(**data)

    with DB() as cur:
        cur.execute(
            UPDATE_STMT,
            (
                data.as_tuple()[1:]
                + (place.id,)
            ),
        )
        return True


def list_places(as_dict=False):
    with DB() as cur:
        cur.execute(SELECT_ALL_STMT)
        return [
            tuple(place)
            if not as_dict
            else dict(place)
            for place
            in cur.fetchall()
        ]


def clear_places():
    with DB() as cur:
        cur.execute(DELETE_ALL_STMT)
