import os

from flask import current_app
from dotenv import load_dotenv

# todo: in .env see all properties marked as todo ! setup a seperate readme for their strategy
load_dotenv()
# todo: set in a venv to isolate needed libraries, to be frozen in a requirements.txt

class DatabaseConfig:
    HOST = os.environ.get("DB_HOST")        # todo: Change for prd
    USER = os.environ.get("DB_USER")        # todo: Change for prd
    PASSWORD = os.environ.get("DB_PASSWORD")    # todo: os.env
    DATABASE_NAME = "whatsapp_db"
    PORT = 3306
    POOL_SIZE = 30
    CONNECTION_TIMEOUT = 10

class DevelopmentDatabaseConfig(DatabaseConfig):
    HOST = os.environ.get("DB_HOST_DEV")
    USER = os.environ.get("DB_USER_DEV")
    PASSWORD = os.environ.get("DB_PASSWORD_DEV")


class Config:

    DATABASE = DatabaseConfig()

    # todo: Can be refactored to be included in a sep META config object
    META_VERIFY_TOKEN = os.environ.get("META_VERIFY_TOKEN")
    META_MESSAGE_URL = os.environ.get("META_MESSAGE_URL")
    META_ACCESS_TOKEN = os.environ.get("META_ACCESS_TOKEN")

    GRACE_PERIOD = os.environ.get("GRACE_PERIOD")


# todo: Complete me with development properties, do the same for Meta config
class DevelopmentConfig(Config):
    DATABASE = DevelopmentDatabaseConfig()


def get_mysql_config() -> dict:

    db_config: DatabaseConfig = current_app.config['DATABASE']

    return {
        "host": db_config.HOST,
        "user": db_config.USER,
        "password": db_config.PASSWORD,  # todo: remove from here
        "database": db_config.DATABASE_NAME,
        "port": db_config.PORT,  # todo: get and set default
        "charset": "utf8mb4",     # todo: this is defined as a const in db, to include
        "pool_name": "app_pool",
        "pool_size": db_config.POOL_SIZE,
        "autocommit": True,
        "collation": "utf8mb4_unicode_ci",
        "connection_timeout": db_config.CONNECTION_TIMEOUT
        # todo : Add a catch statement on top level, so that when an error occurs, redirects the lead to state unexpected
    }
