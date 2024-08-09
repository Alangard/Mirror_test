from datetime import date
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.users.schemas import UserResponse, UserCreate
from app.users.services import get_user_by_id, create_user


router = APIRouter()

@router.get("/users/{id}/", response_model=UserResponse)
async def get_user(id: int, session: AsyncSession = Depends(get_async_session)):
    response = await get_user_by_id(id, session)
    return response

@router.post("/users/", response_model=UserResponse)
async def add_user(user_info: UserCreate, session: AsyncSession = Depends(get_async_session)):
    response = await create_user(user_info, session)
    return response