import pytest
from datetime import datetime, timedelta
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_team(client: AsyncClient):
    """Test creating a new team."""
    # Create a season first
    start_date = datetime(2025, 1, 11, 21, 25, 28)
    end_date = start_date + timedelta(days=90)
    season_response = await client.post(
        "/api/v1/seasons/",
        json={
            "name": "Test Season",
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        },
    )
    assert season_response.status_code == 201
    season_id = season_response.json()["id"]

    # Create a team
    response = await client.post(
        "/api/v1/teams/",
        json={"name": "Test Team", "color": "#FF0000", "season_id": season_id},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Team"
    assert data["color"] == "#FF0000"
    assert data["season_id"] == season_id


@pytest.mark.asyncio
async def test_list_teams(client: AsyncClient):
    """Test listing teams in a season."""
    # Create a season first
    start_date = datetime(2025, 1, 11, 21, 25, 28)
    end_date = start_date + timedelta(days=90)
    season_response = await client.post(
        "/api/v1/seasons/",
        json={
            "name": "Test Season",
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        },
    )
    assert season_response.status_code == 201
    season_id = season_response.json()["id"]

    # Create a few teams
    teams = [
        {"name": f"Test Team {i}", "color": f"#FF{i:04d}", "season_id": season_id}
        for i in range(3)
    ]
    for team in teams:
        response = await client.post("/api/v1/teams/", json=team)
        assert response.status_code == 201

    # Test listing
    response = await client.get(f"/api/v1/teams/?season_id={season_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3
    assert all(team["season_id"] == season_id for team in data)


@pytest.mark.asyncio
async def test_get_team(client: AsyncClient):
    """Test getting a specific team."""
    # Create a season first
    start_date = datetime(2025, 1, 11, 21, 25, 28)
    end_date = start_date + timedelta(days=90)
    season_response = await client.post(
        "/api/v1/seasons/",
        json={
            "name": "Test Season",
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        },
    )
    assert season_response.status_code == 201
    season_id = season_response.json()["id"]

    # Create a team
    team_response = await client.post(
        "/api/v1/teams/",
        json={"name": "Test Get Team", "color": "#00FF00", "season_id": season_id},
    )
    assert team_response.status_code == 201
    team_id = team_response.json()["id"]

    # Get the team
    response = await client.get(f"/api/v1/teams/{team_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Get Team"
    assert data["color"] == "#00FF00"
    assert data["season_id"] == season_id


@pytest.mark.asyncio
async def test_create_team_invalid_season(client: AsyncClient):
    """Test creating a team with invalid season ID."""
    response = await client.post(
        "/api/v1/teams/",
        json={"name": "Invalid Team", "color": "#FF0000", "season_id": 999999},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Season not found"


@pytest.mark.asyncio
async def test_create_duplicate_team(client: AsyncClient):
    """Test creating a team with duplicate name in same season."""
    # Create a season first
    start_date = datetime(2025, 1, 11, 21, 25, 28)
    end_date = start_date + timedelta(days=90)
    season_response = await client.post(
        "/api/v1/seasons/",
        json={
            "name": "Test Season",
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        },
    )
    assert season_response.status_code == 201
    season_id = season_response.json()["id"]

    team_data = {"name": "Duplicate Team", "color": "#FF0000", "season_id": season_id}

    # First creation should succeed
    response1 = await client.post("/api/v1/teams/", json=team_data)
    assert response1.status_code == 201

    # Second creation with same name should fail
    response2 = await client.post("/api/v1/teams/", json=team_data)
    assert response2.status_code == 400
