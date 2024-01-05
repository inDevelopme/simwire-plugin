from flask import Blueprint

home_bp = Blueprint('home', __name__)
admin_bp = Blueprint('admin', __name__)
auth_bp = Blueprint('auth', __name__)
from .home_blueprint import *
from .auth_blueprint import *
from .admin_blueprint import *
