from motor.motor_asyncio import AsyncIOMotorDatabase

from config.database import with_db
from repositories.BaseRepository import BaseRepository
from repositories.util import PAGINATION_AGGREGATION
from schemas.common import PaginationParams, PaginatedData

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__("users")

    @with_db
    async def get_paginated(self, page_params: PaginationParams, db: AsyncIOMotorDatabase):
        try:
            results =  await db[self.collection].aggregate([PAGINATION_AGGREGATION(page_params)]).next()
            return PaginatedData(data=results["data"], total_count=results["page_meta"][0]["total_count"], **page_params.dict())
        except:
            return None