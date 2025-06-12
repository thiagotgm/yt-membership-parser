"""
Fixtures for integration testing.
"""

import pytest
from fastapi.testclient import TestClient

from yt_membership_parser.api import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    """
    The client for testing the API with.
    """
    return TestClient(app, raise_server_exceptions=False)
