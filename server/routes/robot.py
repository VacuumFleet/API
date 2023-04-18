import logging
from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from server.database import (
    add_robot,
    retrieve_robots,
    retrieve_robots_user,
    update_robot_user,
)
from server.models.userModel import User
from server.models.robotModel import (
    ErrorResponseModel,
    ResponseModel,
    RobotInDB,
    Robot,
    RobotUpdateModel,
)
from server.routes.auth import get_current_user
from typing import Annotated

router = APIRouter()


@router.post("/", response_description="Robot data added into the database")
async def createRobot(user: Annotated[User, Depends(get_current_user)], robot_create: Robot = Body(...)):
    robot_create = robot_create.dict()
    robot_create["user"] = str(user.id)
    robot = RobotInDB(**robot_create)
    robot = jsonable_encoder(robot)

    new_robot = await add_robot(robot)
    return ResponseModel(new_robot, "Robot added successfully.")

@router.put("/{id}", response_description="Update robot")
async def updateRobot(id: str, user: Annotated[User, Depends(get_current_user)], robot_update: RobotUpdateModel = Body(...)):
    robot_update = {k: v for k, v in robot_update.dict().items() if v is not None}
    updated_robot = await update_robot_user(id, user, robot_update)
    if updated_robot:
        return ResponseModel(
            "Robot with ID: {} name update is successful".format(id),
            "Robot name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the robot data.",
    )

@router.get("/user", response_description="Retrieve all robots corresponding to a user")
async def getRobots(user: Annotated[User, Depends(get_current_user)]):
    robots = await retrieve_robots_user(str(user.id))
    if robots:
        return ResponseModel(robots, "Robots data retrieved successfully.")
    return ResponseModel(robots, "Empty list returned")
