from fastapi import HTTPException

from repositories.shopping_cart import ShoppingCartRepository
from repositories.user import UserRepository
from schemas.common import APIResponse
from schemas.user import CreateUser, UpdateUser, UserRegistrationResponse
from schemas.shopping_cart import CreateShoppingCart

user_repository = UserRepository()
shopping_cart_repository = ShoppingCartRepository()

async def register_user(user: CreateUser):
    user_id = await user_repository.create(document=user)
    if not user_id:
        raise HTTPException(status_code=500, detail=APIResponse(code=500, message="User registration Failed!").dict())
    shopping_cart_id = await shopping_cart_repository.create(CreateShoppingCart(user_id=user_id))
    if not shopping_cart_id:
        # delete the created user
        # ideally not needed if we have transactions
        # bug mongodb doesnt support transaction in standalone mode
        await delete_user(user_id)
        raise HTTPException(status_code=500, detail=APIResponse(code=500, message="Cannot create cart of user. User registration Failed!").dict())
    return UserRegistrationResponse(user_id=user_id, shopping_cart_id=shopping_cart_id)

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

async def does_user_exist(id: str):
    exists = await user_repository.check_if_exists(id)
    if not exists:
        raise HTTPException(status_code=404, detail=APIResponse(code=404, message="User not found!").dict())
    return True