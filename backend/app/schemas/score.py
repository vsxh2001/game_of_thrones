from pydantic import BaseModel, Field
from datetime import datetime


class ScoreBase(BaseModel):
    team_id: int
    score: int = Field(..., ge=0)


class RoundScoreBase(ScoreBase):
    round_id: int


class RoundScoreCreate(RoundScoreBase):
    pass


class RoundScoreResponse(RoundScoreBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class MatchScoreBase(ScoreBase):
    match_id: int


class MatchScoreCreate(MatchScoreBase):
    pass


class MatchScoreResponse(MatchScoreBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class SeasonScoreBase(ScoreBase):
    season_id: int


class SeasonScoreCreate(SeasonScoreBase):
    pass


class SeasonScoreResponse(SeasonScoreBase):
    id: int
    updated_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True
