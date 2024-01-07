from env_load import Config
from flask_cors import CORS
from pathlib import Path
from flask import Flask, jsonify, request
from flask_login import LoginManager
from blueprints import home_bp, auth_bp, admin_bp
from models import db, User


application = app = Flask(__name__)
CORS(app)


def get_extra_files():
    for bp in (app.blueprints or {}).values():
        macros_dir = Path(bp.root_path)
        for filepath in macros_dir.rglob('*.html'):
            yield str(filepath)


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


@app.before_request
def exclude_health_check_routes():
    if request.path.startswith('/health_check'):
        try:
            return jsonify(status='ok')
        except (TypeError, ValueError) as e:
            # Handle any exceptions that may occur during the health check
            return jsonify(status='error', message='error'), 500  # Return a 500 Internal Server Error on failure


@app.route('/health_check')
def health_check():
    # Minimal health check logic here (e.g., check database connection)
    try:
        # Perform a minimal check (e.g., check the database connection)
        # If using SQLAlchemy, roll back any uncommitted transactions to avoid session creation
        return jsonify(status='ok')
    except (TypeError, ValueError) as e:
        # Handle any exceptions that may occur during the health check
        return jsonify(status='error', message='error'), 500  # Return a 500 Internal Server Error on failure


app.register_blueprint(home_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run(extra_files=list(get_extra_files()))