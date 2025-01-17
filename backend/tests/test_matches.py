import pytest
from datetime import datetime, timedelta
from httpx import AsyncClient
from db.models.matches import MatchStatus


@pytest.mark.asyncio
async def test_create_match(client: AsyncClient):
    # First create a season
    start_date = datetime(2025, 1, 11, 21, 25, 28)
    end_date = start_date + timedelta(days=90)
    season_response = await client.post(
        "api/v1/seasons/",
        json={
            "name": "Test Season 2025",
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        },
    )
    assert season_response.status_code == 201
    season_data = season_response.json()
    season_id = season_data["id"]

    # Create a match
    response = await client.post(
        "api/v1/matches/",
        json={
            "name": "Test Match 1",
            "season_id": season_id,
            "start_time": start_date.isoformat(),
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Match 1"
    assert data["season_id"] == season_id
    assert data["status"] == "scheduled"
    assert data["start_time"] is not None


@pytest.mark.asyncio
async def test_list_matches(client: AsyncClient):
    # Create a season
    start_date = datetime(2025, 1, 11, 21, 25, 28)
    end_date = start_date + timedelta(days=90)
    season_response = await client.post(
        "api/v1/seasons/",
        json={
            "name": "Test Season 2025 - Matches",
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        },
    )
    season_id = season_response.json()["id"]

    # Create multiple matches
    matches = [{"name": f"Test Match {i}", "season_id": season_id} for i in range(1, 4)]

    for match in matches:
        await client.post("api/v1/matches/", json=match)

    # List matches
    response = await client.get(f"api/v1/matches/?season_id={season_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert all(match["season_id"] == season_id for match in data)


@pytest.mark.asyncio
async def test_get_match(client: AsyncClient):
    # Create a season
    start_date = datetime(2025, 1, 11, 21, 25, 28)
    end_date = start_date + timedelta(days=90)
    season_response = await client.post(
        "api/v1/seasons/",
        json={
            "name": "Test Season 2025 - Single Match",
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        },
    )
    season_id = season_response.json()["id"]

    # Create a match
    match_response = await client.post(
        "api/v1/matches/",
        json={
            "name": "Test Match Single",
            "season_id": season_id,
        },
    )
    match_id = match_response.json()["id"]

    # Get the match
    response = await client.get(f"api/v1/matches/{match_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == match_id
    assert data["name"] == "Test Match Single"
    assert data["season_id"] == season_id


@pytest.mark.asyncio
async def test_update_match(client: AsyncClient):
    # Create a season
    start_date = datetime(2025, 1, 11, 21, 25, 28)
    end_date = start_date + timedelta(days=90)
    season_response = await client.post(
        "api/v1/seasons/",
        json={
            "name": "Test Season 2025 - Update Match",
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        },
    )
    season_id = season_response.json()["id"]

    # Create a match
    match_response = await client.post(
        "api/v1/matches/",
        json={
            "name": "Test Match Update",
            "season_id": season_id,
        },
    )
    match_id = match_response.json()["id"]

    # Update the match
    new_start_time = datetime(2025, 1, 12, 21, 25, 28)
    response = await client.patch(
        f"api/v1/matches/{match_id}",
        json={
            "start_time": new_start_time.isoformat(),
            "status": MatchStatus.IN_PROGRESS.value,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == match_id
    assert data["start_time"] == new_start_time.isoformat()
    assert data["status"] == MatchStatus.IN_PROGRESS.value


@pytest.mark.asyncio
async def test_match_lifecycle(client: AsyncClient):
    # Create a season
    start_date = datetime(2025, 1, 11, 21, 25, 28)
    end_date = start_date + timedelta(days=90)
    season_response = await client.post(
        "api/v1/seasons/",
        json={
            "name": "Test Season 2025 - Match Lifecycle",
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        },
    )
    season_id = season_response.json()["id"]

    # Start the season
    await client.post(f"api/v1/seasons/{season_id}/start")

    # Create a match
    match_response = await client.post(
        "api/v1/matches/",
        json={
            "name": "Test Match Lifecycle",
            "season_id": season_id,
        },
    )
    match_id = match_response.json()["id"]

    # Start the match
    response = await client.post(f"api/v1/matches/{match_id}/start")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == MatchStatus.IN_PROGRESS.value

    # End the match
    response = await client.post(f"api/v1/matches/{match_id}/end")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == MatchStatus.COMPLETED.value
