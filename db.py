import sqlite3
import click
from flask import g, current_app
from flask.cli import with_appcontext
from flask import jsonify
# for admin login
import hashlib
import os

DATABASE = 'afpwnsqt.db'

# This function is used to get the database.
# It is used in the app.py file to get the database.
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            DATABASE,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

# This function is used to close the database.
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# This function is used to initialize the database.
def init_db():
    with current_app.app_context():
        db = get_db()
        with current_app.open_resource('schema.sql', mode='r') as f:
            db.executescript(f.read())

# This function is used to initialize the database.
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def get_area(area_id):
    db = get_db()
    query = "SELECT * FROM my_areas WHERE id = ?"
    area = db.execute(query, (area_id,)).fetchone()

    print("SQL Query:", query)  # print the SQL query

    if not area:
        return jsonify({"error": "Area not found"}), 404

    return jsonify({"type": area["type"], "count": area["count"]})





# for login
def get_user_by_id(user_id):
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    return user

def get_user_by_username(username):
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    return user

# Admin routes ---------------------------------------------------------------
@click.command('create-admin')
@with_appcontext
@click.option('--username', prompt='Username', help='The admin username.')
@click.option('--password', prompt='Password', help='The admin password.')
@click.option('--email', prompt='Email', help='The admin email.')
def create_admin(username, password, email):
    """Create an admin user."""
    # Hash the password
    salt = os.urandom(32)
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

    with current_app.app_context():
        db = get_db()

        # Check if the user already exists
        user = db.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()

        if user is not None:
            click.echo(f'Error: User with username {username} already exists.')
            return

        # Insert the admin user into the database
        db.execute(
            'INSERT INTO users (username, email, password, salt, is_admin) VALUES (?, ?, ?, ?, ?)',
            (username, email, hashed_password, salt, 1)
        )
        db.commit()

    click.echo(f'Admin user {username} created successfully.')


# used to initialize the app with the database.
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command, 'init-db') # This is used to initialize the database.
    app.cli.add_command(create_admin, 'create-admin') # This is used to create an admin user.


