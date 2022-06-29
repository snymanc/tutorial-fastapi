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
