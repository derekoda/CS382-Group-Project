from flask import *
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_login import current_user
import click
import db
from db import get_db
# for admin login
import hashlib
import os





app = Flask(__name__)
# add the database to the app
db.init_app(app)
app.secret_key = 'super_secret_key' # used to encrypt the session cookie

# Routes used to render a HTML file that can be edited in the templates folder.
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/index')
def index_redirect():
    return redirect(url_for('index'))

@app.route('/findarea', methods=['GET','POST'])
def findarea():
    return render_template("findarea.html")

@app.route('/areas', methods=['GET','POST'])
def find_area():
    
    if request.method == 'POST':
        global attribute1
        global attribute2
        global vending
        
        # stores form data in variables
        attribute1 = request.form['attribute']
        attribute2 = request.form['attribute2']
        vending = request.form['vending']

    db = get_db()

    if(attribute2 != ''):
        areas = db.execute(
        "SELECT * FROM area WHERE (type = ? OR type = ?)",
        (attribute1,attribute2)
        ).fetchall()
    else:
        areas = db.execute(
        "SELECT * FROM area WHERE type = ?",
        (attribute1,)
        ).fetchall()
    return render_template('areas.html', areas=areas)

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/buildingdirectory')
def buildingdirectory():
    db = get_db()
    areas = db.execute("SELECT * FROM area ").fetchall()
    return render_template('buildingdirectory.html', areas=areas)
    
@app.route('/contribute')
#@login_required # this route requires the user to be logged in
def contribute():
    return render_template("contribute.html")


# Database routes -------------------------------------------------------------
# Routes used to add data to the database for areas in the building.
@app.route('/add_area', methods=['POST'])
@login_required # this route requires the user to be logged in
def add_area():
    type = request.form['type']
    count = request.form['count']
    location = request.form['location']

    location = location.split(",")
    latitude = float(location[0][1:])
    longitude = float(location[1][:-1])

    db = get_db()
    db.execute(
        'INSERT INTO area (type, count, lat, lng) VALUES (?, ?, ?, ?)',
        (type, count, latitude, longitude)
    )
    db.commit()
    return redirect(url_for('index'))

# Routes used to get data from the database for areas in the building.
@app.route('/areas')
def areas():
    db = get_db()
    areas = db.execute('SELECT * FROM area').fetchall()
    return render_template('areas.html', areas=areas)

# Login section ---------------------------------------------------------------
# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        self.is_authenticated
        self.is_active
        self.is_anonymous
    def get_id(self):
        return self.id

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    user_data = db.get_user_by_id(user_id)
    if user_data:
        return User(user_data['id'], user_data['username'], user_data['password'])
    return None
# Login routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        next = request.args.get('next')
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        else:
            stored_password, stored_salt = user['password'], user['salt']
            hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), stored_salt, 100000)

            if stored_password != hashed_password:
                error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            login_user(load_user(session['user_id']))
            if next is None:
                return redirect(url_for('index'))
            else:
                return redirect(url_for('contribute'))

        flash(error)

    return render_template('login.html')


# logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
  
