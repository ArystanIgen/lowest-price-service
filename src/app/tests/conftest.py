from collections.abc import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.api.deps.session import get_async_session
from app.core.config import CONFIG
from app.db.session import async_engine as test_async_engine
from app.main import main_app
from app.models import BaseModel
from app.tests.fixtures import *  # noqa: F403


@pytest_asyncio.fixture
async def test_engine() -> AsyncGenerator:
    await test_async_engine.dispose()

    async with test_async_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)

    yield test_async_engine

    async with test_async_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)

    await test_async_engine.dispose()


@pytest_asyncio.fixture
async def async_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    session_factory = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with session_factory() as session:
        try:
            yield session
        finally:
            if session.in_transaction():
                await session.rollback()


@pytest_asyncio.fixture
async def async_client(async_session: AsyncSession):
    def _get_db_override() -> AsyncSession:
        return async_session

    main_app.dependency_overrides[get_async_session] = _get_db_override

    transport = ASGITransport(app=main_app)
    async with AsyncClient(
        transport=transport,
        base_url=CONFIG.api.host,
    ) as client:
        yield client

    main_app.dependency_overrides.clear()
