from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from pyobjectID import MongoObjectId, PyObjectId


class User(BaseModel):
    id: Optional[MongoObjectId] = Field(alias="_id", default=None)
    name: str
    email: EmailStr

class UpdateUser(BaseModel):
    id: PyObjectId = Field(alias="_id")
    name: Optional[str] = None
    email: Optional[EmailStr] = None