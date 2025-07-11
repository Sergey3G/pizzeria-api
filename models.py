from sqlalchemy import Column, Integer, String, Float, Date, Enum as SqlEnum, UniqueConstraint
from enum import Enum

from database import Base
from custom_types import UserName, UserEmail, UserPassword


class RoleEnum(str, Enum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email", name="uq_email"), )

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    birth_date = Column(Date, nullable=True)
    age = Column(Integer, nullable=True)
    city = Column(String, nullable=True)
    street = Column(String, nullable=True)
    house_number = Column(String, nullable=True)
    balance = Column(Float, default=0.0)
    hashed_password = Column(String, nullable=False)
    role = Column(SqlEnum(RoleEnum), default=RoleEnum.USER)


class Pizza(Base):
    __tablename__ = "pizzas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    size = Column(String)
    price = Column(Float)


class Pizzeria(Base):
    __tablename__ = "pizzerias"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String)
    street = Column(String)
    house_number = Column(String)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    pizza_id = Column(Integer)
    pizzeria_id = Column(Integer)
    date = Column(Date)
