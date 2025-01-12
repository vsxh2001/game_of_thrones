from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from db.models.seasons import SeasonStatus


class SeasonBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class SeasonCreate(SeasonBase):
    pass


class SeasonUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[SeasonStatus] = None


class SeasonResponse(SeasonBase):
    id: int
    status: SeasonStatus
    created_at: datetime

    class Config:
        from_attributes = True
