import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

from geopy import distance


def calculate_distance(coords1, coords2, prec=2):
    value = distance.geodesic(coords1, coords2).km
    if isinstance(prec, int):
        return round(value, prec)
    return value


def forget(d: dict, *keys):
    return {k: v for k, v in d.items() if k not in keys}


def get_path(p=None):
    base = Path(os.path.abspath(os.path.dirname(__file__)))
    if p is not None:
        backwards = p.count("..")
        if backwards:
            for _ in range(backwards):
                base = getattr(base, "parent")
            return base
        return base / p
    return base


def setup_logging(app, filename="app.log"):
    file_handler = RotatingFileHandler(
        filename,
        maxBytes=1024*1024,
        backupCount=10,
    )
    file_formatter = logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s [in %(filename)s:%(lineno)d]",
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)

    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()
    stream_formatter = logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s",
    )
    stream_handler.setFormatter(stream_formatter)
    app.logger.addHandler(stream_handler)

    app.logger.info('Flask application started.')
