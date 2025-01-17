from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from config.database import with_db
from repositories.BaseRepository import BaseRepository
from schemas.shopping_cart import CreateShoppingCart, AddToCart, RemoveFromCart

cart_products_aggregate = {
    "$lookup": {
        "from": "products",
        "localField": "items.product_id",
        "foreignField": "_id",
        "as": "products"
    }
}

cart_id_match = lambda id: {
    "$match": {
        "_id": ObjectId(id)
    }
}
user_id_match = lambda id: {
    "$match": {
        "user_id": ObjectId(id)
    }
}

class ShoppingCartRepository(BaseRepository):
    def __init__(self):
        super().__init__("shopping_carts")

    @with_db
    async def create(self, shopping_cart: CreateShoppingCart, **kwargs):
        return await super().create(document=shopping_cart, init_dict={"items": []})

    @with_db
    async def get_by_id(self, id: str, db: AsyncIOMotorDatabase):
        try:
            cart = (await db[self.collection].aggregate([cart_id_match(id), cart_products_aggregate]).to_list())[0]
            return cart
        except Exception as e:
            print(e)
            return None

    @with_db
    async def get_by_user_id(self, user_id: str, db: AsyncIOMotorDatabase):
        try:
            return (await db[self.collection].aggregate([user_id_match(user_id), cart_products_aggregate]).to_list())[0]
        except:
            return None

    @with_db
    async def add_to_cart(self, id: str, request: AddToCart, db: AsyncIOMotorDatabase):
        try:
            await db[self.collection].find_one_and_update({"_id": ObjectId(id)}, { "$push": {"items": request.dict()} })
            return True
        except Exception as e:
            print(e)
            return False

    @with_db
    async def remove_from_cart(self, id: str, request: RemoveFromCart, db: AsyncIOMotorDatabase):
        try:
            await db[self.collection].find_one_and_update({"_id": ObjectId(id)}, { "$pull": {"items": {'product_id': request.product_id}} })
            return True
        except Exception as e:
            print(e)
            return False

    @with_db
    async def clear_cart(self, id: str, db: AsyncIOMotorDatabase):
        try:
            await db[self.collection].find_one_and_update({"_id": ObjectId(id)}, { "$pull": {"items": {} }})
            return True
        except Exception as e:
            print(e)
            return False

    @with_db
    async def check_if_product_exists(self, id: str, product_id: str, db: AsyncIOMotorDatabase):
        exists = await db[self.collection].find_one({"_id": ObjectId(id), "items.product_id": ObjectId(product_id)})
        if exists:
            return True
        return False

    @with_db
    async def check_if_user_associated(self, id: str, db: AsyncIOMotorDatabase):
        cart = await db[self.collection].find_one({"_id": ObjectId(id)}, {"user_id": 1})
        if "user_id" in cart:
            return True
        return False