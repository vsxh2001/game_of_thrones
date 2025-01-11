from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from enum import Enum


class MatchStatus(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class MatchTeam(BaseModel):
    team_id: int
    score: int = Field(default=0, ge=0)


class MatchBase(BaseModel):
    season_id: int
    start_time: datetime


class MatchCreate(MatchBase):
    teams: List[int] = Field(min_items=2)


class MatchUpdate(BaseModel):
    status: Optional[MatchStatus] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class MatchTeamResponse(MatchTeam):
    team_name: str
    team_color: str


class MatchResponse(MatchBase):
    id: int
    status: MatchStatus
    end_time: Optional[datetime] = None
    teams: List[MatchTeamResponse]
    created_at: datetime

    class Config:
        from_attributes = True
