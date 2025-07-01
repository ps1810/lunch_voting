from dataclasses import dataclass
from typing import Optional
from datetime import date, datetime
from decimal import Decimal
from enum import Enum


class VoteWeight(Enum):
    FIRST = Decimal('1.0')
    SECOND = Decimal('0.5')
    SUBSEQUENT = Decimal('0.25')


@dataclass
class Vote:
    id: Optional[int]
    user_id: int
    restaurant_id: int
    weight: Decimal
    created_at: Optional[datetime] = None

    def __post_init__(self):
        if self.weight not in [e.value for e in VoteWeight]:
            raise ValueError(f"Invalid vote weight: {self.weight}")


@dataclass
class UserVoteStats:
    user_id: int
    date: date
    votes_used: int
    votes_remaining: int
    total_allowed: int

@dataclass
class RestaurantVoteStats:
    restaurant_id: int
    restaurant_name: str
    date: date
    total_votes: int
    unique_voters: int
    total_score: Decimal