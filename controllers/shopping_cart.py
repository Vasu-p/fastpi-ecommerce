from fastapi import APIRouter, HTTPException
from schemas.common import APIResponse
from schemas.shopping_cart import CreateShoppingCart, ShoppingCartOutbound, AddToCart, RemoveFromCart
import services.shopping_cart as shopping_cart_service

router = APIRouter()


@router.post("/", response_model=APIResponse)
async def create_cart(cart: CreateShoppingCart):
    # Call the service to register the cart
    shopping_cart_id = await shopping_cart_service.create_shopping_cart(cart)
    return APIResponse(code=200, message="Shopping cart created successfully!", detail={"_id": shopping_cart_id}).dict()

@router.get("/{cart_id}", response_model=ShoppingCartOutbound)
async def get_cart_by_id(cart_id: str):
    # Fetch the cart by ID, if not found, raise HTTP 404
    cart = await shopping_cart_service.get_shopping_cart_by_id(cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Shopping cart not found")
    return cart

@router.delete("/{cart_id}", response_model=APIResponse)
async def delete_cart(cart_id: str):
    # Delete the shopping cart
    deleted = await shopping_cart_service.delete_shopping_cart(cart_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Shopping cart not found")
    return APIResponse(code=200, message="Shopping cart deleted successfully!").dict()

@router.post("/{cart_id}/add", response_model=APIResponse)
async def add_to_cart(cart_id: str, request: AddToCart):
    await shopping_cart_service.add_to_cart(cart_id, request)
    return APIResponse(code=200, message="Product added successfully!").dict()

@router.post("/{cart_id}/remove", response_model=APIResponse)
async def remove_from_cart(cart_id: str, request: RemoveFromCart):
    await shopping_cart_service.remove_from_cart(cart_id, request)
    return APIResponse(code=200, message="Product removed successfully!").dict()

@router.post("/{cart_id}/clear", response_model=APIResponse)
async def clear_cart(cart_id: str):
    await shopping_cart_service.clear_cart(cart_id)
    return APIResponse(code=200, message="Cart cleared successfully!").dict()