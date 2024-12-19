from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from pyobjectID import MongoObjectId


class User(BaseModel):
    id: Optional[MongoObjectId] = Field(alias="_id", default=None)
    name: str
    email: EmailStr
