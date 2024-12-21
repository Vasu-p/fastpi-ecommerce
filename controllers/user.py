from typing import List

from fastapi import APIRouter, Depends

import services.user as user_service
import services.shopping_cart as shopping_cart_service
from schemas.common import APIResponse, PaginationParams, PaginatedData
from schemas.shopping_cart import ShoppingCartOutbound
from schemas.user import UpdateUser, UserOutbound, CreateUser, UserRegistrationResponse

router = APIRouter()


@router.post("/", response_model=APIResponse)
async def register_user(user: CreateUser):
    user_registration: UserRegistrationResponse = await user_service.register_user(user)
    return APIResponse(code=200, message="User registered successful!",
                       detail={"_id": user_registration.user_id, "shopping_cart_id": user_registration.shopping_cart_id}).dict()

@router.get("/all", response_model=List[UserOutbound])
async def get_users():
    return await user_service.get_all_users()

@router.get("/", response_model=PaginatedData[UserOutbound])
async def get_users_paginated(page_params: PaginationParams = Depends()):
    return await user_service.get_users_paginated(page_params)

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

@router.get("/{user_id}/shopping-cart", response_model=ShoppingCartOutbound)
async def get_shopping_cart_for_user(user_id: str):
    return await shopping_cart_service.get_shopping_cart_by_user_id(user_id)