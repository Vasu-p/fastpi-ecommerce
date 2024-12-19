from fastapi import HTTPException

import repositories.user as user_repository
from schemas.common import APIResponse
from schemas.user import User, UpdateUser


async def register_user(user: User):
    created_id = await user_repository.create(user)
    if not created_id:
        raise HTTPException(status_code=500, detail=APIResponse(code=500, message="User Registration Failed!").dict())
    return created_id

async def get_all_users():
    return await user_repository.get_all()

async def get_user_by_id(id: str):
    user = await user_repository.get_by_id(id)
    if not user:
        raise HTTPException(status_code=404, detail=APIResponse(code=404, message="User not found!").dict())
    return user

async def update_user(user: UpdateUser):
    user = await user_repository.update_user(user)
    print(f"user is ${user}")
    if not user:
        raise HTTPException(status_code=404, detail=APIResponse(code=404, message="User not found!").dict())
    return user