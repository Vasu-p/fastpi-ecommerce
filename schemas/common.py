from typing import Optional, Any

from pydantic import BaseModel, Field
from pyobjectID import PyObjectId, MongoObjectId


class APIResponse(BaseModel):
    code: int
    message: str
    detail: Any = None

class OutboundModel(BaseModel):
    id: Optional[MongoObjectId] = Field(alias="_id", default=None)

class UpdateModel(BaseModel):
    id: PyObjectId = Field(alias="_id")