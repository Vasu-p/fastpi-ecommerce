from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from pyobjectID import MongoObjectId
from schemas.common import DocumentUpdate


class User(BaseModel):
    id: Optional[MongoObjectId] = Field(alias="_id", default=None)
    name: str
    email: EmailStr

class UpdateUser(DocumentUpdate):
    name: Optional[str] = None
    email: Optional[EmailStr] = None