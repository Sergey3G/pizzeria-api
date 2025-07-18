from sqlalchemy.ext.asyncio import AsyncSession

from repositories.users import UserRepository
from schemas import UserCreate
from models import User
from custom_types import PositiveInt


class UserService:
    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)

    async def register_user(self, user_data: UserCreate):
        existing = await self.repository.get_by_email(user_data.email)
        if existing:
            raise ValueError("User with this email already exists")
        return await self.repository.create(user_data)

    async def get_user(self, user_id: PositiveInt):
        user = self.repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user
