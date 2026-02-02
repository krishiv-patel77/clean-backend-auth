from typing import Annotated
from src.core.config import settings

from fastapi import Depends
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Create the engine using the DB URL
engine = create_async_engine(settings.DATABASE_URL, pool_pre_ping=True, pool_size=5, max_overflow=10)

# Config for each individual DB session
AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base used to extend all sqlalchemy database tables
Base = declarative_base()

# Generator for getting a db session
async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()

# This is the type annotation we will use to start a DB session automatically; this is what we will import to other files from this file
DB_Session = Annotated[AsyncSession, Depends(get_db)]