"""Tests for LocalFileWriter."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

import pytest

from pipeline.models import Batch, Record
from pipeline.writers import LocalFileWriter, WriterError
from pipeline.writers import local_writer as local_writer_module


def make_batch(count: int = 3, batch_id: str = "batch") -> Batch:
    records = tuple(
        Record(
            record_id=f"r-{index}",
            customer_id="c-1",
            event_type="purchase",
            amount=Decimal("1.25"),
            occurred_at=datetime(2024, 3, 1, tzinfo=timezone.utc),
        )
        for index in range(count)
    )
    return Batch(batch_id=batch_id, records=records)


def test_write_creates_jsonl_file(tmp_path: Path) -> None:
    result = LocalFileWriter(tmp_path).write(make_batch())

    destination = tmp_path / "batch.jsonl"
    assert result.destination == str(destination)
    assert result.records_written == 3
    lines = destination.read_text(encoding="utf-8").splitlines()
    assert [json.loads(line)["record_id"] for line in lines] == ["r-0", "r-1", "r-2"]


def test_write_creates_missing_output_directory(tmp_path: Path) -> None:
    output_dir = tmp_path / "nested" / "out"

    LocalFileWriter(output_dir).write(make_batch())

    assert (output_dir / "batch.jsonl").exists()


def test_write_overwrites_previous_output_for_same_batch(tmp_path: Path) -> None:
    writer = LocalFileWriter(tmp_path)
    writer.write(make_batch(count=3))

    writer.write(make_batch(count=1))

    lines = (tmp_path / "batch.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1


def test_write_rejects_empty_batch(tmp_path: Path) -> None:
    with pytest.raises(WriterError, match="no records"):
        LocalFileWriter(tmp_path).write(make_batch(count=0))

    assert list(tmp_path.iterdir()) == []


def _fail_on_second_dump(monkeypatch: pytest.MonkeyPatch) -> None:
    """Make json.dumps fail on its second call, after one record has been written."""
    real_dumps = json.dumps
    calls = {"count": 0}

    def flaky_dumps(*args: object, **kwargs: object) -> str:
        calls["count"] += 1
        if calls["count"] == 2:
            raise ValueError("cannot serialise record")
        return real_dumps(*args, **kwargs)  # type: ignore[arg-type]

    monkeypatch.setattr(local_writer_module.json, "dumps", flaky_dumps)


def test_write_leaves_no_partial_file_when_serialisation_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _fail_on_second_dump(monkeypatch)

    with pytest.raises(WriterError, match="Failed to write batch 'batch'") as excinfo:
        LocalFileWriter(tmp_path).write(make_batch())

    assert isinstance(excinfo.value.__cause__, ValueError)
    assert list(tmp_path.iterdir()) == []


def test_write_keeps_existing_output_when_a_later_write_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    writer = LocalFileWriter(tmp_path)
    writer.write(make_batch(count=3))
    original = (tmp_path / "batch.jsonl").read_text(encoding="utf-8")
    _fail_on_second_dump(monkeypatch)

    with pytest.raises(WriterError):
        writer.write(make_batch(count=3))

    assert (tmp_path / "batch.jsonl").read_text(encoding="utf-8") == original
    assert not (tmp_path / "batch.jsonl.tmp").exists()


def test_write_reports_unwritable_destination(tmp_path: Path) -> None:
    blocker = tmp_path / "not-a-directory"
    blocker.write_text("occupied", encoding="utf-8")

    with pytest.raises(WriterError, match="Failed to write batch"):
        LocalFileWriter(blocker).write(make_batch())
