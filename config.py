import os
import psycopg2
from dotenv import load_dotenv

import random
import string

# Load variables from .env
load_dotenv()


class Config:
    """Basic configuration class."""
    # Absolute filesystem path to the Flask project directory
    BASEDIR = os.path.abspath(os.path.dirname(__file__))

    # Relative filesystem path to the static directory
    STATIC_ROOT = os.getenv('STATIC_ROOT', '/static')

    # Cross-Site Request Forgery
    CSRF_ENABLED = True

    # Set up the App SECRET_KEY
    SECRET_KEY = os.getenv('SECRET_KEY', None)
    if not SECRET_KEY:
        SECRET_KEY = ''.join(
            random.choice(string.ascii_lowercase) for i in range(32))

    # SQLAlchemy and database configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DB_ENGINE = os.getenv('DB_ENGINE', None)
    DB_USER = os.getenv('DB_USER', None)
    DB_PASSWORD = os.getenv('DB_PASSWORD', None)
    DB_HOST = os.getenv('DB_HOST', None)
    DB_PORT = os.getenv('DB_PORT', None)
    DB_NAME = os.getenv('DB_NAME', None)

    USE_SQLITE = True

    if DB_ENGINE and DB_NAME and DB_USER:
        try:
            SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".format(
                DB_ENGINE,
                DB_USER,
                DB_PASSWORD,
                DB_HOST,
                DB_PORT,
                DB_NAME,
            )
            # Connection check
            conn = psycopg2.connect(SQLALCHEMY_DATABASE_URI)
            conn.close()
            USE_SQLITE = False
        except Exception as e:
            print('DBMS ERROR:', e)
            print('Fallback to SQLite.')

    if USE_SQLITE:
        SQLALCHEMY_DATABASE_URI = "sqlite:///" \
                                  + os.path.join(BASEDIR, 'db.sqlite3')

    # List of installed custom applications
    INSTALLED_APPS = [
        'users',
    ]


class DevelopmentConfig(Config):
    """Configuration for development."""
    DEBUG = True


class TestingConfig(Config):
    """Configuration for testing."""
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    """Configuration for production."""
    DEBUG = False


# All possible configurations
config_list = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'test': TestingConfig,
}
