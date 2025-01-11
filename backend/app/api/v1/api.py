from fastapi import APIRouter
from app.api.v1.endpoints import seasons, teams, matches, rounds, cubes

api_router = APIRouter()

api_router.include_router(seasons.router, prefix="/seasons", tags=["seasons"])
api_router.include_router(teams.router, prefix="/teams", tags=["teams"])
api_router.include_router(matches.router, prefix="/matches", tags=["matches"])
api_router.include_router(rounds.router, prefix="/rounds", tags=["rounds"])
api_router.include_router(cubes.router, prefix="/cubes", tags=["cubes"])
