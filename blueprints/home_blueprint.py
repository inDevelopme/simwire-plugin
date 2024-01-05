from flask import render_template, url_for
from flask_login import LoginManager, login_required, current_user, logout_user, login_user

from pathlib import Path
from . import home_bp


# load the views
@home_bp.route('/homepage')
@login_required
def landing_page():
    return f"Welcome, {current_user.id}! This is a protected page." + str(url_for('home.landing_page'))


@home_bp.route('/')
def index():
    return "this is the index page"
