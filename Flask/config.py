from os import environ, path
# from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
#load_dotenv(path.join(basedir, '.env'))


class Config:
    """Set Flask configuration variables from .env file."""

    # General Flask Config
    # SECRET_KEY = environ.get('SECRET_KEY')
    # FLASK_ENV = environ.get('FLASK_ENV')
    FLASK_APP = 'app.py'
    FLASK_DEBUG = 1

    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, 'db.sqlite')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = basedir + '/static/images/'
    STYLE_FOLDER = basedir + '/static/styles/'