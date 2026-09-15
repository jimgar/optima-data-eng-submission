from datetime import UTC, datetime

import polars as pl
from pipeline import strftime_for_output


def test_matches_readme_format() -> None:
    df = pl.DataFrame({"Race Datetime": [datetime(2024, 7, 7, 14, 0, tzinfo=UTC)]})

    assert strftime_for_output(df).get_column("Race Datetime").to_list() == [
        "2024-07-07T14:00:00.000"
    ]
