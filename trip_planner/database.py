import sqlite3


def setup_database():
    conn = sqlite3.connect('trip_planner.db')
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS places(id INTEGER PRIMARY KEY, name TEXT, location TEXT, latitude REAL, longitude REAL)",
    )
    conn.commit()
    conn.close()


def add_place(name, location, lat, lon):
    conn = sqlite3.connect('trip_planner.db')
    c = conn.cursor()
    c.execute(
        "INSERT INTO places (name, location, latitude, longitude) VALUES (?, ?, ?, ?)",
        (name, location, lat, lon),
    )
    conn.commit()
    conn.close()


def update_place(_id, name=None, location=None, lat=None, lon=None):
    conn = sqlite3.connect('trip_planner.db')
    c = conn.cursor()

    # Find the current data first
    c.execute("SELECT name, location, latitude, longitude FROM places WHERE id=?", (_id,))
    result = c.fetchone()
    if not result:
        print("ID not found.")
        return

    # If no new data is provided, keep the old
    name = name or result[0]
    location = location or result[1]
    lat = lat or result[2]
    lon = lon or result[3]

    c.execute("UPDATE places SET name=?, location=?, latitude=?, longitude=? WHERE id=?",
              (name, location, lat, lon, _id))
    conn.commit()
    conn.close()


def list_places():
    conn = sqlite3.connect('trip_planner.db')
    c = conn.cursor()
    c.execute("SELECT id, name, location, latitude, longitude FROM places")
    places = c.fetchall()
    conn.close()
    return places
