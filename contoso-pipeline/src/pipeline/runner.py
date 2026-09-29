"""Pipeline orchestration entry point."""

from __future__ import annotations

import argparse
import logging
import sys
from collections.abc import Sequence

from pipeline.config import ConfigError, PipelineConfig, load_config
from pipeline.readers import CsvReader, ReaderError
from pipeline.writers import LocalFileWriter, WriteResult, WriterBase, WriterError

logger = logging.getLogger(__name__)


def build_writer(config: PipelineConfig) -> WriterBase:
    """Create the writer selected by the configuration.

    Args:
        config: Resolved pipeline configuration.

    Returns:
        The writer instance.

    Raises:
        ConfigError: If ``config.writer`` has no registered implementation.
    """
    if config.writer == "local":
        return LocalFileWriter(config.output_dir)
    raise ConfigError(f"No writer implementation registered for {config.writer!r}")


def run_pipeline(config: PipelineConfig) -> WriteResult:
    """Read the configured source and write it with the configured writer.

    Args:
        config: Resolved pipeline configuration.

    Returns:
        Details of the completed write.

    Raises:
        ConfigError: If the configured writer is not available.
        ReaderError: If the source cannot be read.
        WriterError: If the output cannot be written.
    """
    writer = build_writer(config)
    batch = CsvReader().read(config.input_path)
    return writer.write(batch)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the pipeline from the command line.

    Args:
        argv: Command-line arguments. Defaults to ``sys.argv[1:]``.

    Returns:
        Process exit code. Zero on success.
    """
    parser = argparse.ArgumentParser(description="Run the Contoso data pipeline.")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging.")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )

    try:
        result = run_pipeline(load_config())
    except (ConfigError, ReaderError, WriterError) as exc:
        logger.error("Pipeline failed: %s", exc)
        return 1

    logger.info("Done: %d records written to %s", result.records_written, result.destination)
    return 0


if __name__ == "__main__":
    sys.exit(main())
