from env_load import Config
from flask_cors import CORS
from pathlib import Path
from flask import Flask, render_template, jsonify, request, flash, url_for, redirect
from flask_login import LoginManager, login_required, current_user, logout_user, login_user
from models import db, User

app = Flask(__name__)
CORS(app)
config = Config()
config.get_environment_config()
config.set_server_side_session(db)

# sqlalchemy needs to know the database configuration
app.config.from_object(config)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# initialize sqlalchemy
db.init_app(app)

with app.app_context():
    db.create_all()


# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    # Replace this with your logic for loading users from a database
    return User.query.get(int(user_id))


# load the views
@app.route('/homepage')
@login_required
def landing_page():
    return f"Welcome, {current_user.id}! This is a protected page." + str(url_for('landing_page'))


@app.route('/')
def index():
    return "this is the index page"


@app.route('/admin')
@login_required
def admin_landing_page():
    return render_template('administration.html')


# renders the manual login page
@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_validate():
    username = request.form['username']
    user = User.query.filter_by(username=username).first()
    if user: #  and check_password_hash(user.password_hash, password):
        # If authentication is successful, log the user in
        login_user(user)
        flash('Logged in successfully!', 'success')
        return redirect(url_for('landing_page'))

    flash('Login failed. Please check your credentials and try again.', 'danger')
    return redirect(url_for('login'))


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return render_template('logout.html')


@app.before_request
def exclude_health_check_routes():
    if request.path.startswith('/health_check'):
        try:
            return jsonify(status='ok')
        except Exception as e:
            # Handle any exceptions that may occur during the health check
            return jsonify(status='error', message=str(e)), 500  # Return a 500 Internal Server Error on failure


@app.route('/health_check')
def health_check():
    # Minimal health check logic here (e.g., check database connection)
    try:
        # Perform a minimal check (e.g., check the database connection)
        # If using SQLAlchemy, roll back any uncommitted transactions to avoid session creation
        return jsonify(status='ok')
    except Exception as e:
        # Handle any exceptions that may occur during the health check
        return jsonify(status='error', message=str(e)), 500  # Return a 500 Internal Server Error on failure


def get_extra_files():
    for bp in (app.blueprints or {}).values():
        macros_dir = Path(bp.root_path)
        for filepath in macros_dir.rglob('*.html'):
            yield str(filepath)


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run(extra_files=list(get_extra_files()))