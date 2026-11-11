import pytest

from api.api_client import ApiClient

pytestmark = pytest.mark.api


@pytest.mark.smoke
def test_health_check_is_up(api: ApiClient):
    response = api.get("/health")
    assert response.status == 200
    assert response.json() == {"status": "UP"}


def test_lists_all_products_with_the_right_shape(api: ApiClient):
    response = api.get("/products")
    assert response.ok
    body = response.json()
    assert len(body) == 6
    for product in body:
        assert isinstance(product["id"], int)
        assert isinstance(product["name"], str)
        assert isinstance(product["price"], float)


def test_gets_one_product_and_404_for_a_missing_one(api: ApiClient):
    assert api.get("/products/3").json()["name"] == "USB-C Cable"
    assert api.get("/products/999").status == 404


def test_login_with_a_wrong_password_returns_401(api: ApiClient):
    response = api.post("/login", {"username": "standard_user", "password": "wrong"})
    assert response.status == 401
