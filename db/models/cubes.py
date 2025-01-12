from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .base import Base


class Cube(Base):
    __tablename__ = "cubes"

    id = Column(Integer, primary_key=True)
    round_id = Column(Integer, ForeignKey("rounds.id"), nullable=False)
    points = Column(Integer, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    round = relationship("Round", back_populates="cubes")
    takeovers = relationship("CubeTakeover", back_populates="cube")
    keepalives = relationship("CubeKeepalive", back_populates="cube")
