from pydantic import BaseModel


class DatabaseSettings(BaseModel):
    host: str
    port: int
    username: str
    password: str
    database: str

    @property
    def url(self):
        return f'postgresql+psycopg2://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}'
