import csv
from collections.abc import Sequence
from pathlib import Path

import pytest

REGULAR_PRICE_FIELDNAMES = (
    "ArtikelNummer",
    "ArtikelDatum",
    "IngangsDatumPrijs",
    "EindDatumPrijs",
    "Prijs",
)
PROMO_PRICE_FIELDNAMES = (
    "ActiePeriode",
    "PromotieNummer",
    "ArtikelNummer",
    "ArtikelDatum",
    "PromotieOmschrijving",
    "StartDatumPromotie",
    "EindDatumPromotie",
    "Status",
    "VanPrijs",
    "VoorPrijs",
)


def _write_csv(
    csv_path: Path,
    fieldnames: Sequence[str],
    rows: list[dict[str, str]],
) -> Path:
    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return csv_path


@pytest.fixture
def mock_regular_price_rows() -> list[dict[str, str]]:
    return [
        {
            "ArtikelNummer": "100153",
            "ArtikelDatum": "12/06/91",
            "IngangsDatumPrijs": "2026-02-10",
            "EindDatumPrijs": "2026-02-28",
            "Prijs": "25.71",
        },
        {
            "ArtikelNummer": "219916",
            "ArtikelDatum": "29/07/14",
            "IngangsDatumPrijs": "15/02/26",
            "EindDatumPrijs": "null",
            "Prijs": "11.59",
        },
    ]


@pytest.fixture
def mock_regular_prices_csv_file_path(
    tmp_path: Path,
    mock_regular_price_rows: list[dict[str, str]],
) -> Path:
    return _write_csv(
        tmp_path / "regular_prices.csv",
        REGULAR_PRICE_FIELDNAMES,
        mock_regular_price_rows,
    )


@pytest.fixture
def mock_promo_price_rows() -> list[dict[str, str]]:
    return [
        {
            "ActiePeriode": "1115",
            "PromotieNummer": "128",
            "ArtikelNummer": "219916",
            "ArtikelDatum": "29/07/14",
            "PromotieOmschrijving": "13 ROSE BL.ZWEIGELT 2018",
            "StartDatumPromotie": "2026-02-14",
            "EindDatumPromotie": "2026-02-21",
            "Status": "40",
            "VanPrijs": "12.58",
            "VoorPrijs": "11.59",
        },
        {
            "ActiePeriode": "1116",
            "PromotieNummer": "204",
            "ArtikelNummer": "781460",
            "ArtikelDatum": "14/06/00",
            "PromotieOmschrijving": "ABSOLUT CITRON 70CL",
            "StartDatumPromotie": "2026-02-22",
            "EindDatumPromotie": "2026-03-05",
            "Status": "40",
            "VanPrijs": "23.58",
            "VoorPrijs": "20.41",
        },
    ]


@pytest.fixture
def mock_promo_prices_csv_file_path(
    tmp_path: Path,
    mock_promo_price_rows: list[dict[str, str]],
) -> Path:
    return _write_csv(
        tmp_path / "promo_prices.csv",
        PROMO_PRICE_FIELDNAMES,
        mock_promo_price_rows,
    )
