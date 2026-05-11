def test_create_and_list_lead(client, auth_headers):
    r = client.post(
        "/api/leads/",
        json={"title": "Big deal", "value": 5000, "notes": "Hot"},
        headers=auth_headers,
    )
    assert r.status_code == 201
    lead = r.json()
    assert lead["title"] == "Big deal"
    assert lead["stage"] == "new"

    r = client.get("/api/leads/", headers=auth_headers)
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_update_lead_stage(client, auth_headers):
    r = client.post("/api/leads/", json={"title": "X"}, headers=auth_headers)
    lead_id = r.json()["id"]
    r = client.patch(
        f"/api/leads/{lead_id}",
        json={"stage": "won", "value": 1000},
        headers=auth_headers,
    )
    assert r.status_code == 200
    assert r.json()["stage"] == "won"
    assert r.json()["value"] == 1000


def test_delete_lead(client, auth_headers):
    r = client.post("/api/leads/", json={"title": "X"}, headers=auth_headers)
    lead_id = r.json()["id"]
    r = client.delete(f"/api/leads/{lead_id}", headers=auth_headers)
    assert r.status_code == 204
    r = client.get("/api/leads/", headers=auth_headers)
    assert r.json() == []


def test_dashboard_stats(client, auth_headers):
    client.post(
        "/api/leads/",
        json={"title": "A", "value": 100, "stage": "won"},
        headers=auth_headers,
    )
    client.post(
        "/api/leads/",
        json={"title": "B", "value": 200, "stage": "lost"},
        headers=auth_headers,
    )
    client.post(
        "/api/leads/",
        json={"title": "C", "value": 300, "stage": "negotiating"},
        headers=auth_headers,
    )
    r = client.get("/api/leads/dashboard/stats", headers=auth_headers)
    assert r.status_code == 200
    body = r.json()
    assert body["total_leads"] == 3
    assert body["total_value"] == 600
    assert body["won"] == 1
    assert body["lost"] == 1
    assert body["in_progress"] == 1


def test_user_cannot_access_other_users_leads(client, auth_headers):
    r = client.post("/api/leads/", json={"title": "Mine"}, headers=auth_headers)
    lead_id = r.json()["id"]

    client.post(
        "/api/auth/register",
        json={"name": "Other", "email": "other@example.com", "password": "pw12345"},
    )
    r = client.post(
        "/api/auth/login",
        data={"username": "other@example.com", "password": "pw12345"},
    )
    other_headers = {"Authorization": f"Bearer {r.json()['access_token']}"}

    r = client.get("/api/leads/", headers=other_headers)
    assert r.json() == []
    r = client.patch(f"/api/leads/{lead_id}", json={"stage": "won"}, headers=other_headers)
    assert r.status_code == 404
