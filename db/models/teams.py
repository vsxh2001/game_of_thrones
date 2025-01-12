from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .base import Base


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    color = Column(String(100), nullable=False)
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=False)
    total_score = Column(Integer, default=0, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    season = relationship("Season", back_populates="teams")
    matches = relationship("Match", secondary="match_teams", back_populates="teams")
    round_scores = relationship("RoundScore", back_populates="team")
    cube_takeovers = relationship("CubeTakeover", back_populates="team")
    cube_keepalives = relationship("CubeKeepalive", back_populates="team")

    __table_args__ = (CheckConstraint("total_score >= 0", name="positive_score"),)
