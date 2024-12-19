from typing import List

from fastapi import APIRouter

from schemas.common import APIResponse
from schemas.product import Product, UpdateProduct
import services.product as product_service

router = APIRouter()


# Endpoint to register a new product
@router.post("/", response_model=APIResponse)
async def register_product(product: Product):
    await product_service.register_product(product)
    return APIResponse(code=200, message="Product registered successfully!").dict()


# Endpoint to get all products
@router.get("/", response_model=List[Product])
async def get_products():
    return await product_service.get_all_products()


# Endpoint to get a specific product by its ID
@router.get("/{product_id}", response_model=Product)
async def get_product_by_id(product_id: str):
    return await product_service.get_product_by_id(product_id)


# Endpoint to update a product
@router.patch("/", response_model=Product)
async def update_product(product: UpdateProduct):
    return await product_service.update_product(product)


# Endpoint to delete a product
@router.delete("/{product_id}", response_model=APIResponse)
async def delete_product(product_id: str):
    await product_service.delete_product(product_id)
    return APIResponse(code=200, message="Product deleted successfully!").dict()
