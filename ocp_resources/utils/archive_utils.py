"""Utilities for archiving and extracting large schema files."""

import gzip
import json
from pathlib import Path
from typing import Any

from simple_logger.logger import get_logger

LOGGER = get_logger(name=__name__)


def save_json_archive(data: dict[str, Any], json_file: Path) -> Path:
    """
    Save JSON data to compressed archive and remove original file.

    Args:
        data: JSON data to save
        json_file: Path to the JSON file (will be compressed to .json.gz)

    Returns:
        Path to the created archive file
    """
    archive_file = json_file.with_suffix(json_file.suffix + ".gz")

    # Save to archive
    with gzip.open(archive_file, "wt", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)

    # Remove original if it exists
    if json_file.exists():
        json_file.unlink()

    LOGGER.info(f"Saved and archived: {archive_file}")
    return archive_file


def load_json_archive(json_file: Path) -> dict[str, Any]:
    """
    Load JSON data from archive file (.json.gz).

    Args:
        json_file: Path to the JSON file (will look for .json.gz)

    Returns:
        Loaded JSON data as dictionary
    """
    archive_file = json_file.with_suffix(json_file.suffix + ".gz")

    LOGGER.info(f"Loading JSON from archive: {archive_file}")
    with gzip.open(archive_file, "rt", encoding="utf-8") as f:
        return json.load(f)
