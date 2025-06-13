"""
Tests for the exposed API server.
"""

from datetime import date
from importlib import resources

from fastapi.testclient import TestClient
from freezegun import freeze_time

from yt_membership_parser.api import ParseResult


@freeze_time("2025-06-13")
def test_parse(client: TestClient):
    image_data = resources.files().joinpath("en_US.png").read_bytes()

    response = client.post("/parse", headers={"Content-Type": "image/png"}, content=image_data)
    assert response.status_code == 200

    result = ParseResult.model_validate(response.json())
    assert result.parsed_data is not None
    assert result.parsed_data.next_billing_date == date(2025, 7, 10)
