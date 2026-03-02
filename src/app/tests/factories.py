from datetime import date, timedelta
from decimal import Decimal
from typing import Any

import factory
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import PriceModel
from app.models.price import PriceType


class PriceFactory(factory.DictFactory):
    article_number = factory.Sequence(lambda n: f"ARTICLE-{n}")
    start_date = factory.LazyFunction(lambda: date.today() - timedelta(days=7))
    end_date = factory.LazyFunction(lambda: date.today() + timedelta(days=7))
    price = Decimal("9.99")
    price_type = PriceType.REGULAR


async def create_price_factory(
    async_session: AsyncSession,
    **kwargs: Any,
) -> PriceModel:
    payload = PriceFactory(**kwargs)
    price = PriceModel(**payload)
    async_session.add(price)
    await async_session.commit()
    await async_session.refresh(price)
    return price
