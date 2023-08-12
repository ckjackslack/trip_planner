from collections import ChainMap

from peewee import (
    CharField,
    DoubleField,
    Model,
    SqliteDatabase,
)

from trip_planner.settings import DB_FILE, ORIGIN
from trip_planner.utils import calculate_distance


db = SqliteDatabase(DB_FILE)


class BaseModel(Model):
    class Meta:
        database = db


class Place(BaseModel):
    name = CharField()
    location = CharField()
    latitude = DoubleField()
    longitude = DoubleField()

    def get_coords(self):
        return (self.latitude, self.longitude)

    @classmethod
    def add_place(cls, name, location, latitude, longitude):
        cls.create(
            name=name,
            location=location,
            latitude=latitude,
            longitude=longitude,
        )

    @classmethod
    def get_places(cls):
        return [
            dict(ChainMap({
                col: getattr(place, col)
                for col
                in list(cls._meta.fields)
            }, {
                "distance": calculate_distance(
                    place.get_coords(),
                    ORIGIN[-2:],
                )
            }))
            for place
            in cls.select()
        ]

    @classmethod
    def clear_places(cls):
        query = cls.delete()
        query.execute()
