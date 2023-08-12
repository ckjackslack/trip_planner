from trip_planner.utils import get_path


BASE_DIR = str(get_path(".."))

DB_FILE = "trip_planner.db"

ORIGIN = (0, "Kielce", "Kielce", 50.866059, 20.627303)

HOST = 'localhost'

TEMPLATE_PATH = get_path("templates")
MAP_FILE = "trip_map.html"
MAP_PATH = str(TEMPLATE_PATH / MAP_FILE)

PORT = 5000

STATIC_PATH = str(get_path("static"))
