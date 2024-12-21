from typing import Optional

from pydantic import BaseModel

from schemas.common import UpdateModel, OutboundModel


class Product(BaseModel):
    name: str
    description: str
    price: float
    category: str
    brand: str

class CreateProduct(Product):
    pass

class ProductOutbound(Product, OutboundModel):
    pass

class UpdateProduct(UpdateModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    brand: Optional[str] = None

class ProductFilterParams(BaseModel):
    search: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    category: Optional[str] = None
    brand: Optional[str] = None