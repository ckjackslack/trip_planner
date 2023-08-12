from trip_planner.cli import get_args
from trip_planner.database import (
    add_place,
    list_places,
    update_place,
    setup_database,
)
from trip_planner.datastructs import PlaceDC
from trip_planner.geolocation import get_location_info
from trip_planner.map_generator import generate_map


def main():
    args = get_args()

    if args.add:
        if args.name:
            location_info, lat, lon = get_location_info(args.name)
            if location_info and lat and lon:
                place = PlaceDC(args.name, location_info, lat, lon)
                add_place(place)
                print(f"{args.name} added with location info: {location_info} ({lat}, {lon})")
            else:
                print("Failed to add the location. Please refine your search.")
        else:
            print("Please provide the name of the place to add.")

    if args.list:
        for place in list_places():
            print(place)

    if args.correct:
        if not args.id:
            print("No ID provided.")
            return

        name = input("Enter new name: ")
        new_location_info = input("Enter new location name: ")

        if not name or not new_location_info:
            print("You need to provide both name and location name.")
            return

        location, lat, lon = get_location_info(new_location_info)

        place = PlaceDC(name, location, lat, lon, args.id)
        update_place(place)

    if args.create_map:
        generate_map(list_places(as_dict=True))


if __name__ == "__main__":
    setup_database()
    main()
