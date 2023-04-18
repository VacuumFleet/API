import pytest
from bson import ObjectId
from server.models import userModel
from server.models.userModel import User, UpdateUserModel, UserInDB
from server.models.robotModel import Robot, RobotInDB
from pydantic import BaseModel
from typing import Union
from server.models.tokenModel import Token, TokenData


# Test du UserModel

def test_create_user_model():
    user_dict = {
        "firstname": "John",
        "lastname": "Doe",
        "email": "jdoe@mail.com",
        "username": "jdoe",
        "password": "fakehashedsecret",
    }
    user = UserInDB(**user_dict)
    assert user.id
    assert user.firstname == "John"
    assert user.lastname == "Doe"
    assert user.email == "jdoe@mail.com"
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
        User(id=bad_id, first_name="John", last_name="Doe", role="simple mortal", is_active="false", last_login="datetime", password="fakehashedsecret")

# Test du tokenModel : 



def test_token_model():
    token = {"access_token": "fakeaccesstoken", "token_type": "bearer"}
    token = Token(**token)
    assert token.access_token == "fakeaccesstoken"
    assert token.token_type == "bearer"


def test_token_data_model():
    token_data = {"username": "jdoe"}
    token_data = TokenData(**token_data)
    assert token_data.username == "jdoe"

# Test du robot 


def test_robot_model():
    user_dict = {
                "name": "beepboop",
                "user": "id",
                "serial": "1234",
                }
    
    user = RobotInDB(**user_dict)
    assert user.name == "beepboop"
    assert user.serial == "1234"

