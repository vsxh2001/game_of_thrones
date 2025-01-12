from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.app.schemas.season import SeasonCreate, SeasonResponse
from db.session import get_db
from db.models.seasons import Season, SeasonStatus
from typing import List

router = APIRouter()


@router.post("/", response_model=SeasonResponse, status_code=201)
async def create_season(season: SeasonCreate, db: AsyncSession = Depends(get_db)):
    """Create a new season"""
    db_season = Season(
        name=season.name,
        start_date=season.start_date,
        end_date=season.end_date,
        status=SeasonStatus.UPCOMING,
    )
    db.add(db_season)
    await db.commit()
    await db.refresh(db_season)
    return db_season


@router.post("/{season_id}/start", response_model=SeasonResponse)
async def start_season(season_id: int, db: AsyncSession = Depends(get_db)):
    """Start a season"""
    query = select(Season).where(Season.id == season_id)
    result = await db.execute(query)
    season = result.scalar_one_or_none()

    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    if season.status != SeasonStatus.UPCOMING:
        raise HTTPException(
            status_code=400, detail="Only upcoming seasons can be started"
        )

    season.status = SeasonStatus.ACTIVE
    await db.commit()
    await db.refresh(season)
    return season


@router.post("/{season_id}/end", response_model=SeasonResponse)
async def end_season(season_id: int, db: AsyncSession = Depends(get_db)):
    """End a season"""
    query = select(Season).where(Season.id == season_id)
    result = await db.execute(query)
    season = result.scalar_one_or_none()

    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    if season.status != SeasonStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Only active seasons can be ended")

    season.status = SeasonStatus.COMPLETED
    await db.commit()
    await db.refresh(season)
    return season


@router.get("/", response_model=List[SeasonResponse])
async def list_seasons(
    db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100
):
    """List all seasons"""
    query = select(Season).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{season_id}", response_model=SeasonResponse)
async def get_season(season_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific season by ID"""
    query = select(Season).where(Season.id == season_id)
    result = await db.execute(query)
    season = result.scalar_one_or_none()

    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    return season
