import json
from pathlib import Path

import polars as pl
from pipeline import write_year_result


def test_writes_named_file_without_year_key(tmp_path: Path) -> None:
    df = pl.DataFrame({"year": ["2024"], "Race Name": ["A"], "Race Round": [1]})

    write_year_result(df, "2024", tmp_path)

    written = json.loads((tmp_path / "stats_2024.json").read_text())
    assert written == [{"Race Name": "A", "Race Round": 1}]
