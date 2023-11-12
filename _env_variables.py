# default configurations
class Config(object):
    DEBUG = True
    TESTING = False
    SESSION_TYPE = 'sqlalchemy'
    SQLALCHEMY_ECHO = True
    PERMANENT_SESSION_LIFETIME = 7200
    MYSQL_CONFIGURATION = {
        'connection_type': 'mysql',
        'username': 'root',
        'password': 'helloworld',
        'hostname': 'mysql',
        'database': 'simportal'
    }

    SQLALCHEMY_DATABASE_URI = \
        MYSQL_CONFIGURATION['connection_type'] + '://'+ \
        MYSQL_CONFIGURATION['username'] + ':' + \
        MYSQL_CONFIGURATION['password'] + '@' + \
        MYSQL_CONFIGURATION['hostname'] + '/' + \
        MYSQL_CONFIGURATION['database']