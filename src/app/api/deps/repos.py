from typing import Annotated

from fastapi import Depends

from app.repositories import PriceRepository


def get_price_repo() -> PriceRepository:
    return PriceRepository()


PriceRepoDep = Annotated[PriceRepository, Depends(get_price_repo)]
