from flask import jsonify

from src.juices.repository.repository import JuiceRepository
from src.juices.shemas import JuiceRequestCreate, JuiceRequestPriceUpdate
from src.juices.shemas.juice import JuiceResponse


class JuiceService:
    def __init__(self, repository: JuiceRepository = None):
        self.repository = repository or JuiceRepository()

    def add_juice(self, body: JuiceRequestCreate):
        self.repository.create_juice(body)
        # ...

    def get_all_juices(self):
        juices = self.repository.read_all_juices()
        # ...
        return [JuiceResponse.from_orm(j).dict() for j in juices]

    def change_juice_price(self, juice_id: int, body: JuiceRequestPriceUpdate):
        self.repository.update_juice_price(juice_id, body)
        # ...

    def delete_juice(self, juice_id: int):
        self.repository.delete_juice(juice_id)
        # ...
