from typing import Optional

from pydantic import EmailStr, BaseModel
from schemas.common import UpdateModel, OutboundModel


class User(BaseModel):
    name: str
    email: EmailStr

class UserOutbound(User, OutboundModel):
    pass

class UpdateUser(UpdateModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None