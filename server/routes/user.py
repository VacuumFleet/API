from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from decouple import config
from server.database import (
    add_user,
    delete_user,
    retrieve_user,
    retrieve_users,
    update_user,
)
from server.models.userModel import (
    ErrorResponseModel,
    ResponseModel,
    UserSchema,
    UpdateUserModel,
)

ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES")

router = APIRouter()


@router.post("/", response_description="User data added into the database")
async def createUser(user: UserSchema = Body(...)):
    user = jsonable_encoder(user)
    new_user = await add_user(user)
    return ResponseModel(new_user, "User added successfully.")


@router.get("/", response_description="Retrieve all users data")
async def getUsers():
    users = await retrieve_users()
    if users:
        return ResponseModel(users, "Users data retrieved successfully.")
    return ResponseModel(users, "Empty list returned")


@router.get("/{id}", response_description="User data retrieve")
async def getUser(id):
    user = await retrieve_user(id)
    if user:
        return ResponseModel(user, "User data retrieved successfully.")
    return ErrorResponseModel("An error occurred", 400, "User doesn't exist.")


@router.put("/{id}", response_description="Update user")
async def updateUser(id: str, user: UpdateUserModel = Body(...)):
    user = {k: v for k, v in user.dict().items() if v is not None}
    updated_user = await update_user(id, user)
    if updated_user:
        return ResponseModel(
            "User with ID: {} name update is successful".format(id),
            "User name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the user data.",
    )


@router.delete("/{id}", response_description="User data deleted from the database")
async def delete_user_data(id: str):
    deleted_user = await delete_user(id)
    if deleted_user:
        return ResponseModel(
            "User with ID: {} removed".format(id), "User deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "User with id {0} doesn't exist".format(id)
    )
