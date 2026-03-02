from datetime import date, timedelta
from decimal import Decimal

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import CONFIG
from app.models.price import PriceType
from app.tests.factories import create_price_factory


@pytest.mark.asyncio
async def test_get_lowest_prices_api_returns_lowest_prices_for_all_articles(
    async_client: AsyncClient,
    async_session: AsyncSession,
):
    today = date.today()

    list_of_prices = [
        {
            "article_number": "ART-400",
            "start_date": today - timedelta(days=7),
            "end_date": today + timedelta(days=7),
            "price": Decimal("18.50"),
            "price_type": PriceType.REGULAR,
        },
        {
            "article_number": "ART-400",
            "start_date": today - timedelta(days=3),
            "end_date": today + timedelta(days=1),
            "price": Decimal("15.25"),
            "price_type": PriceType.PROMO,
        },
        {
            "article_number": "ART-401",
            "start_date": today - timedelta(days=5),
            "end_date": None,
            "price": Decimal("7.10"),
            "price_type": PriceType.REGULAR,
        },
        {
            "article_number": "ART-402",
            "start_date": today - timedelta(days=45),
            "end_date": today - timedelta(days=31),
            "price": Decimal("1.99"),
            "price_type": PriceType.REGULAR,
        }

    ]

    for price in list_of_prices:
        await create_price_factory(
            async_session,
            article_number=price["article_number"],
            start_date=price["start_date"],
            end_date=price["end_date"],
            price=price["price"],
            price_type=price["price_type"],
        )

    response = await async_client.get(
        f"{CONFIG.api.prefix}/v1/articles/lowest-prices"
    )

    assert response.status_code == 200

    payload = {
        item["article_number"]: item["lowest_price"]
        for item in response.json()
    }
    assert payload == {
        "ART-400": 15.25,
        "ART-401": 7.1,
    }


@pytest.mark.asyncio
async def test_get_article_lowest_price_api_returns_specific_article(
    async_client: AsyncClient,
    async_session: AsyncSession,
):
    today = date.today()

    list_of_prices = [
        {
            "start_date": today - timedelta(days=12),
            "end_date": today + timedelta(days=5),
            "price": Decimal("21.00"),
            "price_type": PriceType.REGULAR,
        },
        {
            "start_date": today - timedelta(days=4),
            "end_date": today + timedelta(days=2),
            "price": Decimal("19.95"),
            "price_type": PriceType.PROMO,
        }
    ]

    for price in list_of_prices:
        await create_price_factory(
            async_session,
            article_number="ART-500",
            start_date=price["start_date"],
            end_date=price["end_date"],
            price=price["price"],
            price_type=price["price_type"],
        )

    response = await async_client.get(
        f"{CONFIG.api.prefix}/v1/articles/ART-500/lowest-price"
    )

    assert response.status_code == 200
    assert response.json() == {
        "article_number": "ART-500",
        "lowest_price": 19.95,
    }


@pytest.mark.asyncio
async def test_get_article_lowest_price_api_returns_not_found(
    async_client: AsyncClient,
):
    response = await async_client.get(
        f"{CONFIG.api.prefix}/v1/articles/UNKNOWN/lowest-price"
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": (
            "No price data found for article UNKNOWN in the last 30 days"
        )
    }
