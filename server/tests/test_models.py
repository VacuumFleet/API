import pytest
from bson import ObjectId
from server.models.userModel import UserSchema, UpdateUserModel
from server.models.tokenModel import Token, TokenData

def test_create_user_model():
    user_dict = {
        "firstname": "John",
        "lastname": "Doe",
        "email": "jdoe@mail.com",
        "username": "jdoe",
        "password": "fakehashedsecret",
    }
    user = UserSchema(**user_dict)
    assert user.id
    assert user.firstname == "John"
    assert user.lastname == "Doe"
    assert user.email == "jdoe@mail.com"
    assert user.username == "jdoe"
    assert user.password == "fakehashedsecret"


def test_update_user_model():
    user_dict = {
        "firstname": "John",
        "lastname": "Doe",
        "email": "jdoe@mail.com",
        "username": "jdoe",
        "password": "fakehashedsecret",
    }
    user = UpdateUserModel(**user_dict)
    assert user.firstname == "John"
    assert user.lastname == "Doe"
    assert user.email == "jdoe@mail.com"
    assert user.username == "jdoe"
    assert user.password == "fakehashedsecret"


def test_invalid_objectid():
    with pytest.raises(ValueError):
        bad_id = "not_an_objectid"
        UserSchema(id=bad_id, firstname="John", lastname="Doe", username="jdoe", email="jdoes@mail.com", password="fakehashedsecret")


def test_token_model():
    token = {
        "access_token": "fakeaccesstoken",
        "token_type": "bearer"
    }
    token = Token(**token)
    assert token.access_token == "fakeaccesstoken"
    assert token.token_type == "bearer"

def test_token_data_model():
    token_data = {
        "username": "jdoe"
    }
    token_data = TokenData(**token_data)
    assert token_data.username == "jdoe"
