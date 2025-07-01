from decimal import Decimal
from datetime import date
from typing import Tuple
from ..entities.vote import VoteWeight
from ..repositories.vote import VoteRepository


class VotingService:
    def __init__(self, vote_repository: VoteRepository):
        self.vote_repository = vote_repository

    def calculate_vote_weight(self, user_id: int, restaurant_id: int, vote_date: date) -> Decimal:
        """Calculate vote weight based on user's previous votes for this restaurant today"""
        existing_votes = self.vote_repository.get_user_votes_for_restaurant_for_date(user_id, restaurant_id, vote_date)
        vote_count = len(existing_votes)

        if vote_count == 0:
            return VoteWeight.FIRST.value
        elif vote_count == 1:
            return VoteWeight.SECOND.value
        else:
            return VoteWeight.SUBSEQUENT.value

    def can_user_vote(self, user_id: int, vote_date: date, max_votes: int) -> Tuple[bool, str]:
        """Check if user can vote for a restaurant"""

        # Check daily vote limit
        user_votes_today = self.vote_repository.get_user_votes_for_date(user_id, vote_date)
        if len(user_votes_today) >= max_votes:
            return False, f"Daily vote limit of {max_votes} reached"

        return True, ""