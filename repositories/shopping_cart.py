from repositories.BaseRepository import BaseRepository

class ShoppingCartRepository(BaseRepository):
    def __init__(self):
        super().__init__("shopping_carts")