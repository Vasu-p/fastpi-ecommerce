from enum import Enum
from typing import Optional, Any, List, TypeVar, Generic

from pydantic import BaseModel, Field
from pygments.lexers import asc
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

class SortDirEnum(str, Enum):
    ASC = "asc"
    DESC = "desc"
    def get_mongodb_dir(self):
        return 1 if self == SortDirEnum.ASC else -1

class SortParams(BaseModel):
    sort_by: str = "_id"
    sort_dir: SortDirEnum = SortDirEnum.ASC