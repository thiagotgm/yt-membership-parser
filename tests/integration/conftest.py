"""
Fixtures for integration testing.
"""

import logging

import pytest
from fastapi.testclient import TestClient

from yt_membership_parser.api import app

_LOGGER = logging.getLogger(__name__)


@app.exception_handler(Exception)
def log_exceptions(_, exc: Exception):
    _LOGGER.exception("Server threw an exception", exc_info=exc)


@pytest.fixture(scope="session")
def client() -> TestClient:
    """
    The client for testing the API with.
    """
    return TestClient(app, raise_server_exceptions=False)
