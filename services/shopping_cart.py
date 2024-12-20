from fastapi import HTTPException

from repositories.shopping_cart import ShoppingCartRepository
from repositories.user import UserRepository
from schemas.common import APIResponse
from schemas.shopping_cart import CreateShoppingCart

shopping_cart_repository = ShoppingCartRepository()
user_repository = UserRepository()

async def create_shopping_cart(shopping_cart: CreateShoppingCart):
    if shopping_cart.user_id:
        user = await user_repository.get_by_id(shopping_cart.user_id)
        if not user:
            raise HTTPException(status_code=404, detail=APIResponse(code=404, message="User not found!").dict())
    created_id = await shopping_cart_repository.create(shopping_cart)
    if not created_id:
        raise HTTPException(status_code=500, detail=APIResponse(code=500, message="Shopping Cart creation Failed!").dict())
    return created_id

async def get_shopping_cart_by_id(id: str):
    shopping_cart = await shopping_cart_repository.get_by_id(id)
    if not shopping_cart:
        raise HTTPException(status_code=404, detail=APIResponse(code=404, message="Shopping Cart not found!").dict())
    return shopping_cart

async def delete_shopping_cart(id: str):
    deleted = await shopping_cart_repository.delete(id)
    if not deleted:
        raise HTTPException(status_code=404, detail=APIResponse(code=404, message="Shopping Cart not found!").dict())
    return True