from fastapi import HTTPException

from repositories.product import ProductRepository
from schemas.common import APIResponse, PaginationParams, SortParams
from schemas.product import CreateProduct, UpdateProduct, ProductFilterParams

product_repository = ProductRepository()


async def register_product(product: CreateProduct):
    created_id = await product_repository.create(document=product)
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

async def does_product_exist(id: str):
    exists = await product_repository.check_if_exists(id)
    if not exists:
        raise HTTPException(status_code=404, detail=APIResponse(code=404, message="Product not found!").dict())
    return True

async def get_products_paginated(page_params: PaginationParams,
                                 filter_params: ProductFilterParams, sort_params: SortParams):
    products = await product_repository.get_paginated(page_params=page_params, sort_params=sort_params, filter_params=filter_params)
    if not products:
        raise HTTPException(status_code=500, detail=APIResponse(code=500, message="Error loading products data!").dict())
    return products