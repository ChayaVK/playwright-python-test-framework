from playwright.sync_api import APIResponse

from api.api_client import ApiClient


class UsersApi:
    """One class per API resource keeps the endpoint paths in a single place."""

    def __init__(self, api: ApiClient):
        self.api = api

    def list(self) -> APIResponse:
        return self.api.get("/users")

    def get(self, user_id: int) -> APIResponse:
        return self.api.get(f"/users/{user_id}")

    def create(self, user: dict) -> APIResponse:
        return self.api.post("/users", user)

    def update(self, user_id: int, user: dict) -> APIResponse:
        return self.api.put(f"/users/{user_id}", user)

    def remove(self, user_id: int) -> APIResponse:
        return self.api.delete(f"/users/{user_id}")
