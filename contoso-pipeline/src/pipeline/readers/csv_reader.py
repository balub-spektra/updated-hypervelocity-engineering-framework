"""CSV source data reader."""

from __future__ import annotations

import csv
import logging
from pathlib import Path

from pipeline.models import REQUIRED_FIELDS, Batch, Record

logger = logging.getLogger(__name__)


class ReaderError(Exception):
    """Raised when source data cannot be read."""


class CsvReader:
    """Reads a CSV file into a single batch."""

    def read(self, path: Path) -> Batch:
        """Read every row of a CSV file.

        The batch identifier is the file name without its extension.

        Args:
            path: Path of the CSV file.

        Returns:
            A batch containing one record per row.

        Raises:
            ReaderError: If the file is missing, has no header, lacks a required
                column, or contains a row that cannot be parsed.
        """
        try:
            handle = path.open("r", encoding="utf-8", newline="")
        except OSError as exc:
            raise ReaderError(f"Cannot open {path}: {exc}") from exc

        with handle:
            reader = csv.DictReader(handle)
            fieldnames = reader.fieldnames or []
            absent = [name for name in REQUIRED_FIELDS if name not in fieldnames]
            if absent:
                raise ReaderError(f"{path} is missing column(s): {', '.join(absent)}")

            records: list[Record] = []
            for row in reader:
                try:
                    records.append(Record.from_row(row))
                except ValueError as exc:
                    raise ReaderError(f"{path} line {reader.line_num}: {exc}") from exc

        logger.info("Read %d records from %s", len(records), path)
        return Batch(batch_id=path.stem, records=tuple(records))
