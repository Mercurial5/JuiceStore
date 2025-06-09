import os

from dotenv import load_dotenv

from database.database import Database
from database.settings import DatabaseSettings
from juices.models import Juice


def get_database():
    load_dotenv()

    db_settings = DatabaseSettings(
        host=os.getenv("JUICE_DB_HOST"),
        port=int(os.getenv("JUICE_DB_PORT")),
        username=os.getenv("JUICE_DB_USERNAME"),
        password=os.getenv("JUICE_DB_PASSWORD"),
        database=os.getenv("JUICE_DB_NAME"),
    )
    return Database(db_settings)


db = get_database()


def get_db_session():
    return db.session
