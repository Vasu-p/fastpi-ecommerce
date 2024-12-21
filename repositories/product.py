from motor.motor_asyncio import AsyncIOMotorDatabase

from config.database import with_db
from repositories.BaseRepository import BaseRepository
from repositories.util import PAGINATION_AGGREGATION, SORT_AGGREGATION
from schemas.common import PaginationParams, SortParams, PaginatedData
from schemas.product import ProductFilterParams

def FILTER_AGGREGATION(filter_params: ProductFilterParams):
    match_dict = {}
    if filter_params.search:
        match_dict["$text"] = { "$search": filter_params.search }
    if filter_params.min_price:
        if "$and" not in match_dict:
            match_dict["$and"] = []
        match_dict["$and"].append({ "price": { "$gt": filter_params.min_price } })
    if filter_params.max_price:
        if "$and" not in match_dict:
            match_dict["$and"] = []
        match_dict["$and"].append({ "price": { "$lt": filter_params.max_price } })
    if filter_params.category:
        match_dict["category"] = filter_params.category
    if filter_params.brand:
        match_dict["brand"] = filter_params.brand

    return {
        "$match": match_dict
    }

class ProductRepository(BaseRepository):
    def __init__(self):
        super().__init__("products")

    @with_db
    async def get_paginated(self, page_params: PaginationParams, sort_params: SortParams,
                      filter_params: ProductFilterParams, db: AsyncIOMotorDatabase):
        try:
            results =  await db[self.collection].aggregate([
                FILTER_AGGREGATION(filter_params),
                SORT_AGGREGATION(sort_params),
                PAGINATION_AGGREGATION(page_params)
            ]).next()
            total_count = results["page_meta"][0]["total_count"] if len(results["page_meta"]) > 0 else 0
            return PaginatedData(data=results["data"], total_count=total_count, **page_params.dict())
        except Exception as e:
            print(e)
            return None