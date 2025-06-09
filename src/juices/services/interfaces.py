from abc import ABC, abstractmethod
from typing import Dict

from juices.schemas import JuiceRequestCreate, JuiceRequestPriceUpdate


class IJuiceService(ABC):

    @abstractmethod
    def add_juice(self, body: JuiceRequestCreate) -> None:
        pass

    @abstractmethod
    def get_all_juices(self, page: int, limit: int) -> Dict:
        """
        Returns a dict with keys: items (list), page (int), limit (int), total (int)
        """
        pass

    @abstractmethod
    def change_juice_price(self, juice_id: int, body: JuiceRequestPriceUpdate) -> None:
        pass

    @abstractmethod
    def delete_juice(self, juice_id: int) -> None:
        pass
