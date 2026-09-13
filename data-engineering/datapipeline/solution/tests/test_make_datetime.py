from datetime import UTC, date, datetime, time

import polars as pl
from pipeline import make_datetime


def test_combines_date_and_time_into_utc_datetime() -> None:
    df = pl.DataFrame(
        {"date": [date(2024, 7, 7)], "time": [time(14, 0)]},
        schema={"date": pl.Date(), "time": pl.Time()},
    )

    out = make_datetime(df)

    assert out.schema["datetime"] == pl.Datetime("us", "UTC")
    assert out.get_column("datetime").to_list() == [
        datetime(2024, 7, 7, 14, 0, tzinfo=UTC)
    ]
