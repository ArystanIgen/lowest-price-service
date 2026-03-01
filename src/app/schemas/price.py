from pydantic import BaseModel, Field


class PriceCreate(BaseModel):
    article_number: str = Field(..., description="Article number")
    start_date: str = Field(..., description="Start date of the price")
    end_date: str = Field(..., description="End date of the price")
    price: float = Field(..., description="Price")


class PriceUpdate(BaseModel):
    article_number: str = Field(..., description="Article number")
    start_date: str = Field(..., description="Start date of the price")
    end_date: str = Field(..., description="End date of the price")
    price: float = Field(..., description="Price")
    price_type: str = Field(..., description="Price type")
