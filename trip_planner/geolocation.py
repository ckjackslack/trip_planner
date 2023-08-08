from geopy.exc import GeocoderServiceError
from geopy.geocoders import Nominatim


def get_location_info(place_name, force=False):
    geolocator = Nominatim(user_agent="trip_planner")
    try:
        location = geolocator.geocode(place_name, exactly_one=False)

        if len(location) == 1:
            return (
                location[0].address,
                location[0].latitude,
                location[0].longitude,
            )

        print("Multiple matches found. Please select one:")
        for idx, loc in enumerate(location, 1):
            print(f"{idx}. {loc.address}")

        if force:
            choice = 1
        else:
            choice = int(input("Enter choice number: "))
        chosen_location = location[choice-1]
        return (
            chosen_location.address,
            chosen_location.latitude,
            chosen_location.longitude,
        )

    except GeocoderServiceError as e:
        print(f"Error occurred while geocoding: {e}")
        return None, None, None
