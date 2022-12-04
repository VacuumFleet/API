from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, SecretStr
from typing import (
    Optional, Union
)


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None


