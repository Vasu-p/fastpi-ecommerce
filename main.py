from dotenv import load_dotenv
from fastapi import FastAPI

from config.database import init_connection, close_connection
from controllers.user import router as UserRouter
from controllers.product import router as ProductRouter

load_dotenv()

app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_connection()

@app.on_event("shutdown")
async def shutdown():
    await close_connection()

app.include_router(UserRouter, prefix="/users")
app.include_router(ProductRouter, prefix="/products")