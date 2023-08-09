CREATE_STMT = """
CREATE TABLE IF NOT EXISTS places(
    id INTEGER PRIMARY KEY,
    name TEXT,
    location TEXT,
    latitude REAL,
    longitude REAL
)""".strip()

INSERT_STMT = """
INSERT INTO places (name, location, latitude, longitude)
VALUES (?, ?, ?, ?)
""".strip()

SELECT_SINGLE_STMT = """
SELECT id, name, location, latitude, longitude
FROM places
WHERE id=?
""".strip()

SELECT_ALL_STMT = """
SELECT id, name, location, latitude, longitude
FROM places
""".strip()

UPDATE_STMT = """
UPDATE places
SET name=?, location=?, latitude=?, longitude=?
WHERE id=?
""".strip()