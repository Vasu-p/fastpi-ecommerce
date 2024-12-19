from fastapi import HTTPException

import repositories.user as user_repository
from schemas.common import APIResponse
from schemas.user import User


async def register_user(user: User):
    created_id = await user_repository.create(user)
    if not created_id:
        raise HTTPException(status_code=500, detail=APIResponse(code=500, message="User Registration Failed!").dict())
    return created_id

async def get_all_users():
    return await user_repository.get_all()