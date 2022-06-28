import pytest

from app import schemas
from .database import client, session


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


@pytest.mark.parametrize("email, password", [
    ("hello@email.com", "password123")
])
def test_login(client, email, password):
    response = client.get("/login",
                           data={"username": email, "password": password})
    assert response.status_code == 200
