from fastapi import HTTPException

from repositories.shopping_cart import ShoppingCartRepository
from schemas.common import APIResponse
from schemas.shopping_cart import CreateShoppingCart, AddToCart, RemoveFromCart
from services.user import does_user_exist
from services.product import does_product_exist

shopping_cart_repository = ShoppingCartRepository()

async def create_shopping_cart(shopping_cart: CreateShoppingCart):
    if shopping_cart.user_id:
        await does_user_exist(str(shopping_cart.user_id))
    shopping_cart_for_user = await shopping_cart_repository.get_by_user_id(shopping_cart.user_id)
    if shopping_cart_for_user:
        raise HTTPException(status_code=400, detail=APIResponse(code=400, message="Shopping Cart already exists for the user!").dict())
    created_id = await shopping_cart_repository.create(shopping_cart)
    if not created_id:
        raise HTTPException(status_code=500, detail=APIResponse(code=500, message="Shopping Cart creation Failed!").dict())
    return created_id

async def get_shopping_cart_by_id(id: str):
    shopping_cart = await shopping_cart_repository.get_by_id(id)
    if not shopping_cart:
        raise HTTPException(status_code=404, detail=APIResponse(code=404, message="Shopping Cart not found!").dict())
    return _compute_cart_amounts(shopping_cart)

async def get_shopping_cart_by_user_id(user_id: str):
    await does_user_exist(user_id)
    shopping_cart = await shopping_cart_repository.get_by_user_id(user_id)
    if not shopping_cart:
        raise HTTPException(status_code=404, detail=APIResponse(code=404, message="Shopping Cart not found!").dict())
    return _compute_cart_amounts(shopping_cart)

async def delete_shopping_cart(id: str):
    user_associated = await shopping_cart_repository.check_if_user_associated(id)
    if user_associated:
        raise HTTPException(status_code=400, detail=APIResponse(code=400, message="Cannot delete the only user cart!").dict())
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

async def remove_from_cart(id: str, request: RemoveFromCart):
    await does_cart_exist(id)
    await does_product_exist_in_cart(id, str(request.product_id))
    removed = await shopping_cart_repository.remove_from_cart(id, request)
    if not removed:
        raise HTTPException(status_code=500, detail=APIResponse(code=500, message="Removing from cart failed!").dict())
    return True

async def clear_cart(id: str):
    await does_cart_exist(id)
    cleared = await shopping_cart_repository.clear_cart(id)
    if not cleared:
        raise HTTPException(status_code=500, detail=APIResponse(code=500, message="Clearing cart failed!").dict())
    return True

def _compute_cart_amounts(cart):
    product_map = {}
    for product in cart["products"]:
        product_map[product["_id"]] = product
    cart_total = 0.0
    for item in cart["items"]:
        item["total_price"] = item["quantity"] * product_map[item["product_id"]]["price"]
        cart_total += item["total_price"]
    cart["total_price"] = cart_total
    return cart