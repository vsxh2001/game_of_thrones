from .seasons import Season
from sqlalchemy.orm import relationship


# Add back-populates for relationships
Season.teams = relationship("Team", back_populates="season")
Season.matches = relationship("Match", back_populates="season")
