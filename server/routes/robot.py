from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from server.database import (
    add_robot,
    retrieve_robots,
)
from server.models.robotModel import (
    ResponseModel,
    RobotModel,
)

router = APIRouter()


@router.post("/", response_description="Robot data added into the database")
async def createRobot(robot: RobotModel = Body(...)):
    robot = jsonable_encoder(robot)
    new_robot = await add_robot(robot)
    return ResponseModel(new_robot, "Robot added successfully.")


@router.get(
    "/{user_id}", response_description="Retrieve all robots corresponding to a user"
)
async def getRobots(user_id):
    robots = await retrieve_robots(user_id)
    if robots:
        return ResponseModel(robots, "Robots data retrieved successfully.")
    return ResponseModel(robots, "Empty list returned")
