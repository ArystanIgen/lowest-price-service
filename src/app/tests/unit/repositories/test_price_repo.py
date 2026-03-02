from datetime import date, timedelta
from decimal import Decimal

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.price import PriceType
from app.repositories.price import PriceRepository
from app.schemas.price import PriceCreate, PriceUpdate
from app.tests.factories import create_price_factory

price_repo = PriceRepository()


@pytest.mark.asyncio
async def test_create_update_and_remove_price_model(
    async_session: AsyncSession,
):
    today = date.today()

    created_price = await price_repo.create(
        async_session,
        obj_in=PriceCreate(
            article_number="ART-100",
            start_date=today - timedelta(days=5),
            end_date=today + timedelta(days=5),
            price=Decimal("12.50"),
            price_type=PriceType.REGULAR,
        ),
    )

    assert created_price is not None
    assert created_price.id is not None
    assert created_price.article_number == "ART-100"

    updated_price = await price_repo.update(
        async_session=async_session,
        instance=created_price,
        obj_update=PriceUpdate(
            article_number=created_price.article_number,
            start_date=created_price.start_date,
            end_date=None,
            price=Decimal("10.25"),
            price_type=PriceType.PROMO,
        ),
    )

    remaining_prices = await price_repo.get_multi(async_session)

    assert updated_price is not None
    assert float(updated_price.price) == pytest.approx(10.25)
    assert updated_price.end_date is None
    assert updated_price.price_type == PriceType.PROMO
    assert len(remaining_prices) == 1

    removed_price = await price_repo.remove(
        async_session=async_session,
        id_=created_price.id,
    )

    remaining_prices = await price_repo.get_multi(async_session)

    assert removed_price is None
    assert remaining_prices == []


@pytest.mark.asyncio
async def test_get_lowest_price_for_article_returns_lowest_active_price(
    async_session: AsyncSession,
):
    today = date.today()
    list_of_prices = [
        {
            "start_date": today - timedelta(days=7),
            "end_date": today + timedelta(days=7),
            "price": Decimal("11.50"),
            "price_type": PriceType.REGULAR,
        },
        {
            "start_date": today - timedelta(days=3),
            "end_date": today + timedelta(days=2),
            "price": Decimal("8.99"),
            "price_type": PriceType.PROMO,
        },
        {
            "start_date": today - timedelta(days=90),
            "end_date": today - timedelta(days=31),
            "price": Decimal("1.99"),
            "price_type": PriceType.REGULAR,
        },
        {
            "start_date": today + timedelta(days=1),
            "end_date": today + timedelta(days=30),
            "price": Decimal("0.99"),
            "price_type": PriceType.PROMO,
        },
    ]

    for price in list_of_prices:
        await create_price_factory(
            async_session,
            article_number="ART-200",
            start_date=price["start_date"],
            end_date=price["end_date"],
            price=price["price"],
            price_type=price["price_type"],
        )

    fetched_price = await price_repo.get_lowest_price_for_article(
        async_session=async_session,
        article_number="ART-200",
        days=30,
    )

    assert fetched_price == {
        "article_number": "ART-200",
        "lowest_price": 8.99,
    }


@pytest.mark.asyncio
async def test_get_lowest_price_for_article_returns_none_when_missing(
    async_session: AsyncSession,
):
    fetched_price = await PriceRepository().get_lowest_price_for_article(
        async_session=async_session,
        article_number="UNKNOWN",
        days=30,
    )

    assert fetched_price is None


@pytest.mark.asyncio
async def test_get_lowest_prices_for_all_articles_groups_by_article(
    async_session: AsyncSession,
):
    today = date.today()

    list_of_prices = [
        {
            "article_number": "ART-300",
            "start_date": today - timedelta(days=10),
            "end_date": today + timedelta(days=1),
            "price": Decimal("14.99"),
            "price_type": PriceType.REGULAR,
        },
        {
            "article_number": "ART-300",
            "start_date": today - timedelta(days=2),
            "end_date": None,
            "price": Decimal("12.49"),
            "price_type": PriceType.REGULAR,
        },
        {
            "article_number": "ART-301",
            "start_date": today - timedelta(days=4),
            "end_date": today + timedelta(days=10),
            "price": Decimal("6.50"),
            "price_type": PriceType.REGULAR,
        },
        {
            "article_number": "ART-302",
            "start_date": today - timedelta(days=45),
            "end_date": today - timedelta(days=31),
            "price": Decimal("2.00"),
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

    fetched_prices = await price_repo.get_lowest_prices_for_all_articles(
        async_session=async_session,
        days=30,
    )

    fetched_by_article = {
        item["article_number"]: item["lowest_price"] for item in fetched_prices
    }

    assert fetched_by_article == {
        "ART-300": 12.49,
        "ART-301": 6.5,
    }
