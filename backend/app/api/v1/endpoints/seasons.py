from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import datetime
from app.schemas.season import SeasonCreate, SeasonResponse
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.post("/", response_model=SeasonResponse)
async def create_season(
    season: SeasonCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new season"""
    query = """
        INSERT INTO seasons (name, status)
        VALUES ($1, 'upcoming')
        RETURNING id, name, start_date, end_date, status, created_at
    """
    result = await db.execute(query, [season.name])
    await db.commit()
    return result.mappings().first()

@router.post("/{season_id}/start", response_model=SeasonResponse)
async def start_season(
    season_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Start a season"""
    # Check if season exists and is in correct state
    query = "SELECT status FROM seasons WHERE id = $1"
    result = await db.execute(query, [season_id])
    status = result.scalar()
    
    if not status:
        raise HTTPException(status_code=404, detail="Season not found")
    if status != 'upcoming':
        raise HTTPException(
            status_code=400,
            detail=f"Cannot start season in {status} status"
        )
    
    # Start the season
    query = """
        UPDATE seasons
        SET status = 'active',
            start_date = $1
        WHERE id = $2
        RETURNING id, name, start_date, end_date, status, created_at
    """
    result = await db.execute(query, [datetime.now(), season_id])
    await db.commit()
    return result.mappings().first()

@router.post("/{season_id}/end", response_model=SeasonResponse)
async def end_season(
    season_id: int,
    db: AsyncSession = Depends(get_db)
):
    """End a season"""
    # Check if season exists and is in correct state
    query = "SELECT status FROM seasons WHERE id = $1"
    result = await db.execute(query, [season_id])
    status = result.scalar()
    
    if not status:
        raise HTTPException(status_code=404, detail="Season not found")
    if status != 'active':
        raise HTTPException(
            status_code=400,
            detail=f"Cannot end season in {status} status"
        )
    
    # End the season
    query = """
        UPDATE seasons
        SET status = 'completed',
            end_date = $1
        WHERE id = $2
        RETURNING id, name, start_date, end_date, status, created_at
    """
    result = await db.execute(query, [datetime.now(), season_id])
    await db.commit()
    return result.mappings().first()

@router.get("/", response_model=List[SeasonResponse])
async def list_seasons(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """List all seasons"""
    query = """
        SELECT id, name, start_date, end_date, status, created_at
        FROM seasons
        ORDER BY created_at DESC
        OFFSET $1 LIMIT $2
    """
    result = await db.execute(query, [skip, limit])
    return result.mappings().all()

@router.get("/{season_id}", response_model=SeasonResponse)
async def get_season(
    season_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific season by ID"""
    query = """
        SELECT id, name, start_date, end_date, status, created_at
        FROM seasons WHERE id = $1
    """
    result = await db.execute(query, [season_id])
    season = result.mappings().first()
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    return season
