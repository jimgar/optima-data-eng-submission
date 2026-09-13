from datetime import UTC, datetime

import polars as pl
from pipeline import filter_year


def test_keeps_only_that_year_in_chronological_order() -> None:
    df = pl.DataFrame(
        {
            "year": ["2024", "2023", "2024"],
            "Race Name": ["Toilet Boiler City", "Rainbow Road", "Banana Peel Swamp"],
            "Race Datetime": [
                datetime(2024, 12, 8, tzinfo=UTC),
                datetime(2023, 3, 5, tzinfo=UTC),
                datetime(2024, 3, 2, tzinfo=UTC),
            ],
        }
    )

    assert filter_year(df, "2024").get_column("Race Name").to_list() == [
        "Banana Peel Swamp",
        "Toilet Boiler City",
    ]
