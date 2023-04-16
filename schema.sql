CREATE TABLE area (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL CHECK (type IN ('computer', 'single_study', 'group_study', 'outlet', 'whiteboard', 'printer', 'quiet', 'loud', 'large_desk', 'small_desk', 'medium_desk', 'padded_chair', 'non_padded_chair', 'window', 'no_window', 'near_exit')),
    count INTEGER NOT NULL,
    date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE area_comment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    area_id INTEGER NOT NULL,
    body TEXT,
    date TIMESTAMP,
    FOREIGN KEY (area_id) REFERENCES area (id) ON DELETE CASCADE
);

CREATE TABLE area_meta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    area_id INTEGER NOT NULL,
    votes INTEGER,
    favs INTEGER,
    FOREIGN KEY (area_id) REFERENCES area (id) ON DELETE CASCADE
);

CREATE TABLE machine (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL CHECK (type IN ('soda', 'snack', 'energy_drink')),
    count INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE floor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    floorNumber INTEGER NOT NULL,
    bathrooms INTEGER DEFAULT 0
);

CREATE TABLE floor_area (
    floor_id INTEGER NOT NULL,
    area_id INTEGER NOT NULL,
    FOREIGN KEY (floor_id) REFERENCES floor (id) ON DELETE CASCADE,
    FOREIGN KEY (area_id) REFERENCES area (id) ON DELETE CASCADE
);

CREATE TABLE floor_machine (
    floor_id INTEGER NOT NULL,
    machine_id INTEGER NOT NULL,
    FOREIGN KEY (floor_id) REFERENCES floor (id) ON DELETE CASCADE,
    FOREIGN KEY (machine_id) REFERENCES machine (id) ON DELETE CASCADE
);
/* 
    For users to make an account, they must have a username and password.
*/
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
