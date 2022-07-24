import os
from datetime import datetime

import motor.motor_asyncio
import pytz
from dotenv import load_dotenv
from fastapi import FastAPI, Response, status
from pydantic import BaseModel, Field

load_dotenv()

timezone_paris = pytz.timezone('Europe/Paris')

api = FastAPI(
    title='vacuumfleet-api',
    description="Cette API collecte diverses données des robots et régit les interactions entre app mobile et robot",
    version='0.0.1',
    license_info={
        'name':'The MIT License (MIT)', 
        'url' : 'https://mit-license.org/'
    },
)

mongo_client = motor.motor_asyncio.AsyncIOMotorClient(os.environ['MONGODB_URL'])

