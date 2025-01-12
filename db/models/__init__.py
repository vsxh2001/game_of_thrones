from .base import Base  # noqa: F401
from .seasons import Season  # noqa: F401
from .teams import Team  # noqa: F401
from .matches import Match  # noqa: F401
from .rounds import Round  # noqa: F401
from .scores import RoundScore, MatchScore, SeasonScore  # noqa: F401
from .cubes import Cube  # noqa: F401
from .cube_control import CubeTakeover, CubeKeepalive  # noqa: F401

from sqlalchemy.orm import relationship

# The models need to be imported in the correct order to handle SQLAlchemy relationships
# Base must be imported first, followed by models in dependency order
# noqa: F401 is used to ignore "unused import" warnings since these imports are needed for SQLAlchemy

# Add back-populates for relationships
Season.teams = relationship("Team", back_populates="season")
Season.matches = relationship("Match", back_populates="season")
