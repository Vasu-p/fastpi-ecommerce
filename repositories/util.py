from schemas.common import PaginationParams, SortParams


def remove_id(dict: dict):
    dict.pop("id", None)
    return dict

def get_skip_limit(page_params: PaginationParams):
    skip = page_params.page_no * page_params.page_size
    limit = page_params.page_size
    return { "skip": skip, "limit": limit }

def PAGINATION_AGGREGATION(page_params: PaginationParams):
    (skip, limit) = get_skip_limit(page_params).values()
    return {
        "$facet": {
            "page_meta": [{"$count": "total_count"}],
            "data": [{"$skip": skip}, {"$limit": limit}]
        }
    }

def SORT_AGGREGATION(sort_params: SortParams):
    sort = {
        "$sort": {
            sort_params.sort_by: sort_params.sort_dir.get_mongodb_dir()
        }
    }
    return sort