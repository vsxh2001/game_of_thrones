from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TeamBase(BaseModel):
    name: str
    color: str
    season_id: int

class TeamCreate(TeamBase):
    pass

class TeamResponse(TeamBase):
    id: int
    total_score: int
    created_at: datetime

    class Config:
        from_attributes = True
