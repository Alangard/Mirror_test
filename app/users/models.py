from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import BaseModel


class Walker(BaseModel):
    __tablename__ = "walkers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    second_name: Mapped[str] = mapped_column(String(100), index=True)

    orders: Mapped["Order"] = relationship("Order", back_populates="walker")