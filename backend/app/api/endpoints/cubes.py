from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.schemas.cube import CubeCreate, CubeResponse, CubeUpdate
from db.session import get_db
from db.models.cubes import Cube
from db.models.matches import Match

router = APIRouter()


@router.post("/", response_model=CubeResponse, status_code=201)
async def create_cube(cube: CubeCreate, db: AsyncSession = Depends(get_db)):
    """Create a new cube"""
    # Check if match exists and is active
    match_query = select(Match).where(Match.id == cube.match_id)
    match_ = await db.execute(match_query)
    match_ = match_.scalar_one_or_none()

    if not match_:
        raise HTTPException(status_code=404, detail="Match not found")

    # Create cube
    db_cube = Cube(match_id=cube.match_id, name=cube.name)
    db.add(db_cube)
    await db.commit()
    await db.refresh(db_cube)
    return db_cube


@router.get("/", response_model=List[CubeResponse])
async def list_cubes(
    round_id: int = None,
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """List all cubes"""
    query = select(Cube)
    if round_id:
        query = query.where(Cube.round_id == round_id)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{cube_id}", response_model=CubeResponse)
async def get_cube(cube_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific cube by ID"""
    query = select(Cube).where(Cube.id == cube_id)
    result = await db.execute(query)
    cube = result.scalar_one_or_none()

    if not cube:
        raise HTTPException(status_code=404, detail="Cube not found")
    return cube


@router.put("/{cube_id}", response_model=CubeResponse)
async def update_cube(
    cube_id: int, cube_update: CubeUpdate, db: AsyncSession = Depends(get_db)
):
    """Update a cube"""
    # Get cube
    query = select(Cube).where(Cube.id == cube_id)
    result = await db.execute(query)
    cube = result.scalar_one_or_none()

    if not cube:
        raise HTTPException(status_code=404, detail="Cube not found")

    # Update cube
    for field, value in cube_update.dict(exclude_unset=True).items():
        setattr(cube, field, value)

    await db.commit()
    await db.refresh(cube)
    return cube


@router.delete("/{cube_id}")
async def delete_cube(cube_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a cube"""
    query = select(Cube).where(Cube.id == cube_id)
    result = await db.execute(query)
    cube = result.scalar_one_or_none()

    if not cube:
        raise HTTPException(status_code=404, detail="Cube not found")

    await db.delete(cube)
    await db.commit()
    return {"message": "Cube deleted successfully"}
