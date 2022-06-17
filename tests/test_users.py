from fastapi.testclient import TestClient

from app import main, schemas

client = TestClient(main.app)


def test_root():
    response = client.get("/")
    assert response.json().get("message") == "Hello World"
    assert response.status_code == 200
