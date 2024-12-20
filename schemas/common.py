from typing import Optional

from pydantic import BaseModel, Field
from pyobjectID import PyObjectId, MongoObjectId


class APIResponse(BaseModel):
    code: int
    message: str

class OutboundModel(BaseModel):
    id: Optional[MongoObjectId] = Field(alias="_id", default=None)

class UpdateModel(BaseModel):
    id: PyObjectId = Field(alias="_id")