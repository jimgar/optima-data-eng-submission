"""End-to-end: run the whole pipeline on a tiny bit of mock data in a temp dir."""

import json
from pathlib import Path

from main import main

RACES_CSV = """\
raceId,year,round,name,date,time
1,2024,1,Bahrain Grand Prix,2024-03-02,15:00:00
2,2018,1,Australian Grand Prix,2018-03-25,null
"""

RESULTS_CSV = """\
resultId,raceId,driverId,position,fastestLapTime
10,1,44,1,01:32.6
11,1,1,2,01:31.4
12,2,5,1,null
"""


def test_main(tmp_path: Path) -> None:
    data_path = tmp_path / "source-data"
    results_path = tmp_path / "results"
    data_path.mkdir()
    results_path.mkdir()
    (data_path / "races.csv").write_text(RACES_CSV)
    (data_path / "results.csv").write_text(RESULTS_CSV)

    main(data_path=data_path, results_path=results_path)

    # Expected files are produced
    assert sorted(p.name for p in results_path.glob("*.json")) == [
        "stats_2018.json",
        "stats_2024.json",
    ]

    # Expected content from a "normal" year, i.e. no nulls
    assert json.loads((results_path / "stats_2024.json").read_text()) == [
        {
            "Race Name": "Bahrain Grand Prix",
            "Race Round": 1,
            "Race Datetime": "2024-03-02T15:00:00.000",
            "Race Winning driverId": 44,
            "Race Fastest Lap": "01:31.4",
        }
    ]

    # Null race time becomes midnight; an all-null fastest lap stays null.
    assert json.loads((results_path / "stats_2018.json").read_text()) == [
        {
            "Race Name": "Australian Grand Prix",
            "Race Round": 1,
            "Race Datetime": "2018-03-25T00:00:00.000",
            "Race Winning driverId": 5,
            "Race Fastest Lap": None,
        }
    ]

    # A log file got produced
    assert len(list((results_path / "logs").glob("pipeline_*.log"))) == 1
