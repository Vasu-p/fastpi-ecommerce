from typing import Optional

from pydantic import EmailStr
from schemas.common import DocumentUpdate, DocumentCreate


class User(DocumentCreate):
    name: str
    email: EmailStr

class UpdateUser(DocumentUpdate):
    name: Optional[str] = None
    email: Optional[EmailStr] = None