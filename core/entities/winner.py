from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date
from decimal import Decimal
from .vote import Vote


@dataclass
class DailyWinner:
    date: date
    restaurant_id: int
    restaurant_name: str
    total_score: Decimal
    unique_voters: int
    votes: Optional[List[Vote]] = field(default_factory=list)

    # def calculate_score(self) -> Decimal:
    #     return sum(vote.weight for vote in self.votes)
    #
    # def calculate_unique_voters(self) -> int:
    #     return len(set(vote.user_id for vote in self.votes))