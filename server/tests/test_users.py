from unittest import TestCase

from fastapi.testclient import TestClient

from server.app import app
from server.models.userModel import UserInDB

client = TestClient(app)


class TestUser(TestCase):
    def test_get_users(self):
        response = client.get("/user/")
        assert response.status_code == 200
        assert len(response.json()["data"]) > 0
