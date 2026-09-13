import logging
import time
from datetime import UTC, datetime
from pathlib import Path


def setup_logging(log_dir: Path) -> None:
    """Log to the terminal and timestamped file."""
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"pipeline_{datetime.now(UTC):%Y-%m-%d_%H-%M-%S}.log"
    logging.Formatter.converter = time.gmtime
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
        force=True,
    )
    logging.getLogger(__name__).info(f"Logging to {log_file}")
