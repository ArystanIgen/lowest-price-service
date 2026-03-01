from datetime import date, timedelta

from typing import Any
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import PriceModel
from app.repositories.base import BaseRepository
from app.schemas.price import PriceUpdate, PriceCreate


class PriceRepository(
    BaseRepository[PriceModel, PriceCreate, PriceUpdate]
):
    model = PriceModel

    async def get_lowest_price_for_article(
        self,
        async_session: AsyncSession,
        article_number: str,
        days: int = 30,
    ) -> dict[str, Any] | None:
        target_date = date.today()
        start_period = target_date - timedelta(days=days)

        stmt = (
            select(
                self.model.article_number,
                func.min(self.model.price).label("lowest_price"),
            )
            .where(
                and_(
                    self.model.article_number == article_number,
                    self.model.start_date <= target_date,
                    (self.model.end_date == None) | (self.model.end_date >= start_period),
                )
            )
            .group_by(self.model.article_number)
        )

        result = await async_session.execute(stmt)
        row = result.first()

        if row and row.lowest_price is not None:
            return {
                "article_number": row.article_number,
                "lowest_price": float(row.lowest_price),
            }
        return None

    async def get_lowest_prices_for_all_articles(
        self,
        async_session: AsyncSession,
        days: int = 30,
    ) -> list[dict[str, Any]]:
        target_date = date.today()
        start_period = target_date - timedelta(days=days)

        stmt = (
            select(
                self.model.article_number,
                func.min(self.model.price).label("lowest_price"),
            )
            .where(
                and_(
                    self.model.start_date <= target_date,
                    (self.model.end_date == None) | (self.model.end_date >= start_period),
                )
            )
            .group_by(self.model.article_number)
        )

        result = await async_session.execute(stmt)
        rows = result.all()

        return [
            {
                "article_number": row.article_number,
                "lowest_price": float(row.lowest_price),
            }
            for row in rows
            if row.lowest_price is not None
        ]
