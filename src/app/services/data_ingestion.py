import asyncio
import csv
from datetime import datetime, date
from decimal import Decimal
from pathlib import Path

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import CONFIG
from app.db.session import async_session_factory
from app.models.price import PriceType
from app.repositories.price import PriceRepository
from app.schemas.price import PriceCreate

price_repo = PriceRepository()


def parse_date(date_str: str | None) -> date | None:
    if not date_str or date_str.strip().lower() == "null":
        return None

    date_str = date_str.strip()
    try:
        dt = datetime.strptime(date_str, "%d/%m/%y")
        return dt.date()
    except ValueError:
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.date()
        except ValueError:
            logger.error(f"Failed to parse date: {date_str}")
            raise


async def ingest_regular_prices(
    async_session: AsyncSession, file_path: str | None = None
) -> int:
    if file_path is None:
        file_path = CONFIG.regular_prices_csv_file_path

    csv_path = Path(file_path)
    if not csv_path.exists():
        csv_path = Path("src") / file_path
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {file_path}")

    logger.info(f"Ingesting regular prices from {csv_path}")

    price_records: list[PriceCreate] = []

    with open(csv_path, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                price_record = PriceCreate(
                    article_number=row["ArtikelNummer"].strip(),
                    start_date=parse_date(row["IngangsDatumPrijs"]),
                    end_date=parse_date(row["EindDatumPrijs"]),
                    price=Decimal(row["Prijs"]),
                    price_type=PriceType.REGULAR,
                )
                price_records.append(price_record)
            except Exception as e:
                logger.warning(f"Failed to parse row: {row}. Error: {e}")
                continue

    # Bulk insert
    if price_records:
        await price_repo.create_bulk(
            async_session=async_session, objs_in=price_records
        )
        logger.info(
            f"Successfully ingested {len(price_records)} regular prices"
        )

    return len(price_records)


async def ingest_promo_prices(
    async_session: AsyncSession, file_path: str | None = None
) -> int:
    if file_path is None:
        file_path = CONFIG.promo_prices_csv_file_path

    csv_path = Path(file_path)
    if not csv_path.exists():
        csv_path = Path("src") / file_path
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {file_path}")

    logger.info(f"Ingesting promo prices from {csv_path}")

    price_records: list[PriceCreate] = []

    with open(csv_path, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                # Use 'VoorPrijs' (promotional price) as the price
                price_record = PriceCreate(
                    article_number=row["ArtikelNummer"].strip(),
                    start_date=parse_date(row["StartDatumPromotie"]),
                    end_date=parse_date(row["EindDatumPromotie"]),
                    price=Decimal(row["VoorPrijs"]),
                    price_type=PriceType.PROMO,
                )
                price_records.append(price_record)
            except Exception as e:
                logger.warning(f"Failed to parse row: {row}. Error: {e}")
                continue

    # Bulk insert
    if price_records:
        await price_repo.create_bulk(
            async_session=async_session, objs_in=price_records
        )
        logger.info(
            f"Successfully ingested {len(price_records)} promo prices"
        )

    return len(price_records)


async def ingest_all() -> None:
    async with async_session_factory() as async_session:
        regular_count = await ingest_regular_prices(
            async_session=async_session
        )
        promo_count = await ingest_promo_prices(
            async_session=async_session
        )

        logger.info(
            f"Done! Ingested total of {regular_count} Regular Prices "
            f"and {promo_count} Promo Prices."
        )


if __name__ == "__main__":
    asyncio.run(ingest_all())
