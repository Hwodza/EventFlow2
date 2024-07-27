from flask import Flask
from flask_mysqldb import MySQL
from flask import Blueprint, render_template
from . import db


views = Blueprint('views', __name__)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'flaskapp'
    db = MySQL(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app



@app.route('/')
def landing():
    return render_template("landing.html")


@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


@app.route('/team')
def teams():
    return render_template("team.html")