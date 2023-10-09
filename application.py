from flask import Flask
from pathlib import Path
from flask import render_template
from flask_cors import CORS
app = application = Flask(__name__)
CORS(app)


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
