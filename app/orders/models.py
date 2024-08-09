import enum
from sqlalchemy import Enum,ForeignKey,Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import TIMESTAMP

from app.database import BaseModel

class Order(BaseModel):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    apartment_number: Mapped[int] = mapped_column(Integer)
    pet_name: Mapped[str] = mapped_column(String(100))
    pet_breed: Mapped[str] = mapped_column(String(100))
    walk_start: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True), index=True)
    walk_end: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True), index=True)

    walker_id: Mapped[int] = mapped_column(Integer, ForeignKey("walkers.id", ondelete='SET NULL'), nullable=True)
    walker: Mapped["Walker"] = relationship("Walker", back_populates="orders")


