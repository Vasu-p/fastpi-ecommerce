from typing import Optional, List
from pydantic import Field, BaseModel
from pyobjectID import MongoObjectId, PyObjectId

from schemas.common import OutboundModel
from schemas.product import ProductOutbound


class ShoppingCartItem(BaseModel):
    product: ProductOutbound
    quantity: int
    total_price: float

class ShoppingCartOutbound(OutboundModel):
    user_id: Optional[MongoObjectId] = Field(default=None)
    items: List[ShoppingCartItem] = []
    price_before_tax: float = 0.0
    tax: float = 0.0
    total_price: float = 0.0

class CreateShoppingCart(BaseModel):
    user_id: Optional[PyObjectId] = Field(default=None)
