from typing import Optional, Any, List, TypeVar, Generic

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

class PaginationParams(BaseModel):
    page_no: int = 0
    page_size: int = 10

T = TypeVar('T')

class PaginatedData(BaseModel, Generic[T]):
    data: List[T]
    total_count: int
    page_no: int
    page_size: int