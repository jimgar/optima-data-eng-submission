from pathlib import Path

import polars as pl
from pipeline import (
    agg_results,
    get_years,
    make_datetime,
    null_times_to_midnight,
    read_data,
    strftime_for_output,
    write_year_result,
)
from schemas import output_schema, schema_races_csv, schema_results_csv

DATA_PATH = Path("source-data")
RESULTS_PATH = Path("results")


def main(data_path: Path = DATA_PATH, results_path: Path = RESULTS_PATH) -> None:
    # Parse

    # I/O of a scan loop theoretically will make worse performance, so just read
    # all into memory (files are miniscule and always will be)
    df_races = read_data(path=data_path / "races.csv", schema=schema_races_csv)
    df_results = read_data(path=data_path / "results.csv", schema=schema_results_csv)

    df_races = make_datetime(null_times_to_midnight(df_races))

    # Aggregate and combine

    df_results_agg = agg_results(df_results)
    joined = (
        df_races.join(df_results_agg, on="raceId", how="left")
        .select(
            [
                "year",
                "name",
                "round",
                "datetime",
                "winning_driverId",
                "race_fastest_lap",
            ]
        )
        .rename(output_schema)
    )

    # Output

    years: list[str] = get_years(joined)

    for year in years:
        filtered = joined.filter(pl.col("year") == year)
        filtered = strftime_for_output(filtered)
        write_year_result(filtered, year, results_path)

    # # No duplicated rows
    # print(df_races.filter(df_races.is_duplicated()))
    # print(df_results.filter(df_results.is_duplicated()))

    # # These need to be unique, and they are. Turn into unit test?
    # # Both = 149
    # print(df_races.select(pl.len()))
    # print(df_races.n_unique(subset=["raceId"]))

    # # These need to be unique, and they are. Turn into unit test?
    # # Both = 2739
    # print(df_results.select(pl.len()))
    # print(df_results.n_unique(subset=["resultId"]))


if __name__ == "__main__":
    main()
