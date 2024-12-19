from pydantic import BaseModel

class APIResponse(BaseModel):
    code: int
    message: str