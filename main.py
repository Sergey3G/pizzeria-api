from fastapi import FastAPI

from database import engine, Base
from routers.users import router as users_router


app = FastAPI()


app.include_router(users_router)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return "Hello, world!"
