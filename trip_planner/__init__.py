import importlib
import json

import bottle

from trip_planner.datastructs import json_dumps
from trip_planner import settings

json.dumps = json_dumps

importlib.reload(bottle)
bottle.TEMPLATE_PATH.insert(0, str(settings.MAIN_TEMPLATE_PATH))

bottle.json_dumps = json_dumps
