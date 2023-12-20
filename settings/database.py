class Config(object):
    DEBUG = True
    TESTING = False
    SESSION_TYPE = 'sqlalchemy'
    SQLALCHEMY_ECHO = True
    PERMANENT_SESSION_LIFETIME = 86400
    MYSQL_CONFIGURATION = {
        'connection_type': '',
        'username': '',
        'password': '',
        'hostname': '',
        'database': ''
    }
    SQLALCHEMY_DATABASE_URI = ''
    SECRET_KEY = 'p9Bv<3Eid9%$i01'



