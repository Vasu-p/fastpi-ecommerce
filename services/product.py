from fastapi import HTTPException

from repositories.product import ProductRepository
from schemas.common import APIResponse
from schemas.product import Product, UpdateProduct

product_repository = ProductRepository()


async def register_product(product: Product):
    created_id = await product_repository.create(product)
    if not created_id:
        raise HTTPException(status_code=500, detail=APIResponse(code=500, message="Product registration Failed!").dict())
    return created_id

async def get_all_products():
    return await product_repository.get_all()

async def get_product_by_id(id: str):
    product = await product_repository.get_by_id(id)
    if not product:
        raise HTTPException(status_code=404, detail=APIResponse(code=404, message="Product not found!").dict())
    return product

async def update_product(product: UpdateProduct):
    product = await product_repository.update(product)
    if not product:
        raise HTTPException(status_code=404, detail=APIResponse(code=404, message="Product not found!").dict())
    return product

async def delete_product(id: str):
    deleted = await product_repository.delete(id)
    if not deleted:
        raise HTTPException(status_code=404, detail=APIResponse(code=404, message="Product not found!").dict())
    return True