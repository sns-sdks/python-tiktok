import json

import pytest

from pytiktok import BusinessAccountApi


class Helpers:
    @staticmethod
    def load_json(file_path):
        with open(file_path, "rb") as f:
            return json.loads(f.read().decode("utf-8"))


@pytest.fixture
def helpers():
    return Helpers


@pytest.fixture
def bus_api():
    return BusinessAccountApi(
        app_id="test_app_id",
        app_secret="test_app_secret",
        access_token="test_access_token",
    )
