from bson import ObjectId
from dotenv import load_dotenv
import motor.motor_asyncio
from decouple import config

MONGODB_URL = config("MONGODB_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

database = client.vacuumfleet

user_collection = database.get_collection("user")

def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "firstname": user["firstname"],
        "lastname": user["lastname"]
    }

def user_helper_with_pwd(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "firstname": user["firstname"],
        "lastname": user["lastname"],
        "password": user["password"]
    }

# Retrieve all users present in the database
async def retrieve_users():
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    return users


# Add a new user into to the database
async def add_user(user_data: dict) -> dict:
    user = await user_collection.insert_one(user_data)
    new_user = await user_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)


# Retrieve a user with a matching ID
async def retrieve_user(id: str) -> dict:
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)

# Retrieve a user with a matching Username
async def retrieve_user_by_username(username: str) -> dict:
    user = await user_collection.find_one({"username": username})
    if user:
        return user_helper(user)

# Retrieve a user with a matching Username with pwd
async def retrieve_user_by_username_with_pwd(username: str) -> dict:
    user = await user_collection.find_one({"username": username})
    if user:
        return user_helper_with_pwd(user)

# Update a user with a matching ID
async def update_user(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        updated_user = await user_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_user:
            return True
        return False


# Delete a user from the database
async def delete_user(id: str):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        await user_collection.delete_one({"_id": ObjectId(id)})
        return True
