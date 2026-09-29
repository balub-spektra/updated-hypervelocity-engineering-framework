"""Record and batch data models."""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation

REQUIRED_FIELDS: tuple[str, ...] = (
    "record_id",
    "customer_id",
    "event_type",
    "amount",
    "occurred_at",
)


@dataclass(frozen=True)
class Record:
    """A single source record.

    Attributes:
        record_id: Unique identifier of the record.
        customer_id: Identifier of the customer the record belongs to.
        event_type: Kind of event, for example ``purchase`` or ``refund``.
        amount: Monetary amount. Negative for refunds.
        occurred_at: Timestamp of the event.
    """

    record_id: str
    customer_id: str
    event_type: str
    amount: Decimal
    occurred_at: datetime

    @classmethod
    def from_row(cls, row: Mapping[str, str]) -> Record:
        """Build a record from a mapping of string fields.

        Args:
            row: Mapping containing every field in ``REQUIRED_FIELDS``.

        Returns:
            The parsed record.

        Raises:
            ValueError: If a field is missing, empty, or cannot be parsed.
        """
        missing = [name for name in REQUIRED_FIELDS if not (row.get(name) or "").strip()]
        if missing:
            raise ValueError(f"Missing required field(s): {', '.join(missing)}")

        try:
            amount = Decimal(row["amount"].strip())
        except InvalidOperation as exc:
            raise ValueError(f"Invalid amount: {row['amount']!r}") from exc

        try:
            occurred_at = datetime.fromisoformat(row["occurred_at"].strip())
        except ValueError as exc:
            raise ValueError(f"Invalid timestamp: {row['occurred_at']!r}") from exc

        return cls(
            record_id=row["record_id"].strip(),
            customer_id=row["customer_id"].strip(),
            event_type=row["event_type"].strip(),
            amount=amount,
            occurred_at=occurred_at,
        )

    def to_dict(self) -> dict[str, str]:
        """Return a JSON-serialisable representation of the record."""
        return {
            "record_id": self.record_id,
            "customer_id": self.customer_id,
            "event_type": self.event_type,
            "amount": str(self.amount),
            "occurred_at": self.occurred_at.isoformat(),
        }


@dataclass(frozen=True)
class Batch:
    """An ordered group of records that is written as one unit.

    Attributes:
        batch_id: Identifier of the batch. Used to name the written output.
        records: The records in the batch.
    """

    batch_id: str
    records: tuple[Record, ...]

    def __len__(self) -> int:
        return len(self.records)

    def __iter__(self) -> Iterator[Record]:
        return iter(self.records)
