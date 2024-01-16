import pytest
from httpx import AsyncClient

from app.main import app

pytestmark = pytest.mark.parametrize("anyio_backend", ["asyncio"])


async def test_root(anyio_backend):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "alive!"}


async def test_add_photo_to_db(anyio_backend):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        file = {"photo": open("./tests/test_data/test_photo.png", "rb")}
        response = await ac.post(
            "/v1/photo/add",
            data={
                "description": "Test description",
                "latitude": 0.0,
                "longitude": 0.0,
                "record_id": "uuid-for-record",
                "date_taken": "2024-01-16",
            },
            files=file,
        )
    print(response.json())
    assert response.status_code == 200
    assert response.json().get("description") == "Test description"
    assert response.json().get("record_id") == "uuid-for-record"
    assert response.json().get("date_taken") == "2024-01-16"


async def test_add_project_to_db(anyio_backend):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/v1/project/start",
            json={
                "country": "Russia",
                "city": "Moscow",
                "start_date": "2024-01-10",
                "end_date": "2024-01-20",
                "name": "TestProject",
                "owner_id": "uuid-for-user",
            },
        )
    assert response.status_code == 200
    assert response.json().get("country") == "Russia"
    assert response.json().get("city") == "Moscow"
    assert response.json().get("start_date") == "2024-01-10"
    assert response.json().get("end_date") == "2024-01-20"
    assert response.json().get("name") == "TestProject"


async def test_add_record_to_db(anyio_backend):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post()
