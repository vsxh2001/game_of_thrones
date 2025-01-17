from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
import enum

from .base import Base


class SeasonStatus(str, enum.Enum):
    UPCOMING = "upcoming"
    ACTIVE = "active"
    COMPLETED = "completed"


class Season(Base):
    __tablename__ = "seasons"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    status = Column(
        Enum(SeasonStatus, name="season_status"),
        default=SeasonStatus.UPCOMING,
        nullable=False,
    )
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
