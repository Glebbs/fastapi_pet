from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@postgres_db:5400/items_db"

engine = create_async_engine(
        SQLALCHEMY_DATABASE_URL,
        # echo=True,
    )

async_session = sessionmaker(
        bind=engine, expire_on_commit=False, class_=AsyncSession
    )


async def get_session():
    async with async_session.begin() as session:
        yield session
