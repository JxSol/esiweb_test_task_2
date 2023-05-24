import os
from dotenv import load_dotenv
from flask_migrate import Migrate

from apps import create_app, db
from config import config_list

# Load variables from .env
load_dotenv()

# Get configurations
config_mode = os.getenv('FLASK_ENV')
try:
    app_config = config_list[config_mode]
except KeyError:
    exit(f"Error: Invalid <config_mode>."
         f"Expected values: {', '.join(config_list.keys)}.")

# Creating app
app = create_app(app_config)

# Make migrations
Migrate(app, db)

# Logging
if app.config.get('DEBUG'):
    app.logger.info('DEBUG = ' + str(app.config.get('DEBUG')))
    app.logger.info('DBMS = ' + app_config.SQLALCHEMY_DATABASE_URI)
    app.logger.info('STATIC_ROOT = ' + app_config.STATIC_ROOT)

# Running app
if __name__ == '__main__':
    app.run(host='0.0.0.0')
