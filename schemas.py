from pydantic import BaseModel, computed_field, ConfigDict
from datetime import date

from custom_types import UserName, UserEmail, UserPassword


class UserCreate(BaseModel):
    email: UserEmail
    name: UserName | None = None
    birth_date: date
    city: str | None = None
    street: str | None = None
    house_number: str | None = None
    password: UserPassword

    @computed_field
    def age(self) -> int:
        today = date.today()
        birth_date = self.birth_date
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age


class UserLogin(BaseModel):
    email: UserEmail
    password: UserPassword


class UserOut(BaseModel):
    id: int
    email: UserEmail
    name: UserName | None
    birth_date: date
    city: str | None
    street: str | None
    house_number: str | None
    balance: float

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    def age(self) -> int:
        today = date.today()
        birth_date = self.birth_date
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age


class UserUpdate(BaseModel):
    name: str | None = None
    birth_date: date | None = None
    city: str | None = None
    street: str | None = None
    house_number: str | None = None


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str


class TokenRefresh(BaseModel):
    refresh_token: str
