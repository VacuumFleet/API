import os
import motor.motor_asyncio

from bson import ObjectId
from decouple import config
from pymongo import MongoClient

from fastapi.testclient import TestClient
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from decouple import config
from server.database import (
    add_user,
    delete_user,
    retrieve_user,
    retrieve_users,
    update_user,
)
from server.models.userModel import (
    ErrorResponseModel,
    ResponseModel,
    UserSchema,
    UpdateUserModel,
)

# from server.app import app

# client = TestClient(app)

router = APIRouter()
client = motor.motor_asyncio.AsyncIOMotorClient("MONGODB_URL")

#  User Route 

import unittest
import os

# from app import app

import json


def test_create_user(client):
    data = {
        "username":"jdoe",
        "email":"jdoe@example.com",
        "password":"secret1"}
    response = client.post("/users/",json.dumps(data))
    assert response.status_code == 200 
    assert response.json()["email"] == "testuser@nofoobar.com"
    assert response.json()["is_active"] == True