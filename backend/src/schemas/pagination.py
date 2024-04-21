from fastapi import Query

class PaginationParams:
    def __init__(
        self,
        skip: int = Query(0, ge=0, description="Number of items to skip"),
        limit: int = Query(10, gt=0, le=100, description="Max number of items to return")
    ):
        self.skip = skip
        self.limit = limit
