from pathlib import Path

import polars as pl
import pytest
from pipeline import read_data


def test_reads_with_schema_and_treats_literal_null_as_missing(tmp_path: Path) -> None:
    csv = tmp_path / "in.csv"
    csv.write_text("id,lap\n1,01:29.4\n2,null\n")
    schema = pl.Schema({"id": pl.UInt8(), "lap": pl.String()})

    df = read_data(csv, schema)

    assert df.schema == schema
    assert df.get_column("lap").to_list() == ["01:29.4", None]


def test_raises_when_value_does_not_fit_schema(tmp_path: Path) -> None:
    csv = tmp_path / "in.csv"
    csv.write_text("id\nabc\n")

    with pytest.raises(pl.exceptions.ComputeError):
        read_data(csv, pl.Schema({"id": pl.UInt8()}))
