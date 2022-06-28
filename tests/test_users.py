import pytest

from app import schemas
from .database import client, session


@pytest.fixture
def test_user(client):
    user_data = {"email": "hello@email.com",
                 "password": "password123"}
    response = client.post("/users/", json=user_data)

    assert response.status_code == 201

    new_user = response.json()
    new_user['password'] = user_data["password"]

    return new_user


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json().get('message') == "Hello World"


@pytest.mark.parametrize("email, password", [
    ("hello@email.com", "password123")
])
def test_create_user(client, email, password):
    response = client.post(
        "/users/",
        json={"email": email, "password": password}
    )

    # Validate response against schema
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == email
    assert response.status_code == 201


def test_login(client, test_user):
    response = client.get("/login",
                          data={"username": test_user["email"], "password": test_user["password"]})
    assert response.status_code == 200
