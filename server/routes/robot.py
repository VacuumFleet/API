import asyncio
from typing import Annotated

from fastapi import APIRouter, Body, Depends, WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder
from websockets.exceptions import ConnectionClosedOK

from server.database import (
    add_robot,
    retrieve_robot,
    retrieve_robots_user,
    update_robot_user,
)
from server.models.robotModel import (
    ErrorResponseModel,
    ResponseModel,
    Robot,
    RobotInDB,
    RobotUpdateModel,
)
from server.models.userModel import User
from server.routes.auth import get_current_user

router = APIRouter()

eventQueue = asyncio.Queue()


@router.post("/", response_description="Robot data added into the database")
async def createRobot(
    user: Annotated[User, Depends(get_current_user)], robot_create: Robot = Body(...)
):
    robot_create = robot_create.dict()
    robot_create["user"] = str(user.id)
    robot = RobotInDB(**robot_create)
    robot = jsonable_encoder(robot)

    new_robot = await add_robot(robot)
    return ResponseModel(new_robot, "Robot added successfully.")


@router.put("/{id}", response_description="Update robot")
async def updateRobot(
    id: str,
    user: Annotated[User, Depends(get_current_user)],
    robot_update: RobotUpdateModel = Body(...),
):
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


@router.get("/{id}/start", response_description="Start robot")
async def startRobot(id: str, user: Annotated[User, Depends(get_current_user)]):
    robot = await retrieve_robot(id)
    if robot:
        if robot.user == str(user.id):
            await eventQueue.put(f"{robot.serial} START")
            return ResponseModel(
                "Robot with ID: {} start is successful".format(id),
                "Robot started successfully",
            )
        else:
            return ErrorResponseModel(
                "An error occurred", 401, "You do not own this robot."
            )

    return ErrorResponseModel(
        "An error occurred", 500, "There was an error starting the robot."
    )


@router.get("/{id}/stop", response_description="Stop robot")
async def stopRobot(id: str, user: Annotated[User, Depends(get_current_user)]):
    robot = await retrieve_robot(id)
    if robot:
        if robot.user == str(user.id):
            await eventQueue.put(f"{robot.serial} STOP")
            return ResponseModel(
                "Robot with ID: {} stop is successful".format(id),
                "Robot stopped successfully",
            )
        else:
            return ErrorResponseModel(
                "An error occurred", 401, "You do not own this robot."
            )

    return ErrorResponseModel(
        "An error occurred", 500, "There was an error stopping the robot."
    )


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except ConnectionClosedOK:
                manager.disconnect(connection)


manager = ConnectionManager()


@router.websocket("/events/ws")
async def robotEventsWs(websocket: WebSocket):
    await manager.connect(websocket)
    while True:
        try:
            event = await eventQueue.get()
            await manager.broadcast(event)
        except WebSocketDisconnect:
            manager.disconnect(websocket)
