import os
from functools import wraps
from typing import Callable

from motor.motor_asyncio import AsyncIOMotorClient

db: AsyncIOMotorClient = None

async def init_connection():
    global db
    if db == None:
        db = AsyncIOMotorClient(os.getenv('DATABASE_URL'))
        print(f"Mongo DB connection created!")

async def close_connection():
    global db
    if db != None:
        db.close()
        print("Mongo DB connection closed!")


def with_db(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        global db
        result = await func(*args, **kwargs, db=db.get_database("default"))
        return result
    return wrapper