import pytest

from app import schemas
from .database import client, session


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
