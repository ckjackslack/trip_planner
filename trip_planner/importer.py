from time import sleep

from trip_planner.helpers import DB
from trip_planner.geolocation import get_location_info
from trip_planner.queries import INSERT_STMT
from trip_planner.settings import BASE_DIR


def get_data(prefix=""):
    with open(BASE_DIR / "trip_planner/data/places.txt", mode="r") as f:
        for line in f:
            line = line.strip()
            if line:
                yield (line, f"{prefix}{line}")


def data_importer():
    to_be_added = []
    data = sorted(get_data("Rome, "))
    print("Found:", len(data))
    for name, phrase in data:
        location_name, lat, lon = get_location_info(phrase, force=True)
        sleep(0.5)
        if location_name:
            to_be_added.append((name, location_name, lat, lon))
    print(f"Adding {len(to_be_added)} entries.")
    with DB() as cur:
        cur.executemany(INSERT_STMT, to_be_added)


def main():
    data_importer()


if __name__ == '__main__':
    main()