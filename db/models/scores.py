from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .base import Base


class RoundScore(Base):
    __tablename__ = "round_scores"

    id = Column(Integer, primary_key=True)
    round_id = Column(Integer, ForeignKey("rounds.id"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    score = Column(Integer, default=0, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    round = relationship("Round", back_populates="scores")
    team = relationship("Team", back_populates="round_scores")

    __table_args__ = (
        UniqueConstraint(
            "round_id", "team_id", "created_at", name="unique_round_team_time"
        ),
    )


class MatchScore(Base):
    __tablename__ = "match_scores"

    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    score = Column(Integer, default=0, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    match = relationship("Match")
    team = relationship("Team")

    __table_args__ = (
        UniqueConstraint("match_id", "team_id", name="unique_match_score_team"),
    )


class SeasonScore(Base):
    __tablename__ = "season_scores"

    id = Column(Integer, primary_key=True)
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    score = Column(Integer, default=0, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    season = relationship("Season")
    team = relationship("Team")

    __table_args__ = (
        UniqueConstraint("season_id", "team_id", name="unique_season_team"),
    )
