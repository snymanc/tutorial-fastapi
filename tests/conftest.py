from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models
from app.config import settings
from app.database import get_db
from app.database import Base
from app.main import app
from app.oauth2 import create_access_token


SQLALCHEMY_DATABASE_URL = f"postgresql://" + \
                          f"{settings.database_username}:" + \
                          f"{settings.database_password}@" + \
                          f"{settings.database_hostname}:" + \
                          f"{settings.database_port}/" + \
                          f"{settings.database_name}_test"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "hello@email.com",
                 "password": "password123"}
    response = client.post("/users/", json=user_data)

    assert response.status_code == 201

    new_user = response.json()
    new_user['password'] = user_data["password"]

    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "hi@email.com",
                 "password": "password123"}
    response = client.post("/users/", json=user_data)

    assert response.status_code == 201

    new_user = response.json()
    new_user['password'] = user_data["password"]

    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token(data={"owner_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture
def test_posts(session, test_user, test_user2):
    # create post with map()
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd user title",
        "content": "2nd user content",
        "owner_id": test_user2['id']
    }]

    # iterator function to unpack posts_data
    def create_post_model(post):
        return models.Post(**post)

    # Using map() to iterate each posts_data
    # Converting map() results to list() for db data
    posts = list(map(create_post_model, posts_data))

    session.add_all(posts)
    session.commit()
    posts_results = session.query(models.Post).all()

    return posts_results
