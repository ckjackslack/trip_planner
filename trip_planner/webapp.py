import os

from bottle import (
    abort,
    get,
    request,
    response,
    route,
    run,
    static_file,
    template,
)

import trip_planner.settings as settings
from trip_planner.database import (
    add_place,
    list_places,
    setup_database,
)
from trip_planner.datastructs import Place
from trip_planner.geolocation import get_location_info
from trip_planner.map_generator import generate_map as genmap


@route('/')
def index():
    if not os.path.isfile(settings.DB_FILE):
        setup_database()
    return template('index')


@route('/map')
def show_locations():
    if not os.path.isfile(settings.MAP_PATH):
        abort(404, "No map file")
    return template(settings.MAP_PATH)


@route('/add_location', method='POST')
def add_location():
    name = request.forms.get('name')
    location_name = request.forms.get('location_name')
    location, lat, lon = get_location_info(location_name, force=True)
    if location:
        place = Place(None, name, location, lat, lon)
        add_place(place)
    return "Location Added" if location else "Failed to Add Location"


@route('/get_locations', method='GET')
def get_locations():
    response.content_type = 'application/json'
    return {
        "locations": list_places(),
    }


@route('/generate_map', method="GET")
def generate_map():
    try:
        genmap()
        ret = "success"
        error = None
    except Exception as e:
        ret = "failure"
        error = str(e)
    response.content_type = 'application/json'
    return {
        "outcome": ret,
        "error": error,
    }


@get('/static/<filename:path>')
def send_static(filename):
    response = static_file(filename, root=settings.STATIC_PATH)
    response.set_header("Cache-Control", "no-cache")
    return response


if __name__ == "__main__":
    run(
        debug=True,
        host=settings.HOST,
        port=settings.PORT,
        reloader=True,
    )
