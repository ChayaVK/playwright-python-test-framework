from playwright.sync_api import APIRequestContext, APIResponse

from config.settings import settings


class ApiClient:
    """Thin wrapper over Playwright's APIRequestContext: base URL, auth token and JSON helpers."""

    def __init__(self, request: APIRequestContext, base_url: str = settings.api_url):
        self.request = request
        self.base_url = base_url
        self.token: str | None = None

    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    def login(self, username: str = settings.username, password: str = settings.password) -> str:
        response = self.post("/login", {"username": username, "password": password})
        assert response.status == 200, f"login should succeed, got {response.status}"
        self.token = response.json()["token"]
        return self.token

    def get(self, path: str) -> APIResponse:
        return self.request.get(self._url(path), headers=self._headers())

    def post(self, path: str, data: dict) -> APIResponse:
        return self.request.post(self._url(path), data=data, headers=self._headers())

    def put(self, path: str, data: dict) -> APIResponse:
        return self.request.put(self._url(path), data=data, headers=self._headers())

    def delete(self, path: str) -> APIResponse:
        return self.request.delete(self._url(path), headers=self._headers())
