from typing import List, Optional
from datetime import date

from django.utils import timezone

from ..entities.winner import DailyWinner
from ..repositories.restaurant import RestaurantRepository
from ..repositories.vote import VoteRepository
from ..repositories.winner import WinnerRepository
from ..services.winner_calculation import WinnerCalculationService


class WinnerUseCases:
    def __init__(self, vote_repository: VoteRepository, restaurant_repository: RestaurantRepository,
                 winner_repository: WinnerRepository):
        self.vote_repository = vote_repository
        self.restaurant_repository = restaurant_repository
        self.winner_repository = winner_repository
        self.calculation_service = WinnerCalculationService(vote_repository)

    def get_daily_winner(self) -> Optional[DailyWinner]:
        # Try to get cached result first
        target_date = timezone.now().date()
        cached_result = self.winner_repository.get_by_date(target_date)
        if cached_result:
            return cached_result

        # Calculate and cache result
        winner = self.calculation_service.calculate_daily_winner()
        if winner:
            return self.winner_repository.save(winner)

        return None

    def force_calculate_winner(self, target_date: date) -> Optional[DailyWinner]:
        """Force recalculation of winner for a specific date"""
        winner = self.calculation_service.calculate_daily_winner(target_date)
        if winner:
            return self.winner_repository.save(winner)
        return None

    def get_winners_by_date_range(self, start_date: Optional[date], end_date: Optional[date]) -> List[DailyWinner]:
        return self.winner_repository.get_date_range(start_date, end_date)