from fastapi import APIRouter, HTTPException, status

from app.api.deps.repos import PriceRepoDep
from app.api.deps.session import AsyncSessionDep
from app.schemas.price import LowestPriceOut

router = APIRouter()


@router.get(
    "/lowest-prices",
    status_code=status.HTTP_200_OK,
    response_model=list[LowestPriceOut],
    summary="Get the lowest prices for all articles",
    description="Returns the lowest prices for all articles "
                "in the last 30 days, "
                "considering both regular and promotional prices",
    operation_id="getLowestPrices",
    response_description="Lowest prices for all articles",
)
async def get_lowest_prices_api(
    async_session: AsyncSessionDep,
    price_repo: PriceRepoDep,
) -> list[LowestPriceOut]:
    fetched_prices = await price_repo.get_lowest_prices_for_all_articles(
        async_session=async_session,
        days=30,
    )

    return [LowestPriceOut(**price) for price in fetched_prices]


@router.get(
    "/{article_number}/lowest-price",
    status_code=status.HTTP_200_OK,
    response_model=LowestPriceOut,
    summary="Get the lowest price for a specific article",
    description="Returns the lowest price for a specific article "
                "in the last 30 days, "
                "considering both regular and promotional prices",
    operation_id="getLowestPrice",
    response_description="Lowest price for a specific article",
)
async def get_article_lowest_price_api(
    article_number: str,
    async_session: AsyncSessionDep,
    price_repo: PriceRepoDep,
) -> LowestPriceOut:
    fetched_price = await price_repo.get_lowest_price_for_article(
        async_session=async_session,
        article_number=article_number,
        days=30,
    )

    if not fetched_price:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No price data found for article {article_number} "
                   f"in the last 30 days",
        )

    return LowestPriceOut(**fetched_price)
