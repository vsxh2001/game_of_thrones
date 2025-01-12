from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    Enum,
    CheckConstraint,
    Table,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from .base import Base


class MatchStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


# Match Teams Association Table
match_teams = Table(
    "match_teams",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("match_id", Integer, ForeignKey("matches.id"), nullable=False),
    Column("team_id", Integer, ForeignKey("teams.id"), nullable=False),
    Column("score", Integer, default=0, nullable=False),
    Column(
        "created_at", DateTime(timezone=True), server_default=func.now(), nullable=False
    ),
    CheckConstraint("score >= 0", name="positive_score"),
)


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True)
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=False)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    status = Column(
        Enum(MatchStatus, name="match_status"),
        default=MatchStatus.SCHEDULED,
        nullable=False,
    )
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    season = relationship("Season", back_populates="matches")
    teams = relationship("Team", secondary=match_teams, back_populates="matches")
    rounds = relationship("Round", back_populates="match")
