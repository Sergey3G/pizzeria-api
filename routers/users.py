from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from models import User
from dependencies import get_db
from schemas import UserCreate, UserOut, TokenPair, TokenRefresh, UserUpdate
from crud import create_user, authenticate_user, get_user, update_user
from utils import create_access_token, create_refresh_token, decode_access_token
from auth import get_current_user, require_admin, oauth2_scheme
from blacklisted_tokens import add_to_blacklist
from custom_types import PositiveInt


router = APIRouter()


@router.post("/register", response_model=UserOut)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await create_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenPair)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    data = {"sub": str(user.id)}
    return {
        "access_token": create_access_token(data, timedelta(minutes=30)),
        "refresh_token": create_refresh_token(data),
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=TokenPair)
async def refresh_tokens(body: TokenRefresh):
    user_id = decode_access_token(body.refresh_token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    data = {"sub": str(user_id)}
    return {
        "access_token": create_access_token(data, timedelta(minutes=30)),
        "refresh_token": create_refresh_token(data),
        "token_type": "bearer"
    }


@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    add_to_blacklist(token)
    return {"message": "Logged out"}


@router.get("/user/{user_id}", response_model=UserOut)
async def get_user_by_id(user_id: PositiveInt, db: AsyncSession = Depends(get_db)):
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/balance", response_model=float)
async def check_balance(current_user=Depends(get_current_user)):
    return current_user.balance


@router.put("/user/me", response_model=UserOut)
async def update_my_profile(
        updates: UserUpdate,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    return await update_user(db, current_user, updates)
