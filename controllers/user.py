from typing import List

from fastapi import APIRouter

from schemas.common import APIResponse
from schemas.user import User, UpdateUser
import services.user as user_service

router = APIRouter()


@router.post("/", response_model=APIResponse)
async def register_user(user: User):
    await user_service.register_user(user)
    return APIResponse(code=200, message="Registration Successful!").dict()

@router.get("/", response_model=List[User])
async def get_users():
    return await user_service.get_all_users()

@router.get("/{user_id}", response_model=User)
async def get_user_by_id(user_id: str):
    return await user_service.get_user_by_id(user_id)

@router.patch("/", response_model=User)
async def update_user(user: UpdateUser):
    return await user_service.update_user(user)
