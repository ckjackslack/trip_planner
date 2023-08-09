import os

import folium

from .database import list_places
from .settings import ORIGIN


def generate_map():
    places = list_places()

    # Check if there are any places in the database
    if not places:
        print("No locations found in the database.")
        print("Defaulting to origin point.")
        places = [ORIGIN]

    # Create a base map
    m = folium.Map(location=[places[0][3], places[0][4]], zoom_start=6)

    # Add markers for each place
    for _, name, _, lat, lon in places:
        folium.Marker([lat, lon], tooltip=name).add_to(m)

    # Adjust the map to fit all markers
    if len(places) > 1:
        m.fit_bounds([[place[3], place[4]] for place in places])

    # Save the map to an HTML file
    try:
        m.save(
            os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                "views",
                "trip_map.html",
            ),
        )
        print("Map generated and saved as trip_map.html!")
    except Exception as e:
        print(f"An error occurred while saving the map: {e}")
