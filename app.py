from flask import *
import db

app = Flask(__name__)
# add the database to the app
db.init_app(app)

# Routes used to render a HTML file that can be edited in the templates folder.
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/index')
def index_redirect():
    return Flask.redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/buildingdirectory')
def buildingdirectory():
    return render_template(
        'buildingdirectory.html')
    
@app.route('/contribute')
def contribute():
    return render_template("contribute.html")

# Routes used to add data to the database for areas in the building.
@app.route('/add_area', methods=['POST'])
def add_area():
    type = request.form['type']
    count = request.form['count']

    db = db.get_db()
    db.execute(
        'INSERT INTO area (type, count) VALUES (?, ?)',
        (type, count)
    )
    db.commit()
    return redirect(url_for('index'))

# Routes used to get data from the database for areas in the building.
@app.route('/areas')
def areas():
    db = db.get_db()
    areas = db.execute('SELECT * FROM area').fetchall()
    return render_template('areas.html', areas=areas)

if __name__ == '__main__':
    app.run(debug=True)