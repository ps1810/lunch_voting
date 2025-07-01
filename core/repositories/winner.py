from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date
from ..entities.winner import DailyWinner


class WinnerRepository(ABC):
    @abstractmethod
    def get_by_date(self, target_date: date) -> Optional[DailyWinner]:
        pass

    @abstractmethod
    def save(self, winner: DailyWinner) -> DailyWinner:
        pass

    @abstractmethod
    def get_date_range(self, start_date: Optional[date], end_date: Optional[date]) -> List[DailyWinner]:
        pass