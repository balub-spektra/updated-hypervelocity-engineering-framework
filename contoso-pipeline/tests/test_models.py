"""Tests for the data models and the CSV reader."""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

import pytest

from pipeline.models import Batch, Record
from pipeline.readers import CsvReader, ReaderError

ROW = {
    "record_id": "r-1",
    "customer_id": "c-1",
    "event_type": "purchase",
    "amount": "12.50",
    "occurred_at": "2024-03-01T09:15:00+00:00",
}


def test_record_from_row_parses_fields() -> None:
    record = Record.from_row(ROW)

    assert record.record_id == "r-1"
    assert record.amount == Decimal("12.50")
    assert record.occurred_at == datetime(2024, 3, 1, 9, 15, tzinfo=timezone.utc)


def test_record_to_dict_is_json_friendly() -> None:
    assert Record.from_row(ROW).to_dict() == ROW


@pytest.mark.parametrize("field", list(ROW))
def test_record_from_row_rejects_missing_field(field: str) -> None:
    row = {**ROW, field: ""}

    with pytest.raises(ValueError, match=field):
        Record.from_row(row)


def test_record_from_row_rejects_bad_amount() -> None:
    with pytest.raises(ValueError, match="Invalid amount"):
        Record.from_row({**ROW, "amount": "abc"})


def test_record_from_row_rejects_bad_timestamp() -> None:
    with pytest.raises(ValueError, match="Invalid timestamp"):
        Record.from_row({**ROW, "occurred_at": "yesterday"})


def test_batch_reports_length_and_iterates() -> None:
    record = Record.from_row(ROW)
    batch = Batch(batch_id="b", records=(record, record))

    assert len(batch) == 2
    assert list(batch) == [record, record]


def test_csv_reader_reads_sample_data() -> None:
    sample = Path(__file__).resolve().parent.parent / "data" / "sample_records.csv"

    batch = CsvReader().read(sample)

    assert batch.batch_id == "sample_records"
    assert len(batch) == 10
    assert batch.records[0].record_id == "r-0001"


def test_csv_reader_reports_missing_file(tmp_path: Path) -> None:
    with pytest.raises(ReaderError, match="Cannot open"):
        CsvReader().read(tmp_path / "missing.csv")


def test_csv_reader_reports_missing_column(tmp_path: Path) -> None:
    path = tmp_path / "bad.csv"
    path.write_text("record_id,customer_id\nr-1,c-1\n", encoding="utf-8")

    with pytest.raises(ReaderError, match="missing column"):
        CsvReader().read(path)


def test_csv_reader_reports_bad_row_with_line_number(tmp_path: Path) -> None:
    path = tmp_path / "bad_row.csv"
    path.write_text(
        "record_id,customer_id,event_type,amount,occurred_at\n"
        "r-1,c-1,purchase,not-a-number,2024-03-01T09:15:00+00:00\n",
        encoding="utf-8",
    )

    with pytest.raises(ReaderError, match="line 2"):
        CsvReader().read(path)
