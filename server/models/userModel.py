from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class UserSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
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
                "firstname": "John",
                "lastname": "Doe",
                "username": "jdoe",
                "email": "jdoe@example.com",
                "password": "*****************",
            }
        }


class UpdateUserModel(BaseModel):
    firstname: Optional[str]
    lastname: Optional[str]
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "firstname": "Hugo",
                "lastname": "Poissonnier",
                "username": "HugoP",
                "email": "jdoe@example.com",
                "password": "*****************",
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
