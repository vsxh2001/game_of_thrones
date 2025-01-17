from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from .base import Base


class RoundStatus(str, enum.Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"


class Round(Base):
    __tablename__ = "rounds"

    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)
    round_number = Column(Integer, nullable=False)
    start_time = Column(DateTime, nullable=True)
    duration = Column(Integer, nullable=False)  # in seconds
    gong_timedelta = Column(Integer, nullable=False)  # in seconds
    status = Column(
        Enum(RoundStatus, name="round_status"),
        default=RoundStatus.PENDING,
        nullable=False,
    )
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("match_id", "round_number", name="unique_match_round_number"),
    )

    # Relationships
    match = relationship("Match", back_populates="rounds")
    scores = relationship("RoundScore", back_populates="round")
    takeovers = relationship("CubeTakeover", back_populates="round")
    keepalives = relationship("CubeKeepalive", back_populates="round")
    cube_configs = relationship("CubeConfig", back_populates="round")
