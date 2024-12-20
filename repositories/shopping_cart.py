from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from config.database import with_db
from repositories.BaseRepository import BaseRepository
from schemas.shopping_cart import CreateShoppingCart, AddToCart


class ShoppingCartRepository(BaseRepository):
    def __init__(self):
        super().__init__("shopping_carts")

    @with_db
    async def create(self, shopping_cart: CreateShoppingCart, **kwargs):
        return await super().create(document=shopping_cart, init_dict={"items": []})

    @with_db
    async def add_to_cart(self, id: str, request: AddToCart, db: AsyncIOMotorDatabase):
        try:
            await db[self.collection].find_one_and_update({"_id": ObjectId(id)}, { "$push": {"items": request.dict()} })
            return True
        except Exception as e:
            print(e)
            return False
