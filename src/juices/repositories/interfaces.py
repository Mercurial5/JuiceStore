from abc import ABC, abstractmethod
from typing import List

from juices.schemas.schemas import JuiceDTO, JuiceRequestPriceUpdate, JuiceRequestCreate


class IJuiceRepository(ABC):

    @abstractmethod
    def read_all_juices(self, offset: int, limit: int) -> List[JuiceDTO]:
        pass

    @abstractmethod
    def create_juice(self, juice: JuiceRequestCreate) -> JuiceDTO:
        pass

    @abstractmethod
    def delete_juice(self, juice_id: int) -> bool:
        pass

    @abstractmethod
    def update_juice_price(self, juice_id: int, body: JuiceRequestPriceUpdate):
        pass

    @abstractmethod
    def count_all_juices(self) -> int:
        pass
