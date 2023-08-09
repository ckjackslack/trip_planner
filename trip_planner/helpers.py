import sqlite3
from collections import namedtuple

from trip_planner import settings


class DB:
    def __init__(self, file=settings.DB_FILE):
        self.file = file
    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        self.conn.row_factory = sqlite3.Row
        return self.conn.cursor()
    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()
