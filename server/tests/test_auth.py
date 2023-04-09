import pytest
from fastapi import HTTPException
from unittest.mock import AsyncMock, patch

from server.routes.auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_password_hash,
    get_user,
    verify_password,
)

pytest_plugins = ('pytest_asyncio',)

@pytest.fixture
def mock_db():
    return {
        "users": [
            {
                "_id": "mock_id",
                "username": "mock_username",
                "hashed_pass": get_password_hash("mock_password"),
            },
        ],
    }


@pytest.mark.asyncio
async def test_get_user_found(mock_db):
    db_mock = AsyncMock(**mock_db)
    result = await get_user("mock_id", db=db_mock)
    assert result["_id"] == "mock_id"
    assert result["username"] == "mock_username"
    assert result["hashed_pass"] == get_password_hash("mock_password")


@pytest.mark.asyncio
async def test_get_user_not_found(mock_db):
    db_mock = AsyncMock(**mock_db)
    result = await get_user("unknown_id", db=db_mock)
    assert result is None


@pytest.mark.asyncio
async def test_authenticate_user_success(mock_db):
    db_mock = AsyncMock(**mock_db)
    result = await authenticate_user("mock_username", "mock_password", db=db_mock)
    assert result["_id"] == "mock_id"
    assert result["username"] == "mock_username"
    assert result["hashed_pass"] == get_password_hash("mock_password")


@pytest.mark.asyncio
async def test_authenticate_user_user_not_found(mock_db):
    db_mock = AsyncMock(**mock_db)
    result = await authenticate_user("unknown_username", "mock_password", db=db_mock)
    assert result is False


@pytest.mark.asyncio
async def test_authenticate_user_wrong_password(mock_db):
    db_mock = AsyncMock(**mock_db)
    result = await authenticate_user("mock_username", "wrong_password", db=db_mock)
    assert result is False


def test_create_access_token():
    data = {"sub": "mock_username"}
    access_token = create_access_token(data)
    assert isinstance(access_token, str)


@pytest.mark.asyncio
async def test_get_current_user_success(mock_db):
    token = create_access_token({"sub": "mock_username"})
    db_mock = AsyncMock(**mock_db)
    result = await get_current_user(token=token.decode(), db=db_mock)
    assert result["_id"] == "mock_id"
    assert result["username"] == "mock_username"
    assert result["hashed_pass"] == get_password_hash("mock_password")


@pytest.mark.asyncio
async def test_get_current_user_missing_token(mock_db):
    db_mock = AsyncMock(**mock_db)
    with pytest.raises(HTTPException) as exc:
        await get_current_user(db=db_mock)
    assert exc.value.status_code == 401