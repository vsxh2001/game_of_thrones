from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .base import Base


class Cube(Base):
    __tablename__ = "cubes"

    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)
    name = Column(String(100), nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    match = relationship("Match", back_populates="cubes")
    configs = relationship("CubeConfig", back_populates="cube")
    takeovers = relationship("CubeTakeover", back_populates="cube")
    keepalives = relationship("CubeKeepalive", back_populates="cube")


class CubeConfig(Base):
    __tablename__ = "cube_configs"

    id = Column(Integer, primary_key=True)
    cube_id = Column(Integer, ForeignKey("cubes.id"), nullable=False)
    round_id = Column(Integer, ForeignKey("rounds.id"), nullable=False)
    points = Column(Integer, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    cube = relationship("Cube", back_populates="configs")
    round = relationship("Round", back_populates="cube_configs")
