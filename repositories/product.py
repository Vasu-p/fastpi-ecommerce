from repositories.BaseRepository import BaseRepository

class ProductRepository(BaseRepository):
    def __init__(self):
        super().__init__("products")