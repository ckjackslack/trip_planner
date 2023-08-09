import os
from pathlib import Path


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