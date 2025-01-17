from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CubeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    match_id: int


class CubeCreate(CubeBase):
    pass


class CubeUpdate(BaseModel):
    name: Optional[str] = None


class CubeResponse(CubeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class CubeTakeoverBase(BaseModel):
    round_id: int
    cube_id: int
    team_id: int
    takeover_time: datetime


class CubeTakeoverCreate(CubeTakeoverBase):
    pass


class CubeTakeoverResponse(CubeTakeoverBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class CubeKeepaliveBase(BaseModel):
    round_id: int
    cube_id: int
    team_id: int
    keepalive_time: datetime


class CubeKeepaliveCreate(CubeKeepaliveBase):
    pass


class CubeKeepaliveResponse(CubeKeepaliveBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
