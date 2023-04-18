import asyncio
import unittest
import motor.motor_asyncio
from server.database import add_user, retrieve_user
import pytest

from server.models.userModel import UserInDB

async def async_open_db():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["vacuumfleet"]
    return db

@pytest.mark.asyncio
async def test_add_user():
    # Créer un utilisateur pour le test
    user = UserInDB(
        firstname="John",
        lastname="Doe",
        email="jdoe@mail.com",
        username="jdoe",
        password="fakehashedsecret",
    )
    
   # Ajouter l'utilisateur à la base de données
    async with async_open_db() as client:
        new_user = await add_user(client, user.dict())

    # Récupérer l'utilisateur depuis la base de données
    async with async_open_db() as client:
        db_user = await retrieve_user(client, new_user["_id"])

    # Vérifier que l'utilisateur ajouté correspond à l'utilisateur récupéré
    assert db_user == new_user