import unittest
import os
import json
import pytest
import httpx
from bson import ObjectId
import motor.motor_asyncio
from unittest import TestCase
from fastapi import FastAPI
from bson import ObjectId
from decouple import config
from pymongo import MongoClient
from server.app import app
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
    user_helper
)
from server.models.userModel import (
    ErrorResponseModel,
    ResponseModel,
    User,
    UpdateUserModel,
)
import pytest
import httpx
import asyncio
import json
import motor.motor_asyncio
import asyncio
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlencode
from datetime import datetime, timedelta
from typing import Union
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from decouple import config
from server.models.tokenModel import Token, TokenData
from server.routes.auth import (
    verify_password,
    get_password_hash,
    authenticate_user,
    retrieve_user_by_username_with_pwd,
    create_access_token,
    get_current_user,
)
from typing import Annotated, Union
from server.routes.auth import (
    login_for_access_token
    )

from server.database import (
    add_robot,
    retrieve_robots,
    retrieve_robots_user,
    update_robot_user,
)

from server.models.robotModel import (
    ErrorResponseModel,
    ResponseModel,
    RobotInDB,
    Robot,
    RobotUpdateModel,
)

from server.models.userModel import (
    User,
    UserInDB
)

from bson import ObjectId
import motor.motor_asyncio
from decouple import config
from urllib.parse import urlencode
from urllib.parse import quote_plus
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import logging
import asyncio
from fastapi.testclient import TestClient
from bson import ObjectId
from decouple import config

import unittest
from fastapi import FastAPI, Request
from httpx import AsyncClient


from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from server.database import (
    add_robot,
    retrieve_robots,
)
from server.models.robotModel import (
    ResponseModel,
    Robot,
)


from fastapi.testclient import TestClient
from server.app import app

router = APIRouter()

# from pytest import asyncio
import pytest
from fastapi import HTTPException
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient
from bson import ObjectId
# from app.main import app
# from app.models.robot import RobotInDB
# from server.models.user import User
from server.database import user_collection, robot_collection
client = TestClient(app)

from server.database import (
    retrieve_user_by_username,
    retrieve_user_by_username_with_pwd,
)
from server.app import (
    app,
)


# from server.app import app

# client = TestClient(app)

router = APIRouter()
client = motor.motor_asyncio.AsyncIOMotorClient("MONGODB_URL")

router = APIRouter()

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
            "password": "password"
        }
        user = User.create(**user_data).first()
        assert user.id is not None
        assert user.firstname == user_data["firstname"]
        assert user.lastname == user_data["lastname"]
        assert user.username == user_data["username"]
        assert user.email == user_data["email"]
        assert user.password == user_data["password"]


# @pytest.mark.asyncio
# async def test_create_user():
#     async with httpx.AsyncClient(app=app, base_url="http://127.0.0.1:8000/") as client:
#         # create a test user
#         user_data = {
#             "firstname": "Alice",
#             "lastname": "Smith",
#             "username": "asmith",
#             "email": "asmith@example.com",
#             "password": "password"
#         }
#         response = await client.post("/user/", json=user_data)
#         assert response.status_code == 200
#         assert response.json() == {
#             "data": {
#                 "firstname": "Alice",
#                 "lastname": "Smith",
#                 "username": "asmith",
#                 "email": "asmith@example.com"
#             },
#             "code": 200,
#             "message": "User added successfully."
#         }
    
# async def test_add_user():
#     # Création d'un utilisateur
#     user_data = {
#         "firstname": "Alice",
#         "lastname": "Smith",
#         "username": "asmith",
#         "email": "asmith@example.com",
#         "password": "password"
#     }

#     try:
#         response = await client.post("/user/", json=user_data)
#     except Exception as e:
#             print(f"Exception: {e}")
#             raise
#     assert response.status_code == 200

#     # Ajout de l'utilisateur à la base de données
#     new_user = await add_user(user_data)

#     # Vérification que les données de l'utilisateur ajouté correspondent aux données de l'utilisateur créé
#     assert new_user["firstname"] == user_data["firstname"]
#     assert new_user["lastname"] == user_data["lastname"]
#     assert new_user["username"] == user_data["username"]
#     assert new_user["email"] == user_data["email"]

#     # Vérification que la fonction renvoie les bonnes données de l'utilisateur ajouté
#     inserted_user = await user_collection.find_one({"_id": new_user["_id"]})
#     assert new_user == user_helper(inserted_user)