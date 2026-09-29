"""Abstract base class shared by every output writer."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass

from pipeline.models import Batch

logger = logging.getLogger(__name__)


class WriterError(Exception):
    """Raised when a batch cannot be written.

    Every writer reports failure with this exception type so callers never
    need to know which backend is in use.
    """


@dataclass(frozen=True)
class WriteResult:
    """Outcome of a successful write.

    Attributes:
        destination: Where the batch was written, for example a file path.
        records_written: Number of records written.
    """

    destination: str
    records_written: int


class WriterBase(ABC):
    """Base class for output writers.

    Subclasses implement ``_write``. Callers use ``write``, which validates the
    batch and guarantees that any failure surfaces as a ``WriterError``.

    A writer must be atomic. If ``_write`` fails, no partial output may remain
    at the destination.
    """

    def write(self, batch: Batch) -> WriteResult:
        """Write a batch to the destination.

        Args:
            batch: The batch to write. Must contain at least one record.

        Returns:
            Details of the completed write.

        Raises:
            WriterError: If the batch is empty or the write fails.
        """
        if len(batch) == 0:
            raise WriterError(f"Batch {batch.batch_id!r} has no records")

        try:
            result = self._write(batch)
        except WriterError:
            raise
        except Exception as exc:
            raise WriterError(f"Unexpected failure writing batch {batch.batch_id!r}: {exc}") from exc

        logger.info("Wrote %d records to %s", result.records_written, result.destination)
        return result

    @abstractmethod
    def _write(self, batch: Batch) -> WriteResult:
        """Write a validated, non-empty batch.

        Implementations must leave no partial output behind on failure and
        should raise ``WriterError`` with a descriptive message.
        """
