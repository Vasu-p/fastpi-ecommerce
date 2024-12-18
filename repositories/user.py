from config.database import with_db
from schemas.user import User
from motor.motor_asyncio import AsyncIOMotorDatabase

@with_db
async def create_user(user: User, db: AsyncIOMotorDatabase):
    try:
        insert_result = await db["users"].insert_one(user.dict(exclude_unset=True))
        return insert_result.inserted_id
    except Exception as e:
        print(e)
        return -1

@with_db
async def get_all_users(db: AsyncIOMotorDatabase):
    return await db["users"].find().to_list()