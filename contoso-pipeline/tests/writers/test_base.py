"""Tests for WriterBase behaviour shared by every writer."""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

import pytest

from pipeline.models import Batch, Record
from pipeline.writers import WriteResult, WriterBase, WriterError


def make_batch(count: int = 2) -> Batch:
    records = tuple(
        Record(
            record_id=f"r-{index}",
            customer_id="c-1",
            event_type="purchase",
            amount=Decimal("1.00"),
            occurred_at=datetime(2024, 3, 1, tzinfo=timezone.utc),
        )
        for index in range(count)
    )
    return Batch(batch_id="batch", records=records)


class RecordingWriter(WriterBase):
    """Writer that records what it was asked to write."""

    def __init__(self) -> None:
        self.batches: list[Batch] = []

    def _write(self, batch: Batch) -> WriteResult:
        self.batches.append(batch)
        return WriteResult(destination="memory", records_written=len(batch))


class ExplodingWriter(WriterBase):
    """Writer whose backend fails with a non-writer exception."""

    def _write(self, batch: Batch) -> WriteResult:
        raise RuntimeError("backend exploded")


class TypedFailureWriter(WriterBase):
    """Writer that already raises WriterError."""

    def _write(self, batch: Batch) -> WriteResult:
        raise WriterError("typed failure")


def test_base_class_cannot_be_instantiated() -> None:
    with pytest.raises(TypeError):
        WriterBase()  # type: ignore[abstract]


def test_write_delegates_to_subclass() -> None:
    writer = RecordingWriter()
    batch = make_batch()

    result = writer.write(batch)

    assert writer.batches == [batch]
    assert result == WriteResult(destination="memory", records_written=2)


def test_write_rejects_empty_batch() -> None:
    writer = RecordingWriter()

    with pytest.raises(WriterError, match="no records"):
        writer.write(make_batch(count=0))

    assert writer.batches == []


def test_write_wraps_unexpected_exceptions() -> None:
    with pytest.raises(WriterError, match="backend exploded") as excinfo:
        ExplodingWriter().write(make_batch())

    assert isinstance(excinfo.value.__cause__, RuntimeError)


def test_write_does_not_rewrap_writer_errors() -> None:
    with pytest.raises(WriterError, match="^typed failure$"):
        TypedFailureWriter().write(make_batch())
