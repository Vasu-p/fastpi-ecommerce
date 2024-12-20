from fastapi import HTTPException

from repositories.user import UserRepository
from schemas.common import APIResponse
from schemas.user import CreateUser, UpdateUser

user_repository = UserRepository()


async def register_user(user: CreateUser):
    created_id = await user_repository.create(user)
    if not created_id:
        raise HTTPException(status_code=500, detail=APIResponse(code=500, message="User registration Failed!").dict())
    return created_id

async def get_all_users():
    return await user_repository.get_all()

async def get_user_by_id(id: str):
    user = await user_repository.get_by_id(id)
    if not user:
        raise HTTPException(status_code=404, detail=APIResponse(code=404, message="User not found!").dict())
    return user

async def update_user(user: UpdateUser):
    user = await user_repository.update(user)
    if not user:
        raise HTTPException(status_code=404, detail=APIResponse(code=404, message="User not found!").dict())
    return user

async def delete_user(id: str):
    deleted = await user_repository.delete(id)
    if not deleted:
        raise HTTPException(status_code=404, detail=APIResponse(code=404, message="User not found!").dict())
    return True