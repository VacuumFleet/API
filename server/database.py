from bson import ObjectId
import motor.motor_asyncio
from decouple import config


ACCESS_TOKEN_EXPIRE_MINUTES="30"
ALGORITHM="HS256"
DATABASE_NAME="vacuumfleet"
MONGODB_URL="mongodb://localhost:27017"
SECRET="awesomesecretkey"

MONGODB_URL = config("MONGODB_URL")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
database = client.vacuumfleet
user_collection = database.get_collection("users")



def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "firstname": user["firstname"],
        "lastname": user["lastname"],
    }


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
        updated_user = await user_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_user:
            return True
        return False


# Delete a user from the database
async def delete_user(id: str):
    user = await user_collection.find_one({"_id": id})
    if user:
        await user_collection.delete_one({"_id": id})
        return True


robot_collection = database.get_collection("robot")


def robot_helper(robot) -> dict:
    return {
        "id": str(robot["_id"]),
        "name": robot["name"],
        "user": robot["user"],
        "serial": robot["serial"],
    }


async def add_robot(robot_data: dict) -> dict:
    robot = await robot_collection.insert_one(robot_data)
    new_robot = await robot_collection.find_one({"_id": robot.inserted_id})
    return robot_helper(new_robot)


async def retrieve_robots(user: str):
    robots = []
    async for robot in robot_collection.find({"user": user}):
        robots.append(robot_helper(robot))
    return robots
