import pytest
import os
from src.app import create_app

host = "http://localhost:5000"


@pytest.fixture
def host_endpoint():
    return os.path.join(host, "api", "v1").replace("\\", "/")
