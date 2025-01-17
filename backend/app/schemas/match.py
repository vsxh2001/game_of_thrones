from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from db.models.matches import MatchStatus


class MatchBase(BaseModel):
    season_id: int


class MatchCreate(MatchBase):
    name: str = Field(..., min_length=1, max_length=100)
    start_time: Optional[datetime] = None
    status: MatchStatus = Field(default=MatchStatus.SCHEDULED)


class MatchUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[MatchStatus] = None


class MatchTeamScore(BaseModel):
    team_id: int
    score: int = 0

    class Config:
        from_attributes = True


class MatchResponse(MatchBase):
    id: int
    name: str
    status: MatchStatus
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class MatchScoreUpdate(BaseModel):
    team_scores: List[MatchTeamScore] = Field(..., min_items=2, max_items=2)
