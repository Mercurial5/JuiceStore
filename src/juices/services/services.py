from juices.repositories.interfaces import IJuiceRepository
from juices.schemas import JuiceRequestCreate, JuiceRequestPriceUpdate, JuiceResponse
from juices.services.interfaces import IJuiceService


class JuiceService(IJuiceService):
    def __init__(self, repository: IJuiceRepository):
        self.repository: IJuiceRepository = repository

    def add_juice(self, body: JuiceRequestCreate):
        self.repository.create_juice(body)

    def get_all_juices(self, page: int, limit: int):
        juices = self.repository.read_all_juices((page - 1) * limit, limit)
        total = self.repository.count_all_juices()
        return {
            "items": [JuiceResponse.from_orm(j).dict() for j in juices],
            "page": page,
            "limit": limit,
            "total": total
        }

    def change_juice_price(self, juice_id: int, body: JuiceRequestPriceUpdate):
        self.repository.update_juice_price(juice_id, body)

    def delete_juice(self, juice_id: int):
        self.repository.delete_juice(juice_id)
