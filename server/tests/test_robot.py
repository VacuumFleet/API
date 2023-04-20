from urllib.parse import urlencode

import httpx
import pytest
from decouple import config
from fastapi.security import OAuth2PasswordBearer
from fastapi.testclient import TestClient
from passlib.context import CryptContext

from server.app import app
from server.models.tokenModel import Token
from server.routes.auth import authenticate_user, create_access_token

SECRET_KEY = config("SECRET")
ALGORITHM = config("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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
            "password": "123",
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
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

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
        headers = {"Authorization": f"Bearer {access_token}"}
        robot_data = {
            "name": "beepboop",
            "serial": "1234",
            "username": "blood",
            "password": "secret11",
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
