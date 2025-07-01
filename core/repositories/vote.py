from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date
from ..entities.vote import Vote, RestaurantVoteStats


class VoteRepository(ABC):
    @abstractmethod
    def get_user_votes_for_date(self, user_id: int, target_date: date) -> List[Vote]:
        pass

    @abstractmethod
    def get_restaurant_votes_for_date(self, restaurant_id: int, target_date: date) -> List[Vote]:
        pass

    @abstractmethod
    def save(self, vote: Vote) -> Vote:
        pass

    @abstractmethod
    def user_has_voted_for_restaurant(self, user_id: int, restaurant_id: int, target_date: date) -> bool:
        pass

    @abstractmethod
    def get_all_votes_for_date(self, target_date: date) -> List[Vote]:
        pass

    @abstractmethod
    def get_votes_of_restaurants_for_date(self, target_date: date) -> List[RestaurantVoteStats]:
        pass

    @abstractmethod
    def get_user_votes_for_restaurant_for_date(self, user_id: int, restaurant_id: int, target_date: date) -> List[Vote]:
        pass