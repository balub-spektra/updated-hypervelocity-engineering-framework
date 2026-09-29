"""Configuration loading."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

ENV_INPUT_PATH = "PIPELINE_INPUT_PATH"
ENV_OUTPUT_DIR = "PIPELINE_OUTPUT_DIR"
ENV_WRITER = "PIPELINE_WRITER"

DEFAULT_INPUT_PATH = "data/sample_records.csv"
DEFAULT_OUTPUT_DIR = "output"
DEFAULT_WRITER = "local"

SUPPORTED_WRITERS: tuple[str, ...] = ("local",)


class ConfigError(Exception):
    """Raised when pipeline configuration is invalid."""


@dataclass(frozen=True)
class PipelineConfig:
    """Resolved pipeline configuration.

    Attributes:
        input_path: CSV file to read.
        output_dir: Directory used by the local writer.
        writer: Name of the writer to use. Must be in ``SUPPORTED_WRITERS``.
    """

    input_path: Path
    output_dir: Path
    writer: str = DEFAULT_WRITER


def load_config(env: Mapping[str, str] | None = None) -> PipelineConfig:
    """Load configuration from environment variables.

    Args:
        env: Mapping to read from. Defaults to ``os.environ``.

    Returns:
        The resolved configuration.

    Raises:
        ConfigError: If the requested writer is not supported.
    """
    source = os.environ if env is None else env
    writer = source.get(ENV_WRITER, DEFAULT_WRITER).strip().lower()
    if writer not in SUPPORTED_WRITERS:
        supported = ", ".join(SUPPORTED_WRITERS)
        raise ConfigError(f"Unsupported writer {writer!r}. Supported writers: {supported}")

    return PipelineConfig(
        input_path=Path(source.get(ENV_INPUT_PATH, DEFAULT_INPUT_PATH)),
        output_dir=Path(source.get(ENV_OUTPUT_DIR, DEFAULT_OUTPUT_DIR)),
        writer=writer,
    )
