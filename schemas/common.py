from pydantic import BaseModel, Field
from pyobjectID import PyObjectId


class APIResponse(BaseModel):
    code: int
    message: str

class DocumentUpdate(BaseModel):
    id: PyObjectId = Field(alias="_id")