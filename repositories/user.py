from bson import ObjectId

from config.database import with_db
from schemas.user import User
from motor.motor_asyncio import AsyncIOMotorDatabase

@with_db
async def create(user: User, db: AsyncIOMotorDatabase):
    try:
        insert_result = await db["users"].insert_one(user.dict(exclude_unset=True))
        return str(insert_result.inserted_id)
    except Exception as e:
        print(e)
        return None

@with_db
async def get_all(db: AsyncIOMotorDatabase):
    users = await db["users"].find().to_list()
    return users

@with_db
async def get_by_id(objectId: str, db: AsyncIOMotorDatabase):
    print(f"querying by {objectId}")
    user = await db["users"].find_one({ "_id": ObjectId(objectId) })
    return user