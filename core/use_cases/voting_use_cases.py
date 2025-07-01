from typing import List, Optional, Tuple
from datetime import date
from django.conf import settings
from ..entities.vote import Vote
from ..entities.restaurant import Restaurant
from ..repositories.vote import VoteRepository
from ..repositories.restaurant import RestaurantRepository
from ..services.voting import VotingService
import logging

logger = logging.getLogger(__name__)


class VotingUseCases:
    def __init__(self, vote_repository: VoteRepository, restaurant_repository: RestaurantRepository):
        self.vote_repository = vote_repository
        self.restaurant_repository = restaurant_repository
        self.voting_service = VotingService(vote_repository)

    def create_vote(self, restaurant_id: int, user_id: int, vote_date: date) -> Tuple[Optional[Vote], str]:
        # Validate restaurant exists
        restaurant = self.restaurant_repository.get_by_id(restaurant_id)
        if not restaurant:
            logger.error(f"Restaurant with ID {restaurant_id} not found for user {user_id} on {vote_date}")
            return None, "Restaurant not found"

        # Check if user can vote
        max_votes = getattr(settings, 'VOTES_PER_USER_PER_DAY', 5)
        can_vote, error_msg = self.voting_service.can_user_vote(
            user_id, vote_date, max_votes
        )

        if not can_vote:
            logger.error(f"User {user_id} cannot vote on {vote_date}: {error_msg}")
            return None, error_msg

        # Calculate weight and create vote
        weight = self.voting_service.calculate_vote_weight(user_id, restaurant_id, vote_date)
        vote = Vote(
            id=None,
            user_id=user_id,
            restaurant_id=restaurant_id,
            weight=weight
        )

        saved_vote = self.vote_repository.save(vote)
        logger.info(f"User {user_id} voted for restaurant {restaurant_id} with weight {weight} on {vote_date}")
        return saved_vote, ""

    def get_user_votes(self, user_id: int, vote_date: date) -> List[Vote]:
        return self.vote_repository.get_user_votes_for_date(user_id, vote_date)
