import sqlite3
import click
from flask import g, current_app
from flask.cli import with_appcontext

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

# used to initialize the app with the database.
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

# for login
def get_user_by_id(user_id):
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    return user

def get_user_by_username(username):
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    return user

