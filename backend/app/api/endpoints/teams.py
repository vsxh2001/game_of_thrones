from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy import select
from backend.app.schemas.team import TeamCreate, TeamResponse
from db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.teams import Team
from db.models.seasons import Season, SeasonStatus

router = APIRouter()


@router.post("/", response_model=TeamResponse, status_code=201)
async def create_team(team: TeamCreate, db: AsyncSession = Depends(get_db)):
    """Create a new team"""
    # Check if season exists and is in correct state
    season_query = select(Season).where(Season.id == team.season_id)
    result = await db.execute(season_query)
    season = result.scalar_one_or_none()

    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    if season.status != SeasonStatus.UPCOMING:
        raise HTTPException(
            status_code=400, detail="Teams can only be added to upcoming seasons"
        )

    # Check if team name is unique in season
    existing_team_query = select(Team).where(
        Team.season_id == team.season_id, Team.name == team.name
    )
    result = await db.execute(existing_team_query)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=400, detail="Team name must be unique within a season"
        )

    # Create team
    db_team = Team(name=team.name, color=team.color, season_id=team.season_id)
    db.add(db_team)
    await db.commit()
    await db.refresh(db_team)
    return db_team


@router.get("/", response_model=List[TeamResponse])
async def list_teams(
    season_id: int, db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100
):
    """List all teams in a season"""
    query = select(Team).where(Team.season_id == season_id)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{team_id}", response_model=TeamResponse)
async def get_team(team_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific team by ID"""
    query = select(Team).where(Team.id == team_id)
    result = await db.execute(query)
    team = result.scalar_one_or_none()

    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team
