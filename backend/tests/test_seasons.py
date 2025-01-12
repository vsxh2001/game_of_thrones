import pytest
from datetime import datetime, timedelta
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_season(client: AsyncClient):
    start_date = datetime(2025, 1, 11, 21, 25, 28)
    end_date = start_date + timedelta(days=90)
    response = await client.post(
        "api/v1/seasons/",
        json={
            "name": "Test Season 2025",
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Season 2025"
    assert data["status"] == "upcoming"
    assert data["start_date"] is not None
    assert data["end_date"] is not None


@pytest.mark.asyncio
async def test_list_seasons(client: AsyncClient):
    # Create a few seasons first
    start_date = datetime(2025, 1, 11, 21, 25, 28)
    seasons = [
        {
            "name": f"Test Season {i}",
            "start_date": (start_date + timedelta(days=i * 90)).isoformat(),
            "end_date": (start_date + timedelta(days=(i + 1) * 90)).isoformat(),
        }
        for i in range(3)
    ]
    for season in seasons:
        response = await client.post("/api/v1/seasons/", json=season)
        assert response.status_code == 201

    # Test listing
    response = await client.get("/api/v1/seasons/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3
    assert all(s["name"].startswith("Test Season") for s in data[:3])


@pytest.mark.asyncio
async def test_get_season(client: AsyncClient):
    # Create a season
    start_date = datetime(2025, 1, 11, 21, 25, 28)
    end_date = start_date + timedelta(days=90)
    create_response = await client.post(
        "/api/v1/seasons/",
        json={
            "name": "Test Get Season",
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        },
    )
    assert create_response.status_code == 201
    season_id = create_response.json()["id"]

    # Get the season
    response = await client.get(f"/api/v1/seasons/{season_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Get Season"
    assert data["id"] == season_id


@pytest.mark.asyncio
async def test_start_season(client: AsyncClient):
    # Create a season
    start_date = datetime(2025, 1, 11, 21, 25, 28)
    end_date = start_date + timedelta(days=90)
    create_response = await client.post(
        "/api/v1/seasons/",
        json={
            "name": "Test Start Season",
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        },
    )
    assert create_response.status_code == 201
    season_id = create_response.json()["id"]

    # Start the season
    response = await client.post(f"/api/v1/seasons/{season_id}/start")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "active"
    assert data["id"] == season_id


@pytest.mark.asyncio
async def test_end_season(client: AsyncClient):
    # Create and start a season
    start_date = datetime(2025, 1, 11, 21, 25, 28)
    end_date = start_date + timedelta(days=90)
    create_response = await client.post(
        "/api/v1/seasons/",
        json={
            "name": "Test End Season",
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        },
    )
    assert create_response.status_code == 201
    season_id = create_response.json()["id"]

    # Start the season
    start_response = await client.post(f"/api/v1/seasons/{season_id}/start")
    assert start_response.status_code == 200

    # End the season
    response = await client.post(f"/api/v1/seasons/{season_id}/end")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert data["id"] == season_id


@pytest.mark.asyncio
async def test_invalid_season_transitions(client: AsyncClient):
    # Create seasons in different states
    start_date = datetime(2025, 1, 11, 21, 25, 28)
    end_date = start_date + timedelta(days=90)
    base_season = {
        "name": "Test Invalid Transitions",
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
    }

    # Create an active season
    active_response = await client.post("/api/v1/seasons/", json=base_season)
    assert active_response.status_code == 201
    active_id = active_response.json()["id"]
    start_response = await client.post(f"/api/v1/seasons/{active_id}/start")
    assert start_response.status_code == 200

    # Create a completed season
    completed_response = await client.post("/api/v1/seasons/", json=base_season)
    assert completed_response.status_code == 201
    completed_id = completed_response.json()["id"]
    await client.post(f"/api/v1/seasons/{completed_id}/start")
    await client.post(f"/api/v1/seasons/{completed_id}/end")

    # Test invalid transitions

    # Cannot start active season
    response = await client.post(f"/api/v1/seasons/{active_id}/start")
    assert response.status_code == 400

    # Cannot start completed season
    response = await client.post(f"/api/v1/seasons/{completed_id}/start")
    assert response.status_code == 400

    # Cannot end upcoming season
    upcoming_response = await client.post("/api/v1/seasons/", json=base_season)
    assert upcoming_response.status_code == 201
    upcoming_id = upcoming_response.json()["id"]
    response = await client.post(f"/api/v1/seasons/{upcoming_id}/end")
    assert response.status_code == 400

    # Cannot end completed season
    response = await client.post(f"/api/v1/seasons/{completed_id}/end")
    assert response.status_code == 400
