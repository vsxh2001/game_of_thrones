import pytest
from datetime import datetime, timedelta
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_cube(client: AsyncClient):
    """Test creating a new cube."""
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

    # Create a match
    match_response = await client.post(
        "/api/v1/matches/",
        json={
            "name": "Test Match",
            "season_id": season_id,
        },
    )
    assert match_response.status_code == 201
    match_id = match_response.json()["id"]

    # Create a cube
    response = await client.post(
        "/api/v1/cubes/",
        json={
            "name": "Cube 1",
            "match_id": match_id,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Cube 1"
    assert data["match_id"] == match_id


@pytest.mark.asyncio
async def test_create_cube_config(client: AsyncClient):
    """Test creating a cube configuration for a round."""
    # Create a season
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

    # Create a match
    match_response = await client.post(
        "/api/v1/matches/",
        json={
            "name": "Test Match",
            "season_id": season_id,
        },
    )
    assert match_response.status_code == 201
    match_id = match_response.json()["id"]

    # Create a cube
    cube_response = await client.post(
        "/api/v1/cubes/",
        json={
            "name": "Cube 1",
            "match_id": match_id,
        },
    )
    assert cube_response.status_code == 201
    cube_id = cube_response.json()["id"]

    # Create a round
    round_response = await client.post(
        "/api/v1/rounds/",
        json={
            "match_id": match_id,
            "round_number": 1,
            "duration": 300,  # 5 minutes
            "gong_timedelta": 60,  # 1 minute
        },
    )
    assert round_response.status_code == 201
    round_id = round_response.json()["id"]

    # Create cube configuration
    response = await client.post(
        "/api/v1/cube-configs/",
        json={
            "cube_id": cube_id,
            "round_id": round_id,
            "points": 100,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["cube_id"] == cube_id
    assert data["round_id"] == round_id
    assert data["points"] == 100


@pytest.mark.asyncio
async def test_list_match_cubes(client: AsyncClient):
    """Test listing all cubes in a match."""
    # Create a season
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

    # Create a match
    match_response = await client.post(
        "/api/v1/matches/",
        json={
            "name": "Test Match",
            "season_id": season_id,
        },
    )
    assert match_response.status_code == 201
    match_id = match_response.json()["id"]

    # Create multiple cubes
    cube_names = ["Cube 1", "Cube 2", "Cube 3"]
    for name in cube_names:
        response = await client.post(
            "/api/v1/cubes/",
            json={
                "name": name,
                "match_id": match_id,
            },
        )
        assert response.status_code == 201

    # List cubes
    response = await client.get(f"/api/v1/cubes/?match_id={match_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(cube_names)
    assert all(cube["match_id"] == match_id for cube in data)
    assert all(cube["name"] in cube_names for cube in data)


@pytest.mark.asyncio
async def test_get_cube_configs(client: AsyncClient):
    """Test getting cube configurations for a round."""
    # Create a season
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

    # Create a match
    match_response = await client.post(
        "/api/v1/matches/",
        json={
            "name": "Test Match",
            "season_id": season_id,
        },
    )
    assert match_response.status_code == 201
    match_id = match_response.json()["id"]

    # Create cubes
    cubes = []
    for i in range(3):
        response = await client.post(
            "/api/v1/cubes/",
            json={
                "name": f"Cube {i+1}",
                "match_id": match_id,
            },
        )
        assert response.status_code == 201
        cubes.append(response.json())

    # Create a round
    round_response = await client.post(
        "/api/v1/rounds/",
        json={
            "match_id": match_id,
            "round_number": 1,
            "duration": 300,
            "gong_timedelta": 60,
        },
    )
    assert round_response.status_code == 201
    round_id = round_response.json()["id"]

    # Create cube configurations
    for i, cube in enumerate(cubes):
        response = await client.post(
            "/api/v1/cube-configs/",
            json={
                "cube_id": cube["id"],
                "round_id": round_id,
                "points": (i + 1) * 100,
            },
        )
        assert response.status_code == 201

    # Get cube configurations for the round
    response = await client.get(f"/api/v1/cube-configs/?round_id={round_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(cubes)
    assert all(config["round_id"] == round_id for config in data)
    assert all(config["points"] > 0 for config in data)


@pytest.mark.asyncio
async def test_create_duplicate_cube(client: AsyncClient):
    """Test creating a cube with duplicate name in the same match."""
    # Create a season
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

    # Create a match
    match_response = await client.post(
        "/api/v1/matches/",
        json={
            "name": "Test Match",
            "season_id": season_id,
        },
    )
    assert match_response.status_code == 201
    match_id = match_response.json()["id"]

    # Create first cube
    response = await client.post(
        "/api/v1/cubes/",
        json={
            "name": "Duplicate Cube",
            "match_id": match_id,
        },
    )
    assert response.status_code == 201

    # Try to create cube with same name
    response = await client.post(
        "/api/v1/cubes/",
        json={
            "name": "Duplicate Cube",
            "match_id": match_id,
        },
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_create_cube_invalid_match(client: AsyncClient):
    """Test creating a cube with an invalid match ID."""
    response = await client.post(
        "/api/v1/cubes/",
        json={
            "name": "Invalid Match Cube",
            "match_id": 99999,  # Non-existent match ID
        },
    )
    assert response.status_code == 404
    assert "match not found" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_create_cube_config_invalid_round(client: AsyncClient):
    """Test creating a cube configuration with an invalid round ID."""
    # Create a season and match first
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

    match_response = await client.post(
        "/api/v1/matches/",
        json={
            "name": "Test Match",
            "season_id": season_id,
        },
    )
    assert match_response.status_code == 201
    match_id = match_response.json()["id"]

    # Create a cube
    cube_response = await client.post(
        "/api/v1/cubes/",
        json={
            "name": "Test Cube",
            "match_id": match_id,
        },
    )
    assert cube_response.status_code == 201
    cube_id = cube_response.json()["id"]

    # Try to create cube config with invalid round
    response = await client.post(
        "/api/v1/cube-configs/",
        json={
            "cube_id": cube_id,
            "round_id": 99999,  # Non-existent round ID
            "points": 100,
        },
    )
    assert response.status_code == 404
    assert "round not found" in response.json()["detail"].lower()
