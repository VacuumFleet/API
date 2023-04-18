from fastapi import FastAPI
from dotenv import load_dotenv
import pytz
from server.routes.user import router as UserRouter
from server.routes.auth import router as TokenRouter
from server.routes.robot import router as RobotRouter
import logging
import motor.motor_asyncio
from decouple import config

FORMAT = "%(levelname)s:%(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG)


load_dotenv()

timezone_paris = pytz.timezone("Europe/Paris")

app = FastAPI(
    title="vacuumfleet-api",
    description="Cette API collecte diverses données des robots et régit les interactions entre app mobile et robot",
    version="0.0.2",
    license_info={"name": "The MIT License (MIT)", "url": "https://mit-license.org/"},
)

app.include_router(UserRouter, tags=["User"], prefix="/user")

app.include_router(TokenRouter, tags=["Token"], prefix="/token")

app.include_router(RobotRouter, tags=["Robot"], prefix="/robot")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
