from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Juice(Base):
    __tablename__ = 'juices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    volume = Column(Float, nullable=False)
    flavor = Column(String, nullable=False)
    price = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Juice(id={self.id}, flavor={self.flavor}, volume={self.volume}, price={self.price})>"
