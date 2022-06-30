import pytest

from app import schemas

# args available via tests/conftest.py
# if the args are not apps to the function
# results may vary


def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")

    def validate_posts(post):
        return schemas.PostOut(**post)

    posts_list = list(map(validate_posts, response.json()))

    assert response.status_code == 200
    assert len(response.json()) == len(test_posts)
    assert posts_list[0].Post.id == test_posts[0].id
    assert posts_list[1].Post.title == test_posts[1].title
    assert posts_list[2].Post.content == test_posts[2].content
    assert posts_list[3].Post.owner_id == test_posts[3].owner_id


def test_unauthorized_user_get_all_posts(client, test_posts):
    response = client.get("/posts/")
    assert response.status_code == 401


def test_unauthorized_get_post(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401


def test_get_post_not_exist(authorized_client, test_posts):
    response = authorized_client.get("/posts/-1")
    assert response.status_code == 404


def test_get_post_one_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")

    post = schemas.PostOut(**response.json())

    assert response.status_code == 200
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.owner_id == test_posts[0].owner_id


@pytest.mark.parametrize("title, content, published", [
    ("create post", "test create post", True),
    ("post creation", "creation of post", False),
    ("post", "create", True)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    response = authorized_client.post("/posts/",
                                      json={
                                          "title": title,
                                          "content": content,
                                          "published": published
                                      })

    created_post = schemas.Post(**response.json())

    assert response.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"]


def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    response = authorized_client.post("/posts/",
                                      json={
                                          "title": "title",
                                          "content": "content"
                                      })

    created_post = schemas.Post(**response.json())

    assert response.status_code == 201
    assert created_post.title == "title"
    assert created_post.content == "content"
    assert created_post.published == True
    assert created_post.owner_id == test_user["id"]


def test_unauthorized_user_create_post(client, test_user, test_posts):
    response = client.post("/posts/",
                           json={"title": "title", "content": "content"
                                 })

    assert response.status_code == 401


def test_unauthorized_user_delete_post(client, test_user, test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}")

    assert response.status_code == 401


def test_delete_post(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")

    assert response.status_code == 204


def test_delete_post_not_exist(authorized_client, test_user, test_posts):
    response = authorized_client.delete("/posts/-1")

    assert response.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[3].id}")

    assert response.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }

    response = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)

    updated_post = schemas.Post(**response.json())

    assert response.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]


def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }

    response = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)

    assert response.status_code == 403


def test_unauthorized_user_update_post(client, test_user, test_posts):
    response = client.put(f"/posts/{test_posts[0].id}")

    assert response.status_code == 401


def test_update_post_not_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }

    response = authorized_client.put("/posts/-1", json=data)

    assert response.status_code == 404
