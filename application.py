# implemented to get operation system information
import os
from pathlib import Path
from flask import Flask
from flask_session import Session
from dotenv import load_dotenv
from os.path import join, dirname
from settings.database import Config

# it is critical that instance variables stay in a segment of code
# that never needs to change such as the current instance's environment name

# load the business access object for communicating with the database
from simcore.salchemy.bao import SalchemyBAO
from flask import render_template
from flask_cors import CORS

app = application = Flask(__name__)
CORS(app)

# setup reader for environment file
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# load environment variables
# if environment is not defined / locl

# todo: For now we will use a try block to prevent EC2 instance in EB from going down
# We want to make it so that this application checks deployed, local, none existing
# It should not attempt a database connection without any environmental variables
try:
    ENV_NAME = os.environ.get("ENV_NAME")
    if (ENV_NAME is None) or (ENV_NAME == "local"):
        MYSQL_USER = os.environ.get("MYSQL_USER")
        MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
        MYSQL_DB = os.environ.get("MYSQL_DB")
        MYSQL_HOST = os.environ.get("MYSQL_HOST")
        MYSQL_CONNECTOR = os.environ.get("MYSQL_CONNECTOR")
        Config.SQLALCHEMY_DATABASE_URI = \
            MYSQL_CONNECTOR + '://' + MYSQL_USER + ':' + MYSQL_PASSWORD + '@' + MYSQL_HOST + '/' + MYSQL_DB

    app.config.from_object(Config)
    # sqlalchemy needs to know the database configuration
    db_bao = SalchemyBAO(Config.MYSQL_CONFIGURATION)

    # Session.sid is not possible without this
    session = Session(app)
    with app.app_context():
        session.app.session_interface.db.create_all()
except TypeError as e:
    # This will happen when the environment variables are not strings
    print(e)

except Exception as e:
    # This will happen particularly when a database connection is not possible
    print(e)
except Exception as e:
    print(e)


# load the views
@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/admin')
def admin_landing_page():
    return render_template('administration.html')


# renders the manual login page
@app.route('/login', methods=['GET', 'POST'])
def user_login():
    return render_template('login.html')


@app.route('/logout', methods=['GET'])
def user_logout():
    return render_template('logout.html')


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
