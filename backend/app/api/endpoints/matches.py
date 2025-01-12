from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from datetime import datetime
from backend.app.schemas.match import (
    MatchCreate,
    MatchResponse,
    MatchUpdate,
    MatchStatus,
)
from db.session import get_db
from db.models.matches import Match, MatchStatus as DBMatchStatus
from db.models.seasons import Season, SeasonStatus
from db.models.teams import Team

router = APIRouter()


@router.post("/", response_model=MatchResponse)
async def create_match(match: MatchCreate, db: AsyncSession = Depends(get_db)):
    """Create a new match"""
    # Check if season exists and is in correct state
    season_query = select(Season).where(Season.id == match.season_id)
    season = await db.execute(season_query)
    season = season.scalar_one_or_none()

    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    if season.status not in [SeasonStatus.UPCOMING, SeasonStatus.ACTIVE]:
        raise HTTPException(
            status_code=400,
            detail="Matches can only be created in upcoming or active seasons",
        )

    # Validate teams exist and belong to the season
    teams_query = select(Team).where(
        Team.id.in_(match.teams), Team.season_id == match.season_id
    )
    result = await db.execute(teams_query)
    teams = result.scalars().all()

    if len(teams) != 2:
        raise HTTPException(
            status_code=400,
            detail="Both teams must exist and belong to the specified season",
        )

    # Create match
    db_match = Match(
        season_id=match.season_id,
        start_time=match.start_time,
        status=DBMatchStatus.SCHEDULED,
        teams=teams,
    )
    db.add(db_match)
    await db.commit()
    await db.refresh(db_match)
    return db_match


@router.get("/", response_model=List[MatchResponse])
async def list_matches(
    season_id: int,
    status: Optional[MatchStatus] = None,
    team_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """List matches with optional filters"""
    query = select(Match).where(Match.season_id == season_id)

    if status:
        query = query.where(Match.status == status)

    if team_id:
        query = query.join(Match.teams).where(Team.id == team_id)

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{match_id}", response_model=MatchResponse)
async def get_match(match_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific match by ID"""
    query = select(Match).where(Match.id == match_id)
    result = await db.execute(query)
    match = result.scalar_one_or_none()

    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match


@router.put("/{match_id}", response_model=MatchResponse)
async def update_match(
    match_id: int, match_update: MatchUpdate, db: AsyncSession = Depends(get_db)
):
    """Update match details"""
    query = select(Match).where(Match.id == match_id)
    result = await db.execute(query)
    match = result.scalar_one_or_none()

    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    # Update match
    for field, value in match_update.dict(exclude_unset=True).items():
        setattr(match, field, value)

    await db.commit()
    await db.refresh(match)
    return match


@router.post("/{match_id}/start", response_model=MatchResponse)
async def start_match(match_id: int, db: AsyncSession = Depends(get_db)):
    """Start a match"""
    query = select(Match).where(Match.id == match_id)
    result = await db.execute(query)
    match = result.scalar_one_or_none()

    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    if match.status != DBMatchStatus.SCHEDULED:
        raise HTTPException(
            status_code=400, detail="Match must be in scheduled state to start"
        )

    match.status = DBMatchStatus.IN_PROGRESS
    match.start_time = datetime.utcnow()
    await db.commit()
    await db.refresh(match)
    return match


@router.post("/{match_id}/end", response_model=MatchResponse)
async def end_match(match_id: int, db: AsyncSession = Depends(get_db)):
    """End a match"""
    query = select(Match).where(Match.id == match_id)
    result = await db.execute(query)
    match = result.scalar_one_or_none()

    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    if match.status != DBMatchStatus.IN_PROGRESS:
        raise HTTPException(status_code=400, detail="Match must be in progress to end")

    match.status = DBMatchStatus.COMPLETED
    match.end_time = datetime.utcnow()
    await db.commit()
    await db.refresh(match)
    return match
