from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import cast

from models import Pizzeria
from dependencies import get_db
from custom_types import PositiveInt

router = APIRouter()


@router.get("/pizzeria")
async def get_pizzeria(pizzeria_id: PositiveInt, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Pizzeria).where(cast("ColumnElement[bool]", Pizzeria.id == pizzeria_id)))
    pizzeria = result.scalar_one_or_none()
    if not pizzeria:
        raise HTTPException(status_code=404, detail="Pizzeria not found")
    return pizzeria
