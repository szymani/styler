from os import environ, path

basedir = path.abspath(path.dirname(__file__))


class Config:
    """Set Flask configuration variables from .env file."""

    # General Flask Config
    if environ.get('SECRET_KEY') is not None:
        SECRET_KEY = environ.get('SECRET_KEY')
    else:       #if there is problem loading env
        SECRET_KEY = "Loading_.env_needs_fixing"
    # FLASK_ENV = environ.get('FLASK_ENV')
    FLASK_APP = 'app.py'
    FLASK_DEBUG = 1

    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, 'db.sqlite')
    #SQLALCHEMY_DATABASE_URI = 'mysql://' + 'username' + ':' + 'password' + '@' + 'sql7.freesqldatabase.com:3306/sql7344809'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig:
    """Set Flask configuration variables from .env file."""

    # General Flask Config
    if environ.get('SECRET_KEY') is not None:
        SECRET_KEY = environ.get('SECRET_KEY')
    else:       #if there is problem loading env
        SECRET_KEY = "Loading_.env_needs_fixing"
    # FLASK_ENV = environ.get('FLASK_ENV')
    FLASK_APP = 'app.py'
    FLASK_DEBUG = 1
    TESTING = True
    
    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, 'test_db.sqlite')
    SQLALCHEMY_DATABASE_TEST_PATH = path.join(basedir, 'test_db.sqlite')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = basedir + '/static/images/'
    STYLE_FOLDER = basedir + '/static/styles/'