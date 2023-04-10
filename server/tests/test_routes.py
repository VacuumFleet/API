from fastapi.testclient import TestClient
from server.app import app


client = TestClient(app)

id = None


# test create user endpoint
def test_create_user():
    user = {
        "firstname": "John",
        "lastname": "Doe",
        "email": "jdoe@mail.com",
        "username": "jdoe",
        "password": "fakehashedsecret",
    }
    response = client.post("/user/", json=user)
    assert response.status_code == 200
    assert response.json()["username"] == "johndoe"
    global id
    id = response.json()["id"]


# test login endpoint
def test_login():
    form_data = {"username": "jdoe", "password": "fakehashedsecret"}
    response = client.post("/token/", data=form_data)
    assert response.status_code == 200
    assert "access_token" in response.json()


# test list users endpoint
def test_list_users():
    response = client.get("/user/")
    assert response.status_code == 200
    assert len(response.json()) > 0


# test update user endpoint
def test_update_user():
    form_data = {
        "firstname": "Jane",
        "lastname": "Doe",
        "username": "jdoe",
        "email": "jdoe@example.com",
        "password": "fakehashedsecret",
    }
    response = client.put(f"/user/{id}", data=form_data)

    assert response.status_code == 200
    assert response.json()["firstname"] == "Jane"


# test delete user endpoint
def test_delete_user():
    response = client.delete(f"/user/{id}")
    assert response.status_code == 200
