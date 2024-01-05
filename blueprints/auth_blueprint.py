from flask import render_template, url_for, redirect
from flask_login import LoginManager, login_required, current_user, logout_user, login_user
from flask import Flask, render_template, jsonify, request, flash, url_for, redirect
from pathlib import Path

from . import auth_bp
from models import User

# renders the manual login page
@auth_bp.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@auth_bp.route('/login', methods=['POST'])
def login_validate():
    username = request.form['username']
    user = User.query.filter_by(username=username).first()
    if user: #  and check_password_hash(user.password_hash, password):
        # If authentication is successful, log the user in
        login_user(user)
        flash('Logged in successfully!', 'success')
        return redirect(url_for('home.landing_page'))

    flash('Login failed. Please check your credentials and try again.', 'danger')
    return redirect(url_for('home.login'))


@auth_bp.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return render_template('logout.html')

