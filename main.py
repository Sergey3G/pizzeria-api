from fastapi import FastAPI

from database import engine, Base
from routers.users import router as users_router
from routers.pizzas import router as pizzas_router
from routers.pizzerias import router as pizzerias_router


app = FastAPI()


app.include_router(users_router)
app.include_router(pizzas_router)
app.include_router(pizzerias_router)


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return "Hello, world!"
