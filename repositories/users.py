from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import cast, List

from models import User
from schemas import UserCreate
from repositories.base import IRepository
from custom_types import UserEmail, PositiveInt


class UserRepository(IRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: PositiveInt) -> User | None:
        result = await self.session.execute(select(User).where(cast("ColumnElement[bool]", User.id == user_id)))
        return result.scalars().first()

    async def get_by_email(self, email: UserEmail) -> User | None:
        result = await self.session.execute(select(User).where(cast("ColumnElement[bool]", User.email == email)))
        return result.scalars().first()

    async def get_all(self) -> List[User]:
        result = await self.session.execute(select(User))
        return list(result.scalars().all())

    async def create(self, user_data: UserCreate) -> User:
        new_user = User(**user_data.dict())
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user

    async def delete(self, user_id: PositiveInt) -> None:
        await self.session.execute(delete(User).where(cast("ColumnElement[bool]", User.id == user_id)))
        await self.session.commit()
