from jose import jwt
import pytest

from app import schemas
from app.config import settings


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

    login_response = schemas.Token(**response.json())
    payload = jwt.decode(login_response.access_token,
                         settings.oauth2_secret_key,
                         algorithms=[settings.oauth2_algorithm])
    id = payload.get("owner_id")

    assert response.status_code == 200
    assert id == test_user["id"]
    assert login_response.token_type == "bearer"


def test_failed_login(client, test_user):
    response = client.get("/login",
                          data={"username": test_user["email"], "password": "wrongPassword"})

    assert response.status_code == 403
    assert response.json().get("detail") == "Invalid Credentials"
