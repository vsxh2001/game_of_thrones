from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from db.models.matches import MatchStatus
from .team import TeamWithScore


class MatchBase(BaseModel):
    season_id: int


class MatchCreate(MatchBase):
    team_ids: List[int] = Field(..., min_items=2, max_items=2)
    start_time: Optional[datetime] = None


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
    status: MatchStatus
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    created_at: datetime
    teams: List[TeamWithScore] = []

    class Config:
        from_attributes = True


class MatchScoreUpdate(BaseModel):
    team_scores: List[MatchTeamScore] = Field(..., min_items=2, max_items=2)
