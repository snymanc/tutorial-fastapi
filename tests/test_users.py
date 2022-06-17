from fastapi.testclient import TestClient
import pytest

from app import main, schemas

client = TestClient(main.app)


def test_root():
    response = client.get("/")
    assert response.json().get("message") == "Hello World"
    assert response.status_code == 200


@pytest.mark.parametrize("email, password", [
    ("hello@email.com", "password123")
])
def test_create_user(email, password):
    response = client.post(
        "/users/",
        json={"email": email, "password": password}
    )

    # Validate response against schema
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == email
    assert response.status_code == 201
