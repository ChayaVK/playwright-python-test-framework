import pytest

from api.api_client import ApiClient
from api.users_api import UsersApi
from utils.random_data import random_email

pytestmark = pytest.mark.api


@pytest.mark.smoke
def test_create_read_update_and_delete_a_user(users_api: UsersApi):
    created = users_api.create({"name": "New Tester", "email": random_email("tester")})
    assert created.status == 201
    user_id = created.json()["id"]

    assert users_api.get(user_id).json()["name"] == "New Tester"

    updated = users_api.update(user_id, {"name": "Senior Tester", "email": random_email("senior")})
    assert updated.json()["name"] == "Senior Tester"

    assert users_api.remove(user_id).status == 204
    assert users_api.get(user_id).status == 404


def test_rejects_a_user_without_a_valid_email(users_api: UsersApi):
    assert users_api.create({"name": "No Email", "email": "not-an-email"}).status == 400


def test_calls_without_a_token_get_401(api: ApiClient):
    assert api.get("/users").status == 401
