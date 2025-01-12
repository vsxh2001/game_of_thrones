from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .base import Base


class CubeTakeover(Base):
    __tablename__ = "cube_takeovers"

    id = Column(Integer, primary_key=True)
    round_id = Column(Integer, ForeignKey("rounds.id"), nullable=False)
    cube_id = Column(Integer, ForeignKey("cubes.id"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    takeover_time = Column(DateTime, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    round = relationship("Round", back_populates="takeovers")
    cube = relationship("Cube", back_populates="takeovers")
    team = relationship("Team", back_populates="cube_takeovers")


class CubeKeepalive(Base):
    __tablename__ = "cube_keepalives"

    id = Column(Integer, primary_key=True)
    round_id = Column(Integer, ForeignKey("rounds.id"), nullable=False)
    cube_id = Column(Integer, ForeignKey("cubes.id"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    keepalive_time = Column(DateTime, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    round = relationship("Round", back_populates="keepalives")
    cube = relationship("Cube", back_populates="keepalives")
    team = relationship("Team", back_populates="cube_keepalives")
