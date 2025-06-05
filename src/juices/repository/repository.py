from sqlalchemy import select, insert, update, delete

from src.juices import get_db_session, Juice
from src.juices.shemas import JuiceRequestCreate, JuiceRequestPriceUpdate


class JuiceRepository:
    def __init__(self, session=None):
        self.session = session or get_db_session()

    def create_juice(self, body: JuiceRequestCreate):
        juice = Juice(volume=body.volume, flavor=body.flavor, price=body.price)
        self.session.add(juice)
        self.session.commit()
        self.session.refresh(juice)  # refresh to get the id after insert
        return juice

    def read_all_juices(self):
        return self.session.query(Juice).all()

    def update_juice_price(self, juice_id: int, body: JuiceRequestPriceUpdate):
        juice = self.session.query(Juice).filter(Juice.id == juice_id).first()
        if not juice:
            raise ValueError(f"Juice with id {juice_id} not found")
        juice.price = body.price
        self.session.commit()

    def delete_juice(self, juice_id: int):
        juice = self.session.query(Juice).filter(Juice.id == juice_id).first()
        if not juice:
            raise ValueError(f"Juice with id {juice_id} not found")
        self.session.delete(juice)
        self.session.commit()
