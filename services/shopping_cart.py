from fastapi import HTTPException

from repositories.shopping_cart import ShoppingCartRepository
from schemas.common import APIResponse
from schemas.shopping_cart import CreateShoppingCart, AddToCart
from services.user import does_user_exist
from services.product import does_product_exist

shopping_cart_repository = ShoppingCartRepository()

async def create_shopping_cart(shopping_cart: CreateShoppingCart):
    if shopping_cart.user_id:
        await does_user_exist(str(shopping_cart.user_id))
    created_id = await shopping_cart_repository.create(shopping_cart, )
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

async def does_cart_exist(id: str):
    exists = await shopping_cart_repository.check_if_exists(id)
    if not exists:
        raise HTTPException(status_code=404, detail=APIResponse(code=404, message="Shopping Cart not found!").dict())
    return True

async def does_product_exist_in_cart(id: str, product_id: str, throw_if_exists = False):
    exists = await shopping_cart_repository.check_if_product_exists(id=id, product_id=product_id)
    if throw_if_exists and exists:
        raise HTTPException(status_code=400, detail=APIResponse(code=400, message="Product already in cart!").dict())
    if not throw_if_exists and not exists:
        raise HTTPException(status_code=404, detail=APIResponse(code=404, message="Product not in cart!").dict())
    return True

async def add_to_cart(id: str, request: AddToCart):
    await does_cart_exist(id)
    await does_product_exist(str(request.product_id))
    await does_product_exist_in_cart(id, str(request.product_id), throw_if_exists=True)
    added = await shopping_cart_repository.add_to_cart(id, request)
    if not added:
        raise HTTPException(status_code=500, detail=APIResponse(code=500, message="Adding to cart failed!").dict())
    return True