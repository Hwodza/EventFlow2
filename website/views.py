from flask import Blueprint, render_template

views = Blueprint('views', __name__)


@views.route('/')
def landing():
    return render_template("landing.html")


@views.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


@views.route('/team')
def teams():
    return render_template("team.html")