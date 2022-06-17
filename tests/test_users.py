from fastapi.testclient import TestClient

from app import main

client = TestClient(main.app)


def test_root():
    response = client.get("/")
    assert response.json().get("message") == "Hello World"
    assert response.status_code == 200


def test_create_user():
    response = client.post(
        "/users/",
        json={"email": "hello@email.com", "password": "password123"}
    )

    assert response.json().get("email") == "hello@email.com"
    assert response.status_code == 201
