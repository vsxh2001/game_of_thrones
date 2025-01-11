from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime
from app.schemas.match import MatchCreate, MatchResponse, MatchUpdate, MatchStatus
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/", response_model=MatchResponse)
async def create_match(match: MatchCreate, db: AsyncSession = Depends(get_db)):
    """Create a new match"""
    # Check if season exists and is in correct state
    query = "SELECT status FROM seasons WHERE id = $1"
    result = await db.execute(query, [match.season_id])
    season_status = result.scalar()

    if not season_status:
        raise HTTPException(status_code=404, detail="Season not found")
    if season_status not in ["upcoming", "active"]:
        raise HTTPException(
            status_code=400,
            detail="Matches can only be created in upcoming or active seasons",
        )

    # Validate teams exist and belong to the season
    teams_query = """
        SELECT id, name, color FROM teams
        WHERE id = ANY($1) AND season_id = $2
    """
    result = await db.execute(teams_query, [match.teams, match.season_id])
    teams = result.mappings().all()

    if len(teams) != 2:
        raise HTTPException(
            status_code=400,
            detail="Both teams must exist and belong to the specified season",
        )

    # Create match
    async with db.begin():
        # Insert match
        match_query = """
            INSERT INTO matches (season_id, start_time, status)
            VALUES ($1, $2, $3)
            RETURNING id, season_id, start_time, end_time, status, created_at
        """
        result = await db.execute(
            match_query, [match.season_id, match.start_time, MatchStatus.SCHEDULED]
        )
        match_data = result.mappings().first()

        # Insert match teams
        teams_insert_query = """
            INSERT INTO match_teams (match_id, team_id, score)
            VALUES ($1, $2, 0)
        """
        for team_id in match.teams:
            await db.execute(teams_insert_query, [match_data["id"], team_id])

    # Fetch complete match data
    return await get_match(match_data["id"], db)


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
    conditions = ["m.season_id = $1"]
    params = [season_id]
    param_count = 1

    if status:
        param_count += 1
        conditions.append(f"m.status = ${param_count}")
        params.append(status)

    if team_id:
        param_count += 1
        conditions.append(
            f"EXISTS (SELECT 1 FROM match_teams mt WHERE mt.match_id = m.id AND mt.team_id = ${param_count})"
        )
        params.append(team_id)

    where_clause = " AND ".join(conditions)

    query = f"""
        WITH match_data AS (
            SELECT
                m.id,
                m.season_id,
                m.start_time,
                m.end_time,
                m.status,
                m.created_at,
                json_agg(
                    json_build_object(
                        'team_id', t.id,
                        'team_name', t.name,
                        'team_color', t.color,
                        'score', mt.score
                    )
                ) as teams
            FROM matches m
            JOIN match_teams mt ON m.id = mt.match_id
            JOIN teams t ON mt.team_id = t.id
            WHERE {where_clause}
            GROUP BY m.id
            ORDER BY m.start_time DESC
            OFFSET ${param_count + 1} LIMIT ${param_count + 2}
        )
        SELECT *
        FROM match_data
    """

    result = await db.execute(query, params + [skip, limit])
    return result.mappings().all()


@router.get("/{match_id}", response_model=MatchResponse)
async def get_match(match_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific match by ID"""
    query = """
        SELECT
            m.id,
            m.season_id,
            m.start_time,
            m.end_time,
            m.status,
            m.created_at,
            json_agg(
                json_build_object(
                    'team_id', t.id,
                    'team_name', t.name,
                    'team_color', t.color,
                    'score', mt.score
                )
            ) as teams
        FROM matches m
        JOIN match_teams mt ON m.id = mt.match_id
        JOIN teams t ON mt.team_id = t.id
        WHERE m.id = $1
        GROUP BY m.id
    """
    result = await db.execute(query, [match_id])
    match = result.mappings().first()

    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match


@router.patch("/{match_id}", response_model=MatchResponse)
async def update_match(
    match_id: int, match_update: MatchUpdate, db: AsyncSession = Depends(get_db)
):
    """Update match details"""
    # Check if match exists
    current_match = await get_match(match_id, db)

    # Build update query
    update_fields = []
    params = []
    param_count = 1

    if match_update.status is not None:
        # Validate status transition
        if not _is_valid_status_transition(
            current_match["status"], match_update.status
        ):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status transition from {current_match['status']} to {match_update.status}",
            )
        update_fields.append(f"status = ${param_count}")
        params.append(match_update.status)
        param_count += 1

    if match_update.start_time is not None:
        update_fields.append(f"start_time = ${param_count}")
        params.append(match_update.start_time)
        param_count += 1

    if match_update.end_time is not None:
        if current_match["status"] != MatchStatus.IN_PROGRESS:
            raise HTTPException(
                status_code=400, detail="Can only set end time for in-progress matches"
            )
        update_fields.append(f"end_time = ${param_count}")
        params.append(match_update.end_time)
        param_count += 1

    if not update_fields:
        return current_match

    # Update match
    query = f"""
        UPDATE matches
        SET {", ".join(update_fields)}
        WHERE id = ${param_count}
        RETURNING id
    """
    params.append(match_id)

    await db.execute(query, params)
    await db.commit()

    return await get_match(match_id, db)


@router.post("/{match_id}/start")
async def start_match(match_id: int, db: AsyncSession = Depends(get_db)):
    """Start a match"""
    match = await get_match(match_id, db)

    if match["status"] != MatchStatus.SCHEDULED:
        raise HTTPException(
            status_code=400, detail="Match must be in scheduled state to start"
        )

    query = """
        UPDATE matches
        SET status = $1
        WHERE id = $2
        RETURNING id
    """
    await db.execute(query, [MatchStatus.IN_PROGRESS, match_id])
    await db.commit()

    return {"message": "Match started successfully"}


@router.post("/{match_id}/end")
async def end_match(match_id: int, db: AsyncSession = Depends(get_db)):
    """End a match"""
    match = await get_match(match_id, db)

    if match["status"] != MatchStatus.IN_PROGRESS:
        raise HTTPException(status_code=400, detail="Match must be in progress to end")

    async with db.begin():
        # Update match status and end time
        query = """
            UPDATE matches
            SET status = $1, end_time = $2
            WHERE id = $3
            RETURNING id
        """
        await db.execute(query, [MatchStatus.COMPLETED, datetime.now(), match_id])

        # Update team total scores from match_scores
        query = """
            UPDATE teams t
            SET total_score = total_score + ms.score
            FROM match_scores ms
            WHERE ms.match_id = $1 AND ms.team_id = t.id
        """
        await db.execute(query, [match_id])

    return {"message": "Match ended successfully"}


def _is_valid_status_transition(current_status: str, new_status: str) -> bool:
    """Validate match status transitions"""
    valid_transitions = {
        MatchStatus.SCHEDULED: {MatchStatus.IN_PROGRESS},
        MatchStatus.IN_PROGRESS: {MatchStatus.COMPLETED},
        MatchStatus.COMPLETED: set(),  # No transitions allowed from completed
    }
    return new_status in valid_transitions.get(current_status, set())
