import logging
import os
import traceback
from typing import AsyncGenerator, Any, AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.ext.declarative import declarative_base
import contextlib 

logger = logging.getLogger(__name__)

def get_db_url() -> str:
    """Fetches the database connection URL from environment variables or falls back to SQLite."""
    if os.environ.get("DB_CONNECTION_URL"):
        return os.environ.get("DB_CONNECTION_URL")


DATABASE_URL = get_db_url()
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, autoflush=False, autocommit=False)
Base = declarative_base()


async def test_database_connection():
    """
    Test the database connection by attempting to connect and close immediately.
    """
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)  # Ensure tables exist
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        return False


class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}):
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine, expire_on_commit=False)

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

sessionmanager = DatabaseSessionManager(os.environ.get("DB_CONNECTION_URL"), {"echo": True})


async def get_session():
    async with sessionmanager.session() as session:
        yield session