"""
Tests for the exposed API server.
"""

from fastapi.testclient import TestClient


def test_parse(client: TestClient):
    response = client.get("/parse")
    assert response.status_code == 500  # While not implemented
