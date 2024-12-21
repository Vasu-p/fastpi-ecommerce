from motor.motor_asyncio import AsyncIOMotorDatabase

from config.database import with_db
from repositories.BaseRepository import BaseRepository
from repositories.util import get_skip_limit
from schemas.common import PaginationParams, PaginatedData

PAGE_META_QUERY = [{"$count": "total_count"}]

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__("users")

    @with_db
    async def get_paginated(self, page_params: PaginationParams, db: AsyncIOMotorDatabase):
        (skip, limit) = get_skip_limit(page_params)
        try:
            results =  await db[self.collection].aggregate([{"$facet": {
                "page_meta": PAGE_META_QUERY,
                "data": [{ "$skip":skip }, { "$limit": limit }]
            }}]).next()
            return PaginatedData(data=results["data"], total_count=results["page_meta"][0]["total_count"], **page_params.dict())
        except:
            return None