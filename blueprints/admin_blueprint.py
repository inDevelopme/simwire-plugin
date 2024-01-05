from flask import render_template, url_for
from flask_login import LoginManager, login_required, current_user, logout_user, login_user
from . import admin_bp


@admin_bp.route('/admin')
@login_required
def admin_landing_page():
    return render_template('administration.html')
