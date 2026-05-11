def test_register_creates_user(client):
    r = client.post(
        "/api/auth/register",
        json={"name": "Alice", "email": "alice@example.com", "password": "pw12345"},
    )
    assert r.status_code == 201
    body = r.json()
    assert body["email"] == "alice@example.com"
    assert body["name"] == "Alice"
    assert "hashed_password" not in body


def test_register_duplicate_email_fails(client):
    payload = {"name": "Bob", "email": "bob@example.com", "password": "pw12345"}
    client.post("/api/auth/register", json=payload)
    r = client.post("/api/auth/register", json=payload)
    assert r.status_code == 400


def test_login_returns_token(client):
    client.post(
        "/api/auth/register",
        json={"name": "Carol", "email": "carol@example.com", "password": "pw12345"},
    )
    r = client.post(
        "/api/auth/login",
        data={"username": "carol@example.com", "password": "pw12345"},
    )
    assert r.status_code == 200
    assert r.json()["token_type"] == "bearer"
    assert r.json()["access_token"]


def test_login_wrong_password_fails(client):
    client.post(
        "/api/auth/register",
        json={"name": "Dan", "email": "dan@example.com", "password": "pw12345"},
    )
    r = client.post(
        "/api/auth/login",
        data={"username": "dan@example.com", "password": "wrong"},
    )
    assert r.status_code == 401


def test_protected_endpoint_requires_auth(client):
    r = client.get("/api/leads/")
    assert r.status_code == 401
