import os
from importlib import import_module
from typing import NoReturn

from flask import Flask

from config import Config
from .db import db


def configure_database(app: Flask) -> NoReturn:
    """Configure database."""
    db.init_app(app)

    @app.before_request
    def initialize_database():
        try:
            db.create_all()
        except Exception as e:
            print('DBMS ERROR: ' + str(e))
            print('Fallback to SQLite.')
            # Fallback to SQLite
            app.config['SQLALCHEMY_DATABASE_URI'] = \
                'sqlite:///' \
                + os.path.join(app.config['BASEDIR'], 'db.sqlite3')
            db.create_all()


def register_blueprints(app: Flask) -> NoReturn:
    """Register blueprints from apps."""
    for module_name in app.config['INSTALLED_APPS']:
        # Import every single module
        module = import_module(f'apps.{module_name}.routes')
        # Register a blueprint from the module
        app.register_blueprint(module.blueprint)


def create_app(config: Config) -> Flask:
    """The Application Factory."""
    app = Flask(__name__)
    app.config.from_object(config)
    configure_database(app)
    register_blueprints(app)
    return app
