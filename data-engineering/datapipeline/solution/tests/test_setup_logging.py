import logging
from pathlib import Path

from logging_config import setup_logging


def test_creates_log_dir_and_timestamped_file_that_receives_messages(
    tmp_path: Path,
) -> None:
    log_dir = tmp_path / "logs"

    setup_logging(log_dir)
    logging.getLogger("test").info("hello from the test")

    (log_file,) = log_dir.glob("pipeline_*.log")
    assert "hello from the test" in log_file.read_text()
