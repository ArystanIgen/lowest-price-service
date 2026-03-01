import datetime

from enum import StrEnum
from decimal import Decimal
from sqlalchemy import Date, String, Numeric, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class PriceType(StrEnum):
    REGULAR = "regular"
    PROMO = "promo"


class PriceModel(BaseModel):
    __tablename__ = "prices"

    article_number: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        index=True,
    )
    start_date: Mapped[datetime.date | None] = mapped_column(
        Date,
        nullable=True,
    )
    end_date: Mapped[datetime.date | None] = mapped_column(
        Date,
        nullable=True,
    )
    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    price_type: Mapped[PriceType] = mapped_column(
        SAEnum(PriceType),
        nullable=False,
    )
