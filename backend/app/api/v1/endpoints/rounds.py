from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.schemas.round import RoundCreate, RoundResponse, RoundUpdate
from db.session import get_db
from db.models.rounds import Round, RoundStatus
from db.models.matches import Match, MatchStatus

router = APIRouter()


@router.post("/", response_model=RoundResponse)
async def create_round(round: RoundCreate, db: AsyncSession = Depends(get_db)):
    """Create a new round"""
    # Check if match exists and is active
    match_query = select(Match).where(Match.id == round.match_id)
    match = await db.execute(match_query)
    match = match.scalar_one_or_none()

    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    if match.status != MatchStatus.ACTIVE:
        raise HTTPException(
            status_code=400, detail="Rounds can only be created in active matches"
        )

    # Create round
    db_round = Round(
        match_id=round.match_id, round_number=round.number, status=RoundStatus.PENDING
    )
    db.add(db_round)
    await db.commit()
    await db.refresh(db_round)
    return db_round


@router.get("/", response_model=List[RoundResponse])
async def list_rounds(
    match_id: int = None,
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """List all rounds"""
    query = select(Round)
    if match_id:
        query = query.where(Round.match_id == match_id)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{round_id}", response_model=RoundResponse)
async def get_round(round_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific round by ID"""
    query = select(Round).where(Round.id == round_id)
    result = await db.execute(query)
    round = result.scalar_one_or_none()

    if not round:
        raise HTTPException(status_code=404, detail="Round not found")
    return round


@router.put("/{round_id}", response_model=RoundResponse)
async def update_round(
    round_id: int, round_update: RoundUpdate, db: AsyncSession = Depends(get_db)
):
    """Update a round"""
    # Get round
    query = select(Round).where(Round.id == round_id)
    result = await db.execute(query)
    round = result.scalar_one_or_none()

    if not round:
        raise HTTPException(status_code=404, detail="Round not found")

    # Update round
    for field, value in round_update.dict(exclude_unset=True).items():
        setattr(round, field, value)

    await db.commit()
    await db.refresh(round)
    return round
