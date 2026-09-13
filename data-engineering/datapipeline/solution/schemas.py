import polars as pl

schema_races_csv: pl.Schema = pl.Schema(
    {
        "raceId": pl.UInt16(),  # Max 65,535. Even after 500 years of 2 races/month there would only be 10,000.
        "year": pl.String(),
        "round": pl.UInt8(),  # Max 255. There are no more than 24 races per year.
        "name": pl.String(),
        "date": pl.Date(),
        "time": pl.Time(),
    }
)

schema_results_csv: pl.Schema = pl.Schema(
    {
        "resultId": pl.UInt32(),
        "raceId": pl.UInt16(),
        "driverId": pl.UInt16(),
        "position": pl.UInt8(),  # Only 22 drivers per race
        "fastestLapTime": pl.String(),
    }
)

output_schema = {
    "name": "Race Name",
    "round": "Race Round",
    "datetime": "Race Datetime",
    "winning_driverId": "Race Winning driverId",
    "race_fastest_lap": "Race Fastest Lap",
}
