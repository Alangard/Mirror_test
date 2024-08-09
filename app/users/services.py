from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import Walker
from app.users.schemas import UserResponse, UserCreate


async def get_user_by_id(id: int, session: AsyncSession) -> UserResponse:

    query = select(Walker).where(Walker.id == id) 
    result = await session.execute(query)
    user = result.scalars().one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail=f"Человек с ID {id} не был найден")
    
    return UserResponse.model_validate(user.__dict__)

async def create_user(user_info: UserCreate, session: AsyncSession) -> UserResponse:

    new_user = Walker(name=user_info.name,second_name=user_info.second_name)
    
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    
    user_dict = new_user.__dict__
    
    return UserResponse(**user_dict)

