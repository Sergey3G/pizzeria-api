from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import cast

from models import Pizza
from dependencies import get_db
from custom_types import PositiveInt

router = APIRouter()


@router.get("/pizza")
async def get_pizza(pizza_id: PositiveInt, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Pizza).where(cast("ColumnElement[bool]", Pizza.id == pizza_id)))
    pizza = result.scalar_one_or_none()
    if not pizza:
        raise HTTPException(status_code=404, detail="Pizza not found")
    return pizza
