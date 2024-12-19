from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel
from pymongo import ReturnDocument

from config.database import with_db
from repositories.util import remove_id
from schemas.common import DocumentUpdate


class BaseRepository:
    def __init__(self, collection):
        self.collection = collection

    @with_db
    async def create(self, document: BaseModel, db: AsyncIOMotorDatabase):
        try:
            insert_result = await db[self.collection].insert_one(document.dict(exclude_unset=True, exclude_none=True))
            return str(insert_result.inserted_id)
        except Exception as e:
            print(e)
            return None

    @with_db
    async def get_all(self, db: AsyncIOMotorDatabase):
        users = await db[self.collection].find().to_list()
        return users

    @with_db
    async def get_by_id(self, objectId: str, db: AsyncIOMotorDatabase):
        user = await db[self.collection].find_one({"_id": ObjectId(objectId)})
        return user

    @with_db
    async def update(self, document: DocumentUpdate, db: AsyncIOMotorDatabase):
        return await db[self.collection].find_one_and_update({"_id": document.id}, {
            "$set": remove_id(document.dict(exclude_none=True, exclude_unset=True))}, return_document=ReturnDocument.AFTER)

    @with_db
    async def delete(self, objectId: str, db: AsyncIOMotorDatabase):
        return await db[self.collection].delete_one({"_id": ObjectId(objectId)})
