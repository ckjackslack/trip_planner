CREATE_STMT = """
CREATE TABLE IF NOT EXISTS place(
    id INTEGER PRIMARY KEY,
    name TEXT,
    location TEXT,
    latitude REAL,
    longitude REAL
)""".strip()

INSERT_STMT = """
INSERT INTO place (name, location, latitude, longitude)
VALUES (?, ?, ?, ?)
""".strip()

SELECT_SINGLE_STMT = """
SELECT id, name, location, latitude, longitude
FROM place
WHERE id=?
""".strip()

SELECT_ALL_STMT = """
SELECT id, name, location, latitude, longitude
FROM place
""".strip()

UPDATE_STMT = """
UPDATE place
SET name=?, location=?, latitude=?, longitude=?
WHERE id=?
""".strip()

DELETE_ALL_STMT = """
DELETE FROM place
""".strip()