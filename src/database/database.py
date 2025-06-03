from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from database.settings import DatabaseSettings


class Database:
    def __init__(self, settings: DatabaseSettings):
        engine = create_engine(settings.url, echo=True, pool_pre_ping=True)
        self._session_maker = sessionmaker(bind=engine)

    @property
    def session(self) -> Session:
        return self._session_maker()
