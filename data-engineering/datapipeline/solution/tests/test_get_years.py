import polars as pl
from pipeline import get_years


def test_years_are_deduplicated_and_sorted() -> None:
    df = pl.DataFrame({"year": ["2024", "2018", "2024"]})

    assert get_years(df) == ["2018", "2024"]


def test_single_year() -> None:
    df = pl.DataFrame({"year": ["2024", "2024"]})

    assert get_years(df) == ["2024"]
