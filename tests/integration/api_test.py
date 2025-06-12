"""
Tests for the exposed API server.
"""

from datetime import date

from fastapi.testclient import TestClient

from yt_membership_parser.api import ParseResult


def test_parse(client: TestClient):
    response = client.get("/parse")
    assert response.status_code == 200

    result = ParseResult.model_validate(response.json())
    assert result.next_billing_date == date(2025, 1, 1)
