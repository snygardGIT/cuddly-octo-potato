from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    original_activities = deepcopy(activities)
    test_client = TestClient(app)

    yield test_client

    activities.clear()
    activities.update(deepcopy(original_activities))
