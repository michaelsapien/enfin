
from pydantic import BaseModel
from typing import List
from datetime import date, time

class AvailabilityInput(BaseModel):
    user_ids: List[int]
    start_date: date
    end_date: date
    timezone: str
