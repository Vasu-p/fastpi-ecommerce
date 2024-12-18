from typing import List

from fastapi import APIRouter

from repositories.user import create_user, get_all_users
from schemas.user import User

router = APIRouter()


@router.post("/")
async def register_user(user: User):
    id = await create_user(user)
    if id != None:
        return { "code": 200 }
    else:
        return { "code": 500 }

@router.get("/", response_model=List[User])
async def get_users():
    users = await get_all_users()
    return users
