import datetime
from typing import List
from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.orders.models import  Order
from app.orders.schemas import OrderCreate, OrderResponse
from app.users.models import Walker

async def get_orders_by_date(walk_date: datetime.date, session: AsyncSession) -> List[OrderResponse]:
    query = select(Order).where(func.date(Order.walk_start) == walk_date)
    result = await session.execute(query)
    
    orders = result.scalars().all()
    
    orders_response = []
    for order in orders:
        # Преобразуем SQLAlchemy объект в словарь
        order_dict = order.__dict__.copy()
        
        # Вычисляем duration_minutes как разницу между walk_end и walk_start
        duration = order.walk_end - order.walk_start
        order_dict['duration_minutes'] = int(duration.total_seconds() // 60)
        
        # Преобразуем словарь в Pydantic модель
        order_response = OrderResponse.model_validate(order_dict)
        orders_response.append(order_response)
    
    return orders_response


async def create_order(order_info: OrderCreate, session: AsyncSession) -> OrderResponse:
    

    # Проверка времени начала прогулки
    # Извлечение времени из datetime
    start_time = order_info.walk_start.time().replace(second=0, microsecond=0)
    
    # Проверка времени начала прогулки
    valid_times = [datetime.time(hour=h, minute=0) for h in range(7, 24)] + [datetime.time(hour=h, minute=30) for h in range(7, 24)]

    if start_time not in valid_times:
        raise HTTPException(status_code=404, detail="Время начала прогулки должно быть в начале или в середине часа, и в пределах от 7:00 до 23:00.")

    
    # Проверка продолжительности прогулки
    duration = order_info.walk_end - order_info.walk_start
    if duration > datetime.timedelta(minutes=30):
        raise HTTPException(status_code=404, detail="Продолжительность прогулки не может превышать 30 минут.")

    # Проверка наличия других заказов в это время (не могут гулять одновременно с несколькими животными)
    stmt = (
        select(Order)
        .where(
            (Order.walk_start <= order_info.walk_end) &
            (Order.walk_end >= order_info.walk_start)
        )
    )
    result = await session.execute(stmt)
    overlapping_orders = result.scalars().all()

    if overlapping_orders:
        raise HTTPException(status_code=404, detail="В это время уже есть другой заказ. Пожалуйста, выберите другое время.")
    
    # Создание нового заказа
    new_order = Order(
        apartment_number=order_info.apartment_number,
        pet_name=order_info.pet_name,
        pet_breed=order_info.pet_breed,
        walk_start=order_info.walk_start,
        walk_end=order_info.walk_end,
        walker_id=None  # Изначально заказ создается без привязки к walker
    )

    session.add(new_order)
    await session.commit()
    await session.refresh(new_order)

    # Преобразование в словарь и добавление поля duration_minutes
    order_dict = new_order.__dict__
    duration_minutes = int(duration.total_seconds() // 60)
    
    return OrderResponse(**{**order_dict, 'duration_minutes': duration_minutes})


async def assign_walker_to_order(order_id: int, walker_id: int, session: AsyncSession) -> OrderResponse:
    order_query = select(Order).where(Order.id == order_id)
    walker_query = select(Walker).where(Walker.id == walker_id)

    order_result = await session.execute(order_query)
    walker_result = await session.execute(walker_query)

    order = order_result.scalars().one_or_none()
    walker = walker_result.scalars().one_or_none()

    if order is None:
        raise HTTPException(status_code=404, detail=f"Заказ с ID {order_id} не найден")
    if walker is None:
        raise HTTPException(status_code=404, detail=f"Человек с ID {walker_id} не был найден")
    
    order.walker_id = walker_id
    await session.commit()

    order_dict = order.__dict__.copy()
    duration = order.walk_end - order.walk_start
    order_dict['duration_minutes'] = int(duration.total_seconds() // 60)
    order_response = OrderResponse.model_validate(order_dict)
    
    return order_response
