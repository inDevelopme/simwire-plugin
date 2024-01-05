from flask import render_template, url_for
from flask_login import LoginManager, login_required, current_user, logout_user, login_user

from pathlib import Path
from . import home_bp


@home_bp.route('/')
def index():
    return "this is the index page"
