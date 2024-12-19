from typing import Optional

from schemas.common import DocumentUpdate, DocumentCreate


class Product(DocumentCreate):
    name: str
    description: str
    price: float
    category: str
    brand: str

class UpdateProduct(DocumentUpdate):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    category: Optional[str]
    brand: Optional[str]