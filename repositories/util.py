from schemas.common import PaginationParams

def remove_id(dict: dict):
    dict.pop("id", None)
    return dict

def get_skip_limit(page_params: PaginationParams):
    skip = page_params.page_no * page_params.page_size
    limit = page_params.page_size
    return {skip, limit}