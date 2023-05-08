import sqlite3

# List of area dictionaries from floor.html
areas = [
    {"id": "near_exit", "type": "Near Exit", "count": 0, "description": "Near the exit", "lat": 37.7749, "lng": -122.4194, "coords": "714,72,791,128"},
    {"id": "snack", "type": "Snack Area", "count": 0, "description": "Snack area", "lat": 37.7749, "lng": -122.4194, "coords": "607,112,663,151"},
    {"id": "soda", "type": "Soda Area", "count": 0, "description": "Soda area", "lat": 37.7749, "lng": -122.4194, "coords": "620,153,659,174"},
    {"id": "energy", "type": "Energy Drink Area", "count": 0, "description": "Energy drink area", "lat": 37.7749, "lng": -122.4194, "coords": "618,177,658,201"},
    {"id": "entrance", "type": "Entrance", "count": 0, "description": "Entrance", "lat": 37.7749, "lng": -122.4194, "coords": "211,153,275,203"},
    {"id": "checkout", "type": "Checkout Area", "count": 0, "description": "Checkout area", "lat": 37.7749, "lng": -122.4194, "coords": "112,230,196,320"},
    {"id": "single_study", "type": "Single Study Area", "count": 0, "description": "Single study area", "lat": 37.7749, "lng": -122.4194, "coords": "466,261,526,317"},
    {"id": "group_study", "type": "Group Study Area", "count": 0, "description": "Group study area", "lat": 37.7749, "lng": -122.4194, "coords": "964,576,1125,731"},
    {"id": "exit", "type": "Exit", "count": 0, "description": "Exit", "lat": 37.7749, "lng": -122.4194, "coords": "1609,874,1689,951"},
    {"id": "snackbar", "type": "Snackbar", "count": 0, "description": "Snackbar", "lat": 37.7749, "lng": -122.4194, "coords": "588,787,882,945"},
]

# Connect to the SQLite database
# Connect to the SQLite database
conn = sqlite3.connect("afpwnsqt.db")
db = conn.cursor()

# Insert each area from the floor.html file into the database
for area in areas:
    db.execute(
        "INSERT INTO my_areas (type, count, description, lat, lng, coords) VALUES (?, ?, ?, ?, ?, ?)",
        (area["type"], area["count"], area["description"], area["lat"], area["lng"], area["coords"]),
    )

# Commit the changes and close the connection
conn.commit()
conn.close()
