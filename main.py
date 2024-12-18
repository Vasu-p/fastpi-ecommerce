from fastapi import FastAPI

from config.database import init_connection, close_connection
from controllers.user import router as UserRouter

app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_connection()

@app.on_event("shutdown")
async def shutdown():
    await close_connection()

app.include_router(UserRouter, prefix="/users")