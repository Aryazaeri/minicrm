def test_create_and_list_contact(client, auth_headers):
    r = client.post(
        "/api/contacts/",
        json={"name": "Acme Corp", "email": "info@acme.com", "company": "Acme"},
        headers=auth_headers,
    )
    assert r.status_code == 201
    assert r.json()["name"] == "Acme Corp"

    r = client.get("/api/contacts/", headers=auth_headers)
    assert len(r.json()) == 1


def test_delete_contact(client, auth_headers):
    r = client.post(
        "/api/contacts/",
        json={"name": "Bye Co"},
        headers=auth_headers,
    )
    cid = r.json()["id"]
    r = client.delete(f"/api/contacts/{cid}", headers=auth_headers)
    assert r.status_code == 204
    r = client.get("/api/contacts/", headers=auth_headers)
    assert r.json() == []
