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
    User
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

SECRET_KEY = config("SECRET")
ALGORITHM = config("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

client = TestClient(app)

# Test avec authentification

@pytest.mark.asyncio
async def test_create_robot_with_authentication():
    async with httpx.AsyncClient(app=app, base_url="http://127.0.0.1:8000/") as client:
        # create a test user
        user_data = {
            "firstname": "allo",
            "lastname": "al",
            "username": "all",
            "email": "allouette@example.com",
            "password": "123"
        }
        await client.post("/user/", json=user_data)

        # authenticate the test user and get the access token
        data = {
            "username": "all",
            "password": "123",
        }
        form_data = urlencode(data)
        response = await client.post(
            "/token",
            data=form_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"})
          
        # Get the token from the response
        user = await authenticate_user(data["username"], data["password"])
        access_token = create_access_token(
            data={"sub": user["username"]},
        )
        access_token = response.json()["access_token"]
        print(access_token)

        # Follow the redirect manually
        assert response.status_code == 307
        response = await client.post(response.headers["location"], json=data)
        print(response.text)
        print(response.json())
        print(response.headers)
        assert response.status_code == 200

        token = Token(**response.json())
        assert token.token_type == "bearer"
        assert token.access_token is not None 

        access_token = token.access_token
        headers={"Authorization": f"Bearer {access_token}"}
        robot_data = {
            "name": "beepboop",
            "serial": "1234",
            "username": "blood",
            "password": "secret11"
        }
        response = await client.post("/robots/", json=robot_data, headers=headers)

      
        try:
            response = await client.post("/robot/", json=robot_data, headers=headers)
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            print(f"HTTP error {exc.status_code}: {exc.message}")
            print(exc.request.headers)
            print(exc.request.body)
            print(exc.response.headers)
            print(exc.response.json())
            raise
        assert response.status_code == 200
        assert True

   

   













# Sans authentification***************************************
# def test_create_robot():
#     # create a test user withput token
#     user = User(
#         id="643ec23118c3b45bb2d90ad5",
#         username="ZTOP",
#         email="ztop@example.com",
#         firstname="ZZ",
#         lastname="ZZTOP"
#         )
#     # create a test robot
#     robot_data = {
#         "name": "beepboop",
#         "serial": "1234"
#         }
#     # send a POST request to the API with the test robot data
#     response = client.post("/robot/user/", json=robot_data)
#     # assert that the response status code is 200 OK
#     assert response.status_code == 405
#     # assert that the response data contains the added robot data and success message
#     assert response.json() == {"code":405, "data":robot_data,"detail": 'Method Not Allowed', "message": "Robot added successfully."}

# async def add_robot(robot_data: dict) -> dict:
#     robot = await robot_collection.insert_one(robot_data)
#     new_robot = await robot_collection.find_one({"_id": robot.inserted_id})
#     return RobotInDB(**new_robot).dict()

# def test_add_robot():
#     # create a test robot data
#     robot_data = {
#         "name": "beepboop",
#         "serial": "1234",
#         "user": "123456"
#     }
#     # add the test robot data to the database
#     new_robot = asyncio.run(add_robot(robot_data))
#     # update the robot_data with the generated _id
#     robot_data['_id'] = new_robot['_id']
#     # assert that the returned robot data matches the added robot data
#     assert new_robot == robot_data




# def test_get_robots():
#     robot_data = {
#         "_id": "643ec6cef0b9f29417506969",
#         "name": "beepboop",
#         "serial": "1234",
#         "user": "643ec23118c3b45bb2d90ad5"
#     }
#     user_id="idpekka"
#     # send a GET request to the API to retrieve the robots for the test user
#     response = client.get(f"/robot/{user_id}")
#     # assert that the response status code is 200 OK
#     assert response.status_code == 200
#     # assert that the response data contains the added robot data and success message
#     robot_data['id'] = response.json()['data'][0][0]['id']
#     expected_data = {"data": [[robot_data]], "message": "Robots data retrieved successfully.", "code":200}
#     assert response.json() == expected_data
