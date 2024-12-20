from typing import List

from fastapi import APIRouter

from schemas.common import APIResponse
from schemas.user import UpdateUser, UserOutbound, CreateUser
import services.user as user_service

router = APIRouter()


@router.post("/", response_model=APIResponse)
async def register_user(user: CreateUser):
    await user_service.register_user(user)
    return APIResponse(code=200, message="User registered successful!").dict()

@router.get("/", response_model=List[UserOutbound])
async def get_users():
    return await user_service.get_all_users()

@router.get("/{user_id}", response_model=UserOutbound)
async def get_user_by_id(user_id: str):
    return await user_service.get_user_by_id(user_id)

@router.patch("/", response_model=UserOutbound)
async def update_user(user: UpdateUser):
    return await user_service.update_user(user)

@router.delete("/{user_id}", response_model=APIResponse)
async def delete_user(user_id: str):
    await user_service.delete_user(user_id)
    return APIResponse(code=200, message="User deleted successful!").dict()