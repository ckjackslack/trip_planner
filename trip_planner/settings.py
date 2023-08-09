from bottle import TEMPLATE_PATH

from trip_planner.utils import get_path


BASE_DIR = str(get_path(".."))
DB_FILE = "trip_planner.db"
ORIGIN = (0, "Kielce", "Kielce", 50.866059, 20.627303)
HOST = 'localhost'
MAIN_TEMPLATE_PATH = get_path("views")
MAP_FILE = "trip_map.html"
MAP_PATH = str(MAIN_TEMPLATE_PATH / MAP_FILE)
PORT = 8080
STATIC_PATH = str(get_path("static"))
TEMPLATE_PATH.insert(0, str(MAIN_TEMPLATE_PATH))