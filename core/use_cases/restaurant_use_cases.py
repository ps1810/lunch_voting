from typing import List, Optional
from datetime import date
from ..entities.restaurant import Restaurant
from ..repositories.restaurant import RestaurantRepository


class RestaurantUseCases:
    def __init__(self, restaurant_repository: RestaurantRepository):
        self.restaurant_repository = restaurant_repository

    def create_restaurant(self, id: Optional[int], name: str, address: str, phone: str, cuisine_type: str, is_votable: bool) -> Restaurant:
        restaurant = Restaurant(
            id=id,
            name=name,
            address=address,
            phone=phone,
            cuisine_type=cuisine_type,
            is_votable=is_votable
        )
        return self.restaurant_repository.save(restaurant)

    def get_restaurant(self, restaurant_id: int) -> Optional[Restaurant]:
        return self.restaurant_repository.get_by_id(restaurant_id)

    def get_all_restaurants(self) -> List[Restaurant]:
        return self.restaurant_repository.get_all()

    def search_restaurants(self, query: str) -> List[Restaurant]:
        return self.restaurant_repository.search(query)

    def delete_restaurant(self, restaurant_id: int) -> bool:
        return self.restaurant_repository.delete(restaurant_id)

    def get_voteable_restaurants(self) -> List[Restaurant]:
        """Get restaurants the user can still vote for today"""
        return self.restaurant_repository.get_votable_restaurants()