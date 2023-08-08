from .cli import get_args
from .database import (
    add_place,
    list_places,
    update_place,
    setup_database,
)
from .geolocation import get_location_info
from .map_generator import generate_map


def main():
    args = get_args()

    if args.add:
        if args.name:
            location_info, lat, lon = get_location_info(args.name)
            if location_info and lat and lon:
                add_place(args.name, location_info, lat, lon)
                print(f"{args.name} added with location info: {location_info} ({lat}, {lon})")
            else:
                print("Failed to add the location. Please refine your search.")
        else:
            print("Please provide the name of the place to add.")

    if args.list:
        for place in list_places():
            print(place)

    if args.correct:
        places = list_places()
        if not places:
            print("No places found.")
            return

        # Display the list of places with IDs
        for place in places:
            print(f"ID: {place[0]} - Name: {place[1]} - Location: {place[2]} - Coordinates: ({place[3]}, {place[4]})")

        # If no ID is provided, default to the last place added
        place_id = args.id or places[-1][0]

        # Prompt user for new data
        name = input("Enter new name (press Enter to skip): ")
        new_location_info = input("Enter new location name (press Enter to skip): ")

        if new_location_info:
            location, lat, lon = get_location_info(new_location_info)
        else:
            location, lat, lon = None, None, None

        update_place(place_id, name, location, lat, lon)

    if args.create_map:
        generate_map()


if __name__ == "__main__":
    setup_database()
    main()
