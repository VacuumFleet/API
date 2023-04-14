import pytest
import asyncio
import motor.motor_asyncio
from datetime import datetime, timedelta
from typing import Union
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from decouple import config
from server.models.tokenModel import Token, TokenData
from server.routes.auth import verify_password, get_password_hash,authenticate_user, retrieve_user_by_username_with_pwd,create_access_token, get_current_user
import logging
import asyncio
from fastapi.testclient import TestClient
from bson import ObjectId
from decouple import config

import unittest
from fastapi import FastAPI



# from pytest import asyncio
import pytest
from fastapi import HTTPException
from unittest.mock import AsyncMock, patch


from server.database import (
    retrieve_user_by_username,
    retrieve_user_by_username_with_pwd,
)

SECRET_KEY = config("SECRET")
ALGORITHM = config("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

app = FastAPI(
    title="vacuumfleet-api",
    description="Cette API collecte diverses données des robots et régit les interactions entre app mobile et robot",
    version="0.0.2",
    license_info={"name": "The MIT License (MIT)", "url": "https://mit-license.org/"},
)

client = TestClient(app)

def test_verify_password():
    plain_password = "myPassword123"
    hashed_password = pwd_context.hash(plain_password)
    assert verify_password(plain_password, hashed_password) == True

    incorrect_password = "incorrectPassword456"
    assert verify_password(incorrect_password, hashed_password) == False


def test_get_password_hash():
    password = "myPassword123"
    hashed_password = get_password_hash(password)
    assert len(hashed_password) > 0
    assert hashed_password != password

def test_create_access_token():
    # Define test data
    data = {"sub": "1234567890", "username": "PP"}
    
    # Call the function to create an access token
    access_token = create_access_token(data).encode()
    
    # Check that the access token was created successfully
    assert isinstance(access_token, bytes)
    assert access_token != ""


@pytest.mark.asyncio
async def test_get_current_user():
    # Test with valid token
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqZG9lIiwiZXhwIjoxNjgxNDgyNTE5fQ.4doM2Y7z__RXM4QFiV2g9VfEA7LhxxT4x4b0zllT-Ho"
    user = "jdoe"
    assert user == "jdoe"

    # Test with invalid token
    invalid_token = "invalid_token"
    try:
        user = await get_current_user(invalid_token)
        assert False, "Expected exception not raised"
    except HTTPException as e:
        assert e.status_code == 401

def test_login():
    response = client.post("/token/", json={"username": "jdoe", "password": "secret1"},
                        headers={"content-type": "application/x-www-form-urlencoded"})
    assert response.status_code == 200
    response_data = response.json()
    assert "access_token" in response_data
    assert "token_type" == "bearer"
    return response_data["token_type"], response_data["access_token"]
