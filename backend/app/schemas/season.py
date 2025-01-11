from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SeasonBase(BaseModel):
    name: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class SeasonCreate(SeasonBase):
    pass

class SeasonUpdate(BaseModel):
    status: str  # upcoming, active, completed

class SeasonResponse(SeasonBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
