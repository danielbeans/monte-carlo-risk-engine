from unittest.mock import MagicMock

import pytest
import rq.job
from fastapi import testclient

from mcengine.db import postgres, redis_rq
from mcengine.main import app


@pytest.fixture()
def client() -> testclient.TestClient:
    return testclient.TestClient(app)