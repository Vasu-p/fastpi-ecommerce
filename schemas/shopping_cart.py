from typing import Optional, List
from pydantic import Field, BaseModel
from pyobjectID import MongoObjectId, PyObjectId

from schemas.common import OutboundModel
from schemas.product import ProductOutbound


class ShoppingCartItem(BaseModel):
    product_id: MongoObjectId
    quantity: int
    total_price: float = 0.0

class ShoppingCartOutbound(OutboundModel):
    user_id: Optional[MongoObjectId] = Field(default=None)
    items: List[ShoppingCartItem] = []
    total_price: float = 0.0
    products: List[ProductOutbound] = []

class CreateShoppingCart(BaseModel):
    user_id: Optional[PyObjectId] = Field(default=None)

class AddToCart(BaseModel):
    product_id: PyObjectId
    quantity: int = 1

class RemoveFromCart(BaseModel):
    product_id: PyObjectId