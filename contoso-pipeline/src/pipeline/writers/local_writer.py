"""Writer that stores batches as JSON Lines files on local disk."""

from __future__ import annotations

import json
import logging
from pathlib import Path

from pipeline.models import Batch
from pipeline.writers.base import WriteResult, WriterBase, WriterError

logger = logging.getLogger(__name__)


class LocalFileWriter(WriterBase):
    """Writes each batch to ``<output_dir>/<batch_id>.jsonl``.

    Records are first written to a temporary file next to the destination and
    then moved into place. A failure part-way through therefore never leaves a
    partially written destination file, and never damages an existing one.
    """

    def __init__(self, output_dir: Path) -> None:
        """Create a writer.

        Args:
            output_dir: Directory to write into. Created if it does not exist.
        """
        self._output_dir = output_dir

    def _write(self, batch: Batch) -> WriteResult:
        final_path = self._output_dir / f"{batch.batch_id}.jsonl"
        temp_path = self._output_dir / f"{batch.batch_id}.jsonl.tmp"

        try:
            self._output_dir.mkdir(parents=True, exist_ok=True)
            with temp_path.open("w", encoding="utf-8") as handle:
                for record in batch:
                    handle.write(json.dumps(record.to_dict()) + "\n")
            temp_path.replace(final_path)
        except (OSError, TypeError, ValueError) as exc:
            self._discard(temp_path)
            raise WriterError(f"Failed to write batch {batch.batch_id!r} to {final_path}: {exc}") from exc

        return WriteResult(destination=str(final_path), records_written=len(batch))

    @staticmethod
    def _discard(path: Path) -> None:
        """Remove a temporary file, ignoring the case where it does not exist."""
        try:
            path.unlink(missing_ok=True)
        except OSError:
            logger.warning("Could not remove temporary file %s", path)
