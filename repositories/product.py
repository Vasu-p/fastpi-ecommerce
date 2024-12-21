from motor.motor_asyncio import AsyncIOMotorDatabase

from config.database import with_db
from repositories.BaseRepository import BaseRepository
from repositories.util import PAGINATION_AGGREGATION, SORT_AGGREGATION
from schemas.common import PaginationParams, SortParams, PaginatedData
from schemas.product import ProductFilterParams


class ProductRepository(BaseRepository):
    def __init__(self):
        super().__init__("products")

    @with_db
    async def get_paginated(self, page_params: PaginationParams, sort_params: SortParams,
                      filter_params: ProductFilterParams, db: AsyncIOMotorDatabase):
        try:
            results =  await db[self.collection].aggregate([
                SORT_AGGREGATION(sort_params),
                PAGINATION_AGGREGATION(page_params)
            ]).next()
            return PaginatedData(data=results["data"], total_count=results["page_meta"][0]["total_count"], **page_params.dict())
        except:
            return None