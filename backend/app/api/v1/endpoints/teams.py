from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import datetime
from app.schemas.team import TeamCreate, TeamResponse
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.post("/", response_model=TeamResponse)
async def create_team(
    team: TeamCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new team"""
    # Check if season exists and is in correct state
    query = "SELECT status FROM seasons WHERE id = $1"
    result = await db.execute(query, [team.season_id])
    season_status = result.scalar()
    
    if not season_status:
        raise HTTPException(
            status_code=404,
            detail="Season not found"
        )
    if season_status != "upcoming":
        raise HTTPException(
            status_code=400,
            detail="Teams can only be added to upcoming seasons"
        )
    
    # Check if team name is unique in season
    query = """
        SELECT id FROM teams 
        WHERE season_id = $1 AND name = $2
    """
    result = await db.execute(query, [team.season_id, team.name])
    if result.scalar():
        raise HTTPException(
            status_code=400,
            detail="Team name already exists in this season"
        )
    
    # Create team
    query = """
        INSERT INTO teams (name, color, season_id, total_score)
        VALUES ($1, $2, $3, 0)
        RETURNING id, name, color, season_id, total_score, created_at
    """
    result = await db.execute(
        query,
        [team.name, team.color, team.season_id]
    )
    await db.commit()
    return result.mappings().first()

@router.get("/", response_model=List[TeamResponse])
async def list_teams(
    season_id: int,
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """List all teams in a season"""
    query = """
        SELECT id, name, color, season_id, total_score, created_at
        FROM teams
        WHERE season_id = $1
        ORDER BY total_score DESC
        OFFSET $2 LIMIT $3
    """
    result = await db.execute(query, [season_id, skip, limit])
    return result.mappings().all()

@router.get("/{team_id}", response_model=TeamResponse)
async def get_team(
    team_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific team by ID"""
    query = """
        SELECT id, name, color, season_id, total_score, created_at
        FROM teams WHERE id = $1
    """
    result = await db.execute(query, [team_id])
    team = result.mappings().first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@router.get("/{team_id}/stats")
async def get_team_stats(
    team_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get team statistics"""
    # Get team basic info
    query = """
        SELECT t.id, t.name, t.color, t.total_score,
               s.name as season_name, s.status as season_status
        FROM teams t
        JOIN seasons s ON t.season_id = s.id
        WHERE t.id = $1
    """
    result = await db.execute(query, [team_id])
    team = result.mappings().first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Get match statistics
    query = """
        SELECT 
            COUNT(DISTINCT m.id) as total_matches,
            COUNT(DISTINCT CASE WHEN mt.score > 0 THEN m.id END) as matches_with_points
        FROM teams t
        LEFT JOIN match_teams mt ON t.id = mt.team_id
        LEFT JOIN matches m ON mt.match_id = m.id
        WHERE t.id = $1
    """
    result = await db.execute(query, [team_id])
    match_stats = result.mappings().first()
    
    # Get cube control statistics
    query = """
        SELECT 
            COUNT(*) as total_captures,
            COUNT(DISTINCT cube_id) as unique_cubes_captured
        FROM cube_takeovers
        WHERE team_id = $1
    """
    result = await db.execute(query, [team_id])
    cube_stats = result.mappings().first()
    
    return {
        "team": team,
        "match_stats": match_stats,
        "cube_stats": cube_stats
    }