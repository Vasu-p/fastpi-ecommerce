from typing import Optional

from pydantic import BaseModel, Field
from pyobjectID import PyObjectId, MongoObjectId


class APIResponse(BaseModel):
    code: int
    message: str

class DocumentCreate(BaseModel):
    id: Optional[MongoObjectId] = Field(alias="_id", default=None)

class DocumentUpdate(BaseModel):
    id: PyObjectId = Field(alias="_id")