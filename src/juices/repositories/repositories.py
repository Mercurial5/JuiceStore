from juices import Juice
from juices.repositories.interfaces import IJuiceRepository
from juices.schemas import JuiceRequestCreate, JuiceRequestPriceUpdate
from juices.schemas.schemas import JuiceDTO


class JuiceRepository(IJuiceRepository):
    def __init__(self, session):
        self.session = session

    def create_juice(self, body: JuiceRequestCreate) -> JuiceDTO:
        juice = Juice(volume=body.volume, flavor=body.flavor, price=body.price)
        self.session.add(juice)
        self.session.commit()
        self.session.refresh(juice)
        return JuiceDTO.from_orm(juice)

    def read_all_juices(self, offset: int, limit: int) -> list[JuiceDTO]:
        return [JuiceDTO.from_orm(j) for j in self.session.query(Juice).offset(offset).limit(limit).all()]

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

    def count_all_juices(self) -> int:
        return self.session.query(Juice).count()
