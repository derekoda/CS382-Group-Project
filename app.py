from flask import *

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)