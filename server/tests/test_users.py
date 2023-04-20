from unittest import TestCase

from fastapi.testclient import TestClient

from server.app import app
from server.models.userModel import User

client = TestClient(app)


class TestUser(TestCase):
    def test_get_users(self):
        response = client.get("/user/")
        assert response.status_code == 200
        assert len(response.json()["data"]) > 0

    def test_insert_user(self):
        user_data = {
            "firstname": "Alice",
            "lastname": "Smith",
            "username": "asmith",
            "email": "asmith@example.com",
            "password": "password",
        }
        user = User.create(**user_data).first()
        assert user.id is not None
        assert user.firstname == user_data["firstname"]
        assert user.lastname == user_data["lastname"]
        assert user.username == user_data["username"]
        assert user.email == user_data["email"]
        assert user.password == user_data["password"]
