import contextlib
import os
import sqlite3
import unittest
from dataclasses import dataclass, astuple
from unittest.mock import Mock, patch

import trip_planner
import trip_planner.settings as settings
from trip_planner.cli import get_args
from trip_planner.database import (
    add_place,
    update_place,
    list_places,
    setup_database,
)
from trip_planner.datastructs import Place
from trip_planner.geolocation import get_location_info
from trip_planner.queries import *
from trip_planner.utils import (
    get_path,
    forget,
)


@dataclass
class Location:
    address: str
    latitude: float
    longitude: float


class TripPlannerTestCase(unittest.TestCase):
    def test_utils_get_path(self):
        module_name = "trip_planner"

        path = str(get_path())
        assert path.count(module_name) == 2

        path = str(get_path(".."))
        assert path.count(module_name) == 1

        path = str(get_path("../../"))
        assert path.count(module_name) == 0

        subpath = "some/path/"
        path = str(get_path(subpath))
        cutoff = path[path.rfind(module_name) + len(module_name):]
        assert cutoff.strip("/") == subpath.strip("/")

    def test_utils_forget(self):
        some_dict = {
            "name": "John",
            "age": 25,
            "is_available": True,
        }
        size = len(some_dict)

        assert len(forget(some_dict, "non_existing")) == size
        assert len(forget(some_dict, "name")) == (size - 1)
        assert len(forget(some_dict, "name", "age")) == (size - 2)
        assert len(forget(some_dict, "name", "age", "is_available")) == 0

    @patch('trip_planner.helpers.sqlite3', spec=sqlite3)
    def test_database(self, mock_sqlite3):
        mock_cursor = mock_sqlite3.connect.return_value.cursor

        mock_execute = mock_cursor.return_value.execute

        mock_fetchone = mock_cursor.return_value.fetchone
        row = (3, 'Name #3', 'Location name #3', 90.100, 110.120)
        mock_fetchone.return_value = row

        mock_fetchall = mock_cursor.return_value.fetchall
        rows = [
            (1, 'Name', 'Location name', 10.20, 30.40),
            (2, 'Name #2', 'Location name #2', 50.60, 70.80),
        ]
        mock_fetchall.return_value = rows

        setup_database()

        mock_execute.assert_called_with(CREATE_STMT)
        mock_execute.assert_called_once()

        places = list_places()

        mock_execute.assert_called_with(SELECT_ALL_STMT)
        assert mock_execute.call_count == 2
        mock_fetchall.assert_called_once()
        assert places == rows

        some_place = Place(*row)
        some_place_kwargs = forget(some_place._asdict(), "id")
        add_place(some_place)

        mock_execute.assert_called_with(
            INSERT_STMT,
            some_place_kwargs,
        )
        assert mock_execute.call_count == 3

        ret = update_place(some_place.id, **some_place_kwargs)

        mock_fetchone.assert_called_once()
        assert mock_execute.call_args_list[-2].args == (
            SELECT_SINGLE_STMT,
            (some_place.id,)
        )
        assert mock_execute.call_args_list[-1].args == (
            UPDATE_STMT,
            (
                tuple(some_place_kwargs.values())
                + (some_place.id,)
            ),
        )
        assert mock_execute.call_count == 5
        assert ret

    @patch('builtins.input')
    def test_geolocation_get_location_info(self, mock_input):
        with contextlib.redirect_stdout(None):
            some_place = "Test place"
            another_place = "Test place 2"

            places = [
                Location(some_place, 10.20, 30.40),
                Location(another_place, 50.60, 70.80),
            ]

            with patch.object(
                trip_planner.geolocation.Nominatim,
                'geocode',
                return_value=places[:1],
            ) as mock_nominatin:
                ret = get_location_info(some_place)

                assert mock_input.call_count == 0
                assert isinstance(ret, tuple)
                assert len(ret) == 3

            with patch.object(
                trip_planner.geolocation.Nominatim,
                'geocode',
                return_value=places,
            ) as mock_nominatin:
                mock_input.return_value = "1"

                ret = get_location_info(some_place)

                assert mock_input.call_count == 1
                assert astuple(places[0]) == ret
                assert isinstance(ret, tuple)
                assert len(ret) == 3

                mock_input.return_value = "2"

                ret = get_location_info(some_place)

                assert mock_input.call_count == 2
                assert astuple(places[1]) == ret
                assert isinstance(ret, tuple)
                assert len(ret) == 3

                ret = get_location_info(another_place, True)

                assert mock_input.call_count == 2
                assert astuple(places[0]) == ret
                assert isinstance(ret, tuple)
                assert len(ret) == 3

            with patch.object(
                trip_planner.geolocation.Nominatim,
                'geocode',
                side_effect=trip_planner.geolocation.GeocoderServiceError(),
            ) as mock_nominatin:
                ret = get_location_info(some_place)

                assert ret == (None, None, None)

    def test_cli_get_args(self):
        def turned_off(parsed, flags, excluded):
            return all(
                getattr(parsed, flag) == False
                for flag
                in flags
                if flag != excluded
            )

        fmt_action = lambda a: f'--{a}'

        available_flags = ['add', 'create_map', 'correct', 'list']

        selected_action = 'list'
        args = [fmt_action(selected_action)]
        parsed = get_args(args)
        assert parsed.list
        assert turned_off(parsed, available_flags, selected_action)

        selected_action = 'correct'
        args = [fmt_action(selected_action), '--id', '1']
        parsed = get_args(args)
        assert parsed.correct
        assert type(parsed.id)is int
        assert parsed.id == 1
        assert turned_off(parsed, available_flags, selected_action)

        selected_action = 'create-map'
        args = [fmt_action(selected_action)]
        parsed = get_args(args)
        assert parsed.create_map
        assert turned_off(
            parsed,
            available_flags,
            selected_action.replace('-', '_'),
        )

        selected_action = 'add'
        args = [fmt_action(selected_action), '--name', 'Test']
        parsed = get_args(args)
        assert parsed.add
        assert parsed.name == args[-1]
        assert turned_off(parsed, available_flags, selected_action)


if __name__ == '__main__':
    unittest.main()