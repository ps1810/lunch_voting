from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date
from ..entities.restaurant import Restaurant


class RestaurantRepository(ABC):
    @abstractmethod
    def get_by_id(self, restaurant_id: int) -> Optional[Restaurant]:
        pass

    @abstractmethod
    def get_all(self) -> List[Restaurant]:
        pass

    @abstractmethod
    def save(self, restaurant: Restaurant) -> Restaurant:
        pass

    @abstractmethod
    def delete(self, restaurant_id: int) -> bool:
        pass

    @abstractmethod
    def search(self, query: str) -> List[Restaurant]:
        pass

    @abstractmethod
    def get_votable_restaurants(self) -> List[Restaurant]:
        pass