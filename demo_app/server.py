"""Practice Shop server: serves the demo web app and a small REST API.

Only the Python standard library is used, so there is nothing extra to install.
Start it by hand with:   python demo_app/server.py
The tests start it for you (see the demo_app fixture in tests/conftest.py).
"""
import json
import os
import re
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent
PORT = int(os.environ.get("DEMO_PORT", "3000"))
TOKEN = "demo-token-123"
EMAIL = re.compile(r"^\S+@\S+\.\S+$")

PRODUCTS = [
    {"id": 1, "slug": "laptop-bag", "name": "Laptop Bag", "price": 49.99},
    {"id": 2, "slug": "wireless-mouse", "name": "Wireless Mouse", "price": 19.99},
    {"id": 3, "slug": "usb-c-cable", "name": "USB-C Cable", "price": 9.99},
    {"id": 4, "slug": "bluetooth-speaker", "name": "Bluetooth Speaker", "price": 39.99},
    {"id": 5, "slug": "water-bottle", "name": "Water Bottle", "price": 14.99},
    {"id": 6, "slug": "desk-lamp", "name": "Desk Lamp", "price": 24.99},
]
USERS = [{"id": 1, "name": "Sample User", "email": "sample.user@example.com", "role": "tester"}]
NEXT_ID = [2]


def valid_user(body):
    return (
        isinstance(body, dict)
        and isinstance(body.get("name"), str)
        and body["name"].strip() != ""
        and bool(EMAIL.match(str(body.get("email", ""))))
    )


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, *args):  # keep the test output clean
        pass

    # ---------- helpers ----------
    def send_json(self, status, body=None):
        data = b"" if body is None else json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def read_body(self):
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b""
        try:
            return json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            return None

    # ---------- routing ----------
    def do_GET(self):
        self.route("GET")

    def do_POST(self):
        self.route("POST")

    def do_PUT(self):
        self.route("PUT")

    def do_DELETE(self):
        self.route("DELETE")

    def route(self, method):
        path = unquote(urlparse(self.path).path)
        if path.startswith("/api/"):
            return self.api(method, path)
        if method != "GET":
            return self.send_json(405, {"error": "Method not allowed"})
        if path == "/":
            self.path = "/index.html"
        if path.endswith(".py"):
            self.send_error(403)
            return
        return super().do_GET()

    def api(self, method, path):
        if path == "/api/health":
            return self.send_json(200, {"status": "UP"})

        if path == "/api/login" and method == "POST":
            body = self.read_body() or {}
            if body.get("username") == "standard_user" and body.get("password") == "Test@123":
                return self.send_json(200, {"token": TOKEN})
            return self.send_json(401, {"error": "Invalid credentials"})

        if path == "/api/products" and method == "GET":
            return self.send_json(200, PRODUCTS)

        match = re.fullmatch(r"/api/products/(\d+)", path)
        if match and method == "GET":
            item = next((p for p in PRODUCTS if p["id"] == int(match.group(1))), None)
            return self.send_json(200, item) if item else self.send_json(404, {"error": "Product not found"})

        if path.startswith("/api/users"):
            if self.headers.get("Authorization") != f"Bearer {TOKEN}":
                return self.send_json(401, {"error": "Missing or invalid token"})
            match = re.fullmatch(r"/api/users/(\d+)", path)
            if not match and method == "GET":
                return self.send_json(200, USERS)
            if not match and method == "POST":
                body = self.read_body()
                if not valid_user(body):
                    return self.send_json(400, {"error": "name and a valid email are required"})
                user = {"id": NEXT_ID[0], "name": body["name"], "email": body["email"], "role": body.get("role", "tester")}
                NEXT_ID[0] += 1
                USERS.append(user)
                return self.send_json(201, user)
            user = next((u for u in USERS if match and u["id"] == int(match.group(1))), None)
            if user is None:
                return self.send_json(404, {"error": "User not found"})
            if method == "GET":
                return self.send_json(200, user)
            if method == "PUT":
                body = self.read_body()
                if not valid_user(body):
                    return self.send_json(400, {"error": "name and a valid email are required"})
                user.update(name=body["name"], email=body["email"], role=body.get("role", user["role"]))
                return self.send_json(200, user)
            if method == "DELETE":
                USERS.remove(user)
                return self.send_json(204)

        return self.send_json(404, {"error": "Not found"})


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Practice Shop running at http://localhost:{PORT}  (press Ctrl+C to stop)", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
