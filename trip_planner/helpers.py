import sqlite3
from collections import namedtuple
from functools import wraps

from flask import make_response, request

from trip_planner import settings


class DB:
    def __init__(self, file=settings.DB_PATH):
        self.file = file
    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        self.conn.row_factory = sqlite3.Row
        return self.conn.cursor()
    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()


def no_cache(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        resp = make_response(f(*args, **kwargs))
        instructions = [
            "no-cache",
            "no-store",
            "must-revalidate",
            "public",
            "max-age=0",
        ]
        resp.headers['Cache-Control'] = ", ".join(instructions)
        resp.headers['Pragma'] = "no-cache"
        resp.headers['Expires'] = "0"
        return resp
    return decorated_function
