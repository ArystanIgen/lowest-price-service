from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field

from app.models.price import PriceType


class PriceCreate(BaseModel):
    article_number: str = Field(..., description="Article number")
    start_date: date | None = Field(..., description="Start date of the price")
    end_date: date | None = Field(..., description="End date of the price")
    price: Decimal = Field(..., description="Price")
    price_type: PriceType = Field(..., description="Price type")


class PriceUpdate(BaseModel):
    article_number: str | None = Field(..., description="Article number")
    start_date: date | None = Field(..., description="Start date of the price")
    end_date: date | None = Field(..., description="End date of the price")
    price: Decimal | None = Field(..., description="Price")
    price_type: PriceType | None = Field(..., description="Price type")


class LowestPriceOut(BaseModel):
    article_number: str = Field(..., description="Article number")
    lowest_price: float = Field(..., description="Lowest price")
