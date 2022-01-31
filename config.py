"""Flask configuration."""
import secrets
from os import environ, path

basedir = path.abspath(path.dirname(__file__))
SECRET_KEY = secrets.token_hex(32)
SQLALCHEMY_DATABASE_URI = 'sqlite:///./database/database.db'

class Config:
    """Set Flask configuration from .env file."""

    # General Config
    SECRET_KEY = SECRET_KEY
    FLASK_APP = environ.get("FLASK_APP")
    FLASK_ENV = environ.get("FLASK_ENV")
    STATIC_FOLDER = 'app/static'
    TEMPLATES_FOLDER = 'app/templates'
    UPLOAD_PATH = 'uploads'

    # Database
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


