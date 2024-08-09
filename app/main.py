from fastapi import FastAPI, Request
from contextlib import asynccontextmanager

from app.config import settings
from app.database import BaseModel, engine
from app.orders.router import router as api_router
from app.users.router import router as user_router




@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Async context manager for startup and shutdown lifecycle events.
    - Creates database tables.
    - Sets up bot commands and webhook.

    Yields control during application's lifespan and performs cleanup on exit.
    - Disposes all database connections.
    - Deletes bot webhook and commands.
    - Closes aiohttp session
    """ 

    # Application startup
    async with engine.begin() as connection:
        # Create tables
        await connection.run_sync(BaseModel.metadata.create_all)
    try:
        yield
    finally:
        await engine.dispose()



application = FastAPI(title="Mirror_test", lifespan=lifespan)

application.include_router(api_router, prefix=settings.api_prefix)
application.include_router(user_router, prefix=settings.api_prefix)



@application.get("/")
async def root(request: Request):
    return 