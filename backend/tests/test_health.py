def test_health_endpoint(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    assert json_data["data"]["status"] == "healthy"
    assert json_data["data"]["database"] == "connected"


def test_version_endpoint(client):
    response = client.get("/api/v1/version")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    assert json_data["data"]["version"] == "1.0.0"
