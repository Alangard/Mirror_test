from datetime import date, datetime
from typing import List
from fastapi import APIRouter, Depends, Path
from fastapi.params import Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.orders.schemas import OrderResponse, OrderCreate
from app.orders.services import get_orders_by_date, assign_walker_to_order, create_order

router = APIRouter()

@router.get("/orders/{date}/", response_model=List[OrderResponse])
async def get_orders(date: date = Path(example=datetime.now().date()), session: AsyncSession = Depends(get_async_session)):
    orders = await get_orders_by_date(date, session)
    return orders

@router.post("/orders/", response_model=OrderResponse)
async def create_orders(order_info: OrderCreate, session: AsyncSession = Depends(get_async_session)):
    response = await create_order(order_info, session)
    return response

@router.patch("/order_asign/{order_id}/", response_model=OrderResponse)
async def asign_orders(order_id: int, walker_id: int, session: AsyncSession = Depends(get_async_session)):
    response = await assign_walker_to_order(order_id, walker_id, session)
    return response