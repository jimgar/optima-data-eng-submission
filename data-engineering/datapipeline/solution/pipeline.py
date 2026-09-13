from datetime import time
from pathlib import Path

import polars as pl


def read_data(path: Path, schema: pl.Schema) -> pl.DataFrame:
    return pl.read_csv(source=path, null_values="null", schema=schema)


def null_times_to_midnight(df: pl.DataFrame) -> pl.DataFrame:
    """Missing race times get 00:00:00."""
    return df.with_columns(time=pl.col("time").fill_null(time(0, 0, 0)))


def make_datetime(df: pl.DataFrame) -> pl.DataFrame:
    """Combine; make UTC explicit"""
    return df.with_columns(
        datetime=pl.col("date").dt.combine(pl.col("time")).dt.replace_time_zone("UTC")
    )


def agg_results(df: pl.DataFrame) -> pl.DataFrame:
    """Aggregate results for each race so they can cleanly join onto the top-level race data."""
    return df.group_by("raceId", maintain_order=True).agg(
        winning_driverId=pl.col("driverId").filter(pl.col("position") == 1).first(),
        race_fastest_lap=pl.col("fastestLapTime").min(),
    )


def get_years(df: pl.DataFrame) -> list[str]:
    return df.get_column("year").unique().sort().to_list()


def filter_year(df: pl.DataFrame, year: str) -> pl.DataFrame:
    """Races for one year in asc order."""
    return df.filter(pl.col("year") == year).sort(pl.col("Race Datetime"))


def strftime_for_output(df: pl.DataFrame) -> pl.DataFrame:
    """Render `Race Datetime` as e.g. "2024-07-07T14:00:00.000" to match the README."""
    return df.with_columns(pl.col("Race Datetime").dt.strftime("%Y-%m-%dT%H:%M:%S%.3f"))


def write_year_result(df: pl.DataFrame, year: str, results_path: Path) -> None:
    df.drop("year").write_json(results_path / f"stats_{year}.json")
