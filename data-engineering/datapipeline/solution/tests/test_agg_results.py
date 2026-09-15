"""Tests for agg_results, in particular the string-min fastest lap and its format assumption."""

import polars as pl
from pipeline import agg_results


def test_fastest_lap_is_alphabetical_min() -> None:
    df = pl.DataFrame(
        {
            "raceId": [1, 1, 1],
            "driverId": [10, 20, 30],
            "position": [1, 2, 3],
            "fastestLapTime": ["01:29.4", "00:59.6", "01:07.3"],
        }
    )

    assert agg_results(df).get_column("race_fastest_lap").to_list() == ["00:59.6"]


def test_fastest_lap_ignores_nulls() -> None:
    df = pl.DataFrame(
        {
            "raceId": [1, 1],
            "driverId": [10, 20],
            "position": [1, 2],
            "fastestLapTime": [None, "01:30.0"],
        }
    )

    assert agg_results(df).get_column("race_fastest_lap").to_list() == ["01:30.0"]


def test_fastest_lap_is_null_when_all_laps_null() -> None:
    df = pl.DataFrame(
        {
            "raceId": [1, 1],
            "driverId": [10, 20],
            "position": [1, 2],
            "fastestLapTime": [None, None],
        },
        schema_overrides={"fastestLapTime": pl.String()},
    )

    assert agg_results(df).get_column("race_fastest_lap").to_list() == [None]


def test_winner_is_driver_in_position_one() -> None:
    df = pl.DataFrame(
        {
            "raceId": [1, 1, 1],
            "driverId": [10, 20, 30],
            "position": [2, 1, None],
            "fastestLapTime": ["01:30.0", "01:31.0", None],
        }
    )

    assert agg_results(df).get_column("winning_driverId").to_list() == [20]


def test_no_driver_in_position_one_gives_null_winner() -> None:
    df = pl.DataFrame(
        {
            "raceId": [1, 1],
            "driverId": [10, 20],
            "position": [2, 3],
            "fastestLapTime": ["01:30.0", "01:31.0"],
        }
    )

    assert agg_results(df).get_column("winning_driverId").to_list() == [None]
