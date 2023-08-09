import os
from pathlib import Path

from geopy import distance


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


def forget(d: dict, *keys):
    return {k: v for k, v in d.items() if k not in keys}


def calculate_distance(coords1, coords2):
    return distance.geodesic(coords1, coords2).km
