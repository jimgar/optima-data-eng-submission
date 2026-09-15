from datetime import time

import polars as pl
from pipeline import null_times_to_midnight


def test_null_becomes_midnight_and_real_time_is_untouched() -> None:
    df = pl.DataFrame({"time": [time(13, 0), None]}, schema={"time": pl.Time()})

    assert null_times_to_midnight(df).get_column("time").to_list() == [
        time(13, 0),
        time(0, 0),
    ]
