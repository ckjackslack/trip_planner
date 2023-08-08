import os

from bottle import (
    TEMPLATE_PATH,
    request,
    response,
    route,
    run,
    static_file,
    template,
)

from trip_planner.database import add_place, list_places
from trip_planner.geolocation import get_location_info


get_path = lambda p: os.path.join(os.path.abspath(os.path.dirname(__file__)), p)

STATIC_PATH = get_path("static")
TEMPLATE_PATH.insert(0, get_path("views"))
print(TEMPLATE_PATH)


@route('/')
def index():
    return template('index')


@route('/map')
def show_locations():
    return template('trip_map.html')


@route('/add_location', method='POST')
def add_location():
    name = request.forms.get('name')
    location_name = request.forms.get('location_name')
    location, lat, lon = get_location_info(location_name, force=True)
    if location:
        add_place(name, location, lat, lon)
    return "Location Added" if location else "Failed to Add Location"


@route('/get_locations', method='GET')
def get_locations():
    locations = list_places()
    response.content_type = 'application/json'
    return {"locations": locations}


# You can also add static routing if you have css or js
@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root=STATIC_PATH)


if __name__ == "__main__":
    run(host='localhost', port=8080)
