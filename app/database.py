from typing import AsyncGenerator
from datetime import datetime, timezone
from sqlalchemy import MetaData, create_engine, text
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from app.config import settings

metadata = MetaData()

class BaseModel(DeclarativeBase):
    metadata = metadata

    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True), server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.now(timezone.utc)
    )


DATABASE_URL_ASYNC = (
    f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)
DATABASE_URL_SYNC = (
    f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

engine = create_async_engine(
    DATABASE_URL_ASYNC, 
    pool_size=40, 
    max_overflow=20, 
    pool_recycle=3600, 
)

sync_engine = create_engine(
    DATABASE_URL_SYNC, 
)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
sync_session_maker = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session