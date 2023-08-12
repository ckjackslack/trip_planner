import sys
sys.dont_write_bytecode = True

from flask import (
    Flask,
    g,
    jsonify,
    render_template,
    request,
)

from trip_planner.geolocation import get_location_info
from trip_planner.helpers import no_cache
from trip_planner.map_generator import generate_map
from trip_planner.models import (
    Place as PlaceModel,
    db,
)
from trip_planner.utils import setup_logging
from trip_planner import settings


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
setup_logging(app)


@app.before_request
def before_request():
    g.db = db
    g.db.connect()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, "db", None)
    if db is not None:
        db.close()


@app.route("/", methods=["GET"])
def index():
    return render_template("index.tpl")


@app.route("/add_locations", methods=["POST"])
def add_locations():
    place = request.form.get("place")
    locations = request.form.get('locs')
    locations = [l.strip() for l in locations.strip().split("\r\n")]

    no_of_locations = len(locations)

    no_of_errors = 0
    for location in locations:
        location_name, lat, lon = get_location_info(
            f"{place}, {location}",
            force=True,
        )
        if location_name:
            PlaceModel.add_place(location, location_name, lat, lon)
        else:
            no_of_errors += 1

    no_of_added = no_of_locations - no_of_errors

    return jsonify({
        "msg": f"Added {no_of_added} of {no_of_locations} locations.",
    })


@app.route("/get_locations", methods=["GET"])
def get_locations():
    places = PlaceModel.get_places()
    return jsonify(locations=places)


@app.route("/clear_locations", methods=["DELETE"])
def clear_locations():
    PlaceModel.clear_places()
    return ('', 204)


@app.route("/create_map", methods=["GET"])
def create_map():
    places = PlaceModel.get_places()
    generate_map(places)
    return ('', 200)


@app.route("/map", methods=["GET"])
@no_cache
def show_map():
    return render_template("trip_map.html")


if __name__ == "__main__":
    app.run(host=settings.HOST, port=settings.PORT)
