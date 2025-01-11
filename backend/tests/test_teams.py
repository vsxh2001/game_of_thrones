import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_team(async_client: AsyncClient):
    """Test creating a new team."""
    # Create a season first
    season_response = await async_client.post(
        "/api/v1/seasons/", json={"name": "Test Season"}
    )
    season_id = season_response.json()["id"]

    # Create team
    response = await async_client.post(
        "/api/v1/teams/",
        json={"name": "Test Team", "color": "#FF0000", "season_id": season_id},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Team"
    assert data["color"] == "#FF0000"
    assert data["season_id"] == season_id
    assert data["total_score"] == 0


@pytest.mark.asyncio
async def test_list_teams(async_client: AsyncClient):
    """Test listing teams in a season."""
    # Create a season
    season_response = await async_client.post(
        "/api/v1/seasons/", json={"name": "Test Teams Season"}
    )
    season_id = season_response.json()["id"]

    # Create multiple teams
    teams = [
        {"name": f"Test Team {i}", "color": f"#FF{i:04d}", "season_id": season_id}
        for i in range(3)
    ]
    for team in teams:
        await async_client.post("/api/v1/teams/", json=team)

    # List teams
    response = await async_client.get(f"/api/v1/teams/?season_id={season_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3
    assert all(t["season_id"] == season_id for t in data)


@pytest.mark.asyncio
async def test_get_team(async_client: AsyncClient):
    """Test getting a specific team."""
    # Create a season
    season_response = await async_client.post(
        "/api/v1/seasons/", json={"name": "Test Get Team Season"}
    )
    season_id = season_response.json()["id"]

    # Create a team
    create_response = await async_client.post(
        "/api/v1/teams/",
        json={"name": "Test Get Team", "color": "#00FF00", "season_id": season_id},
    )
    team_id = create_response.json()["id"]

    # Get the team
    response = await async_client.get(f"/api/v1/teams/{team_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Get Team"
    assert data["id"] == team_id


@pytest.mark.asyncio
async def test_create_team_invalid_season(async_client: AsyncClient):
    """Test creating a team with invalid season ID."""
    response = await async_client.post(
        "/api/v1/teams/",
        json={
            "name": "Invalid Team",
            "color": "#FF0000",
            "season_id": 99999,  # Non-existent season
        },
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_duplicate_team(async_client: AsyncClient):
    """Test creating a team with duplicate name in same season."""
    # Create a season
    season_response = await async_client.post(
        "/api/v1/seasons/", json={"name": "Test Duplicate Team Season"}
    )
    season_id = season_response.json()["id"]

    # Create first team
    team_data = {"name": "Duplicate Team", "color": "#FF0000", "season_id": season_id}
    await async_client.post("/api/v1/teams/", json=team_data)

    # Try to create duplicate team
    response = await async_client.post("/api/v1/teams/", json=team_data)
    assert response.status_code == 400
