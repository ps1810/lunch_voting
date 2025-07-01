from typing import Optional
from django.utils import timezone
from datetime import date
from ..entities.winner import DailyWinner
from ..repositories.vote import VoteRepository


class WinnerCalculationService:
    def __init__(self, vote_repository: VoteRepository):
        self.vote_repository = vote_repository
    def calculate_daily_winner(self, calculation_date: date=None) -> Optional[DailyWinner]:
        """Calculate the winner for a specific date"""
        if calculation_date is None:
            calculation_date = timezone.now().date()
        daily_score = self.vote_repository.get_votes_of_restaurants_for_date(calculation_date)

        if not daily_score:
            return None

        # Find winner (highest score, ties broken by unique voters)
        winner = max(daily_score, key=lambda r: (r.total_score, r.unique_voters))
        return DailyWinner(
            date=calculation_date,
            restaurant_id=winner.restaurant_id,
            restaurant_name= winner.restaurant_name,
            total_score=winner.total_score,
            unique_voters=winner.unique_voters,
        )