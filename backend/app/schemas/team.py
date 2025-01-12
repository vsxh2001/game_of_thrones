from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TeamBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    color: str = Field(..., min_length=1, max_length=100)
    season_id: int


class TeamCreate(TeamBase):
    pass


class TeamUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    color: Optional[str] = Field(None, min_length=1, max_length=100)
    total_score: Optional[int] = Field(None, ge=0)


class TeamResponse(TeamBase):
    id: int
    total_score: int = 0
    created_at: datetime

    class Config:
        from_attributes = True


class TeamWithScore(TeamResponse):
    score: int = 0
