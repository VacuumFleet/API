import logging

import motor.motor_asyncio
from bson import ObjectId
from decouple import config

from server.models.robotModel import RobotInDB
from server.models.userModel import User, UserInDB

ACCESS_TOKEN_EXPIRE_MINUTES = "30"
ALGORITHM = "HS256"
DATABASE_NAME = config("DATABASE_NAME")
MONGODB_URL = config("MONGODB_URL")
SECRET = config("SECRET")

MONGODB_URL = config("MONGODB_URL")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
database = client.by6n3mnrj30iuodgptgs
user_collection = database.get_collection("users")
robot_collection = database.get_collection("robot")


def user_helper(user) -> UserInDB:
    return UserInDB(**user)


def user_helper_with_pwd(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "firstname": user["firstname"],
        "lastname": user["lastname"],
        "password": user["password"],
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
    user = await user_collection.find_one({"_id": id})
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
    user = await user_collection.find_one({"_id": id})
    if user:
        updated_user = await user_collection.update_one({"_id": id}, {"$set": data})
        if updated_user:
            return True
        return False
    else:
        return False


# Delete a user from the database
async def delete_user(id: str):
    user = await user_collection.find_one({"_id": id})
    if user:
        await user_collection.delete_one({"_id": id})
        return True


robot_collection = database.get_collection("robot")


def robot_helper(robot) -> RobotInDB:
    return RobotInDB(**robot)


async def add_robot(robot_data: dict) -> dict:
    robot = await robot_collection.insert_one(robot_data)
    new_robot = await robot_collection.find_one({"_id": robot.inserted_id})
    return robot_helper(new_robot)


async def retrieve_robots_user(user: str):
    robots = []
    async for robot in robot_collection.find({"user": user}):
        robots.append(robot_helper(robot))
    return robots


async def retrieve_robot(id: str):
    robot = await robot_collection.find_one({"_id": id})
    if robot:
        return robot_helper(robot)


async def update_robot_user(id: str, user: User, data: dict):
    if len(data) < 1:
        return False
    robot = await robot_collection.find_one({"_id": id, "user": str(user.id)})
    if robot:
        updated_robot = await robot_collection.update_one({"_id": id}, {"$set": data})
        if updated_robot:
            return True
        return False
    else:
        return False
