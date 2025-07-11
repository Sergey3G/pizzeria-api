from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from typing import cast

from models import User
from schemas import UserCreate, UserUpdate
from utils import hash_password, verify_password


async def create_user(db: AsyncSession, user_data: UserCreate):
    result = await db.execute(select(User).where(cast("ColumnElement[bool]", User.email == user_data.email)))
    if result.scalar_one_or_none():
        raise ValueError("Email already registered")

    hashed_pwd = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        name=user_data.name,
        birth_date=user_data.birth_date,
        age=user_data.age,
        city=user_data.city,
        street=user_data.street,
        house_number=user_data.house_number,
        hashed_password=hashed_pwd,
    )
    db.add(new_user)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ValueError("Email already registered")
    await db.refresh(new_user)
    return new_user


async def authenticate_user(db: AsyncSession, email: str, password: str):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user and verify_password(password, user.hashed_password):
        return user
    return None


async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def update_user(db: AsyncSession, user: User, updates: UserUpdate):
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(user, field, value)
    await db.commit()
    await db.refresh(user)
    return user
