from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Restaurant:
    id: Optional[int]
    name: str
    address: str
    phone: str
    cuisine_type: str
    is_votable: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if not self.name.strip():
            raise ValueError("Restaurant name cannot be empty")