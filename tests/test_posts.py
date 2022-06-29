# args available via tests/conftest.py
# if the args are not apps to the function
# results may vary
def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")

    assert response.status_code == 200
