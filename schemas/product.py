from typing import Optional

from pydantic import BaseModel

from schemas.common import UpdateModel, OutboundModel


class Product(BaseModel):
    name: str
    description: str
    price: float
    category: str
    brand: str

class ProductOutbound(Product, OutboundModel):
    pass

class UpdateProduct(UpdateModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    category: Optional[str]
    brand: Optional[str]