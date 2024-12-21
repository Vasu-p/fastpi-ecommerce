from typing import List

from fastapi import APIRouter, Depends

from schemas.common import APIResponse, PaginatedData, PaginationParams, SortParams
from schemas.product import CreateProduct, UpdateProduct, ProductOutbound, ProductFilterParams
import services.product as product_service

router = APIRouter()


# Endpoint to register a new product
@router.post("/", response_model=APIResponse)
async def register_product(product: CreateProduct):
    product_id = await product_service.register_product(product)
    return APIResponse(code=200, message="Product registered successfully!", detail={"_id": product_id}).dict()


# Endpoint to get all products
@router.get("/all", response_model=List[ProductOutbound])
async def get_products():
    return await product_service.get_all_products()

@router.get("/", response_model=PaginatedData[ProductOutbound])
async def get_paginated_products(page_params: PaginationParams = Depends(),
                                 sort_params: SortParams = Depends(), filter_params: ProductFilterParams = Depends()):
    return await product_service.get_products_paginated(page_params=page_params,
                                                        sort_params=sort_params, filter_params=filter_params)

# Endpoint to get a specific product by its ID
@router.get("/{product_id}", response_model=ProductOutbound)
async def get_product_by_id(product_id: str):
    return await product_service.get_product_by_id(product_id)


# Endpoint to update a product
@router.patch("/", response_model=ProductOutbound)
async def update_product(product: UpdateProduct):
    return await product_service.update_product(product)


# Endpoint to delete a product
@router.delete("/{product_id}", response_model=APIResponse)
async def delete_product(product_id: str):
    await product_service.delete_product(product_id)
    return APIResponse(code=200, message="Product deleted successfully!").dict()
