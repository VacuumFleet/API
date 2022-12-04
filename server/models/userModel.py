from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, SecretStr
from typing import (
    Optional
)

class UserSchema(BaseModel):
    firstname: str = Field(...)
    lastname: str = Field(...)
    username: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "firstname": "Hugo",
                "lastname" : "Poissonnier",
                "username": "HugoP",
                "email": "jdoe@example.com",
                "password": "*****************"
            }
        }

class UserSchemaWithoutPwd(BaseModel):
    firstname: str = Field(...)
    lastname: str = Field(...)
    username: str = Field(...)
    email: EmailStr = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "firstname": "Hugo",
                "lastname" : "Poissonnier",
                "username": "HugoP",
                "email": "jdoe@example.com",
            }
        }

class UpdateUserModel(BaseModel):
    firstname:  Optional[str]
    lastname:  Optional[str]
    username:  Optional[str]
    email:  Optional[EmailStr]
    password: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "firstname": "Hugo",
                "lastname" : "Poissonnier",
                "username": "HugoP",
                "email": "jdoe@example.com",
                "password": "*****************"
            }
        }

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {}
    return {"error": error, "code": code, "message": message}