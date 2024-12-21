from typing import Optional

from pydantic import EmailStr, BaseModel
from pyobjectID import MongoObjectId

from schemas.common import UpdateModel, OutboundModel


class User(BaseModel):
    name: str
    email: EmailStr

class CreateUser(User):
    pass

class UserOutbound(User, OutboundModel):
    pass

class UpdateUser(UpdateModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class UserRegistrationResponse(BaseModel):
    user_id: str
    shopping_cart_id: str