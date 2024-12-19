from repositories.BaseRepository import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__("users")