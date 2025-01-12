from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from db.models.rounds import RoundStatus


class RoundBase(BaseModel):
    match_id: int
    round_number: int = Field(..., ge=1)
    duration: int = Field(..., ge=1)  # in seconds
    gong_timedelta: int = Field(..., ge=1)  # in seconds


class RoundCreate(RoundBase):
    pass


class RoundUpdate(BaseModel):
    start_time: Optional[datetime] = None
    duration: Optional[int] = Field(None, ge=1)
    gong_timedelta: Optional[int] = Field(None, ge=1)
    status: Optional[RoundStatus] = None


class RoundResponse(RoundBase):
    id: int
    status: RoundStatus
    start_time: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True
