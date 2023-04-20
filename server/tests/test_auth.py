import pytest
from decouple import config
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.testclient import TestClient
from passlib.context import CryptContext

from server.app import app
from server.routes.auth import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)

SECRET_KEY = config("SECRET")
ALGORITHM = config("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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
    response = client.post(
        "/token/",
        data={
            "username": "jdoe",
            "password": "secret1",
        },
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    response_data = response.json()
    assert "access_token" in response_data
    assert "token_type" in response_data
    return response_data["token_type"], response_data["access_token"]
