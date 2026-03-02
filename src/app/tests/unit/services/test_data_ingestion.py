from datetime import date
from pathlib import Path

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.price import PriceType
from app.repositories.price import PriceRepository
from app.services import data_ingestion

price_repo = PriceRepository()


@pytest.mark.asyncio
async def test_ingest_regular_prices_creates_price_records(
    async_session: AsyncSession,
    mock_regular_prices_csv_file_path: Path,
):
    inserted_rows = await data_ingestion.ingest_regular_prices(
        async_session=async_session,
        file_path=str(mock_regular_prices_csv_file_path),
    )

    stored_prices = await price_repo.get_multi(async_session)

    assert inserted_rows == 2
    assert len(stored_prices) == 2
    assert stored_prices[0].article_number == "100153"
    assert stored_prices[0].price_type == PriceType.REGULAR
    assert stored_prices[0].start_date == date(2026, 2, 10)
    assert stored_prices[0].end_date == date(2026, 2, 28)
    assert stored_prices[1].article_number == "219916"
    assert stored_prices[1].end_date is None



@pytest.mark.asyncio
async def test_ingest_promo_prices_uses_promotional_price(
    async_session: AsyncSession,
    mock_promo_prices_csv_file_path: Path,
):
    inserted_rows = await data_ingestion.ingest_promo_prices(
        async_session=async_session,
        file_path=str(mock_promo_prices_csv_file_path),
    )

    stored_prices = await price_repo.get_multi(async_session)

    assert inserted_rows == 2
    assert len(stored_prices) == 2
    assert stored_prices[0].price_type == PriceType.PROMO
    assert float(stored_prices[0].price) == pytest.approx(11.59)
    assert float(stored_prices[1].price) == pytest.approx(20.41)


@pytest.mark.asyncio
async def test_ingest_regular_prices_raises_for_missing_files():
    with pytest.raises(FileNotFoundError):
        await data_ingestion.ingest_regular_prices(
            async_session=None,  # type: ignore[arg-type]
            file_path="missing.csv",
        )
