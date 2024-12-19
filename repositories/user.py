from bson import ObjectId
from pymongo import ReturnDocument

from config.database import with_db
from repositories.util import remove_id
from schemas.user import User, UpdateUser
from motor.motor_asyncio import AsyncIOMotorDatabase

@with_db
async def create(user: User, db: AsyncIOMotorDatabase):
    try:
        insert_result = await db["users"].insert_one(user.dict(exclude_unset=True, exclude_none=True))
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

@with_db
async def update(user: UpdateUser, db: AsyncIOMotorDatabase):
    return await db["users"].find_one_and_update({ "_id": user.id }, { "$set": remove_id(user.dict(exclude_none=True, exclude_unset=True)) }, return_document=ReturnDocument.AFTER)

@with_db
async def delete(objectId: str, db: AsyncIOMotorDatabase):
    return await db["users"].delete_one({ "_id": ObjectId(objectId) })
