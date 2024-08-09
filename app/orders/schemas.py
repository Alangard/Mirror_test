from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class Orders(BaseModel):
    apartment_number: int
    pet_name: str
    pet_breed: str
    walk_start: datetime
    walk_end: datetime

class OrderCreate(Orders):
    pass

class OrderResponse(Orders):
    id: int
    walker_id: int | None 
    duration_minutes: int = Field(..., ge=1, le=30)

    class Config:
        model_config = {'from_attributes': True}
