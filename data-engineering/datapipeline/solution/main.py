import logging
from pathlib import Path

from logging_config import setup_logging
from pipeline import (
    agg_results,
    filter_year,
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

logger = logging.getLogger(__name__)


def main(data_path: Path = DATA_PATH, results_path: Path = RESULTS_PATH) -> None:
    setup_logging(results_path / "logs")
    logger.info("Pipeline started")

    # Parse

    # I/O of a scan loop theoretically will make worse performance, so just read
    # all into memory (files are miniscule and always will be)
    races_path = data_path / "races.csv"
    df_races = read_data(path=races_path, schema=schema_races_csv)
    logger.info(f"Read {df_races.height} races from {races_path}")

    race_results_path = data_path / "results.csv"
    df_results = read_data(path=race_results_path, schema=schema_results_csv)
    logger.info(f"Read {df_results.height} results from {race_results_path}")

    df_races = make_datetime(null_times_to_midnight(df_races))

    # Aggregate and combine

    df_results_agg = agg_results(df_results)
    logger.info(f"Aggregated results for {df_results_agg.height} races")
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
    logger.info(f"Years to process: {years}")

    for year in years:
        filtered = filter_year(joined, year)
        filtered = strftime_for_output(filtered)
        write_year_result(filtered, year, results_path)
        logger.info(f"Wrote {filtered.height} races for {year}")

    logger.info("All files written!")

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
