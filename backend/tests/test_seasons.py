import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_season(async_client: AsyncClient):
    """Test creating a new season."""
    response = await async_client.post(
        "/api/v1/seasons/", json={"name": "Test Season 2025"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Season 2025"
    assert data["status"] == "upcoming"


@pytest.mark.asyncio
async def test_list_seasons(async_client: AsyncClient):
    """Test listing seasons."""
    # Create a few seasons first
    seasons = [{"name": f"Test Season {i}"} for i in range(3)]
    for season in seasons:
        await async_client.post("/api/v1/seasons/", json=season)

    # Test listing
    response = await async_client.get("/api/v1/seasons/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3
    assert all(s["name"].startswith("Test Season") for s in data[:3])


@pytest.mark.asyncio
async def test_get_season(async_client: AsyncClient):
    """Test getting a specific season."""
    # Create a season
    create_response = await async_client.post(
        "/api/v1/seasons/", json={"name": "Test Get Season"}
    )
    season_id = create_response.json()["id"]

    # Get the season
    response = await async_client.get(f"/api/v1/seasons/{season_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Get Season"
    assert data["id"] == season_id


@pytest.mark.asyncio
async def test_start_season(async_client: AsyncClient):
    """Test starting a season."""
    # Create a season
    create_response = await async_client.post(
        "/api/v1/seasons/", json={"name": "Test Start Season"}
    )
    season_id = create_response.json()["id"]

    # Start the season
    response = await async_client.post(f"/api/v1/seasons/{season_id}/start")
    assert response.status_code == 200

    # Verify season status
    get_response = await async_client.get(f"/api/v1/seasons/{season_id}")
    data = get_response.json()
    assert data["status"] == "active"
    assert data["start_date"] is not None


@pytest.mark.asyncio
async def test_end_season(async_client: AsyncClient):
    """Test ending a season."""
    # Create and start a season
    create_response = await async_client.post(
        "/api/v1/seasons/", json={"name": "Test End Season"}
    )
    season_id = create_response.json()["id"]
    await async_client.post(f"/api/v1/seasons/{season_id}/start")

    # End the season
    response = await async_client.post(f"/api/v1/seasons/{season_id}/end")
    assert response.status_code == 200

    # Verify season status
    get_response = await async_client.get(f"/api/v1/seasons/{season_id}")
    data = get_response.json()
    assert data["status"] == "completed"
    assert data["end_date"] is not None


@pytest.mark.asyncio
async def test_invalid_season_transitions(async_client: AsyncClient):
    """Test invalid season status transitions."""
    # Create a season
    create_response = await async_client.post(
        "/api/v1/seasons/", json={"name": "Test Invalid Transitions"}
    )
    season_id = create_response.json()["id"]

    # Try to end before starting
    response = await async_client.post(f"/api/v1/seasons/{season_id}/end")
    assert response.status_code == 400

    # Start the season
    await async_client.post(f"/api/v1/seasons/{season_id}/start")

    # Try to start again
    response = await async_client.post(f"/api/v1/seasons/{season_id}/start")
    assert response.status_code == 400

    # End the season
    await async_client.post(f"/api/v1/seasons/{season_id}/end")

    # Try to start completed season
    response = await async_client.post(f"/api/v1/seasons/{season_id}/start")
    assert response.status_code == 400

    # Try to end completed season
    response = await async_client.post(f"/api/v1/seasons/{season_id}/end")
    assert response.status_code == 400
