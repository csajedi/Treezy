import pytest
from starlette.testclient import TestClient

from app.main import app
from core import *

@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client  # testing happens here
