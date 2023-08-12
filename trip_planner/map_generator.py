import folium

from trip_planner.datastructs import ListOfPlaces, PlaceDC
from trip_planner.settings import MAP_PATH, ORIGIN


def generate_map(places: ListOfPlaces):
    if not places:
        print("Defaulting to origin point.")
        places = [
            PlaceDC.from_tuple(ORIGIN[1:]).dict(),
        ]

    first = places[0]
    m = folium.Map(
        location=[
            first.get("latitude"),
            first.get("longitude"),
        ],
        zoom_start=6,
    )

    for place in places:
        name, lat, lon = (
            place.get(key)
            for key
            in ["name", "latitude", "longitude"]
        )
        folium.Marker([lat, lon], tooltip=name).add_to(m)

    if len(places) > 1:
        m.fit_bounds([
            [
                place.get("latitude"),
                place.get("longitude"),
            ]
            for place
            in places
        ])

    try:
        m.save(MAP_PATH)
        print("Map generated and saved as trip_map.html!")
    except Exception as e:
        print(f"An error occurred while saving the map: {e}")
