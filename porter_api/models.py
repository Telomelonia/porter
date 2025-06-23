from dataclasses import dataclass
from typing import Optional

@dataclass
class VehicleQuote:
    name: str
    price_range: str
    min_price: Optional[int]
    max_price: Optional[int]
    capacity: str
    capacity_kg: Optional[int]
