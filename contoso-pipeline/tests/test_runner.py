"""Tests for configuration loading and the pipeline runner."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pipeline.config import ConfigError, PipelineConfig, load_config
from pipeline.readers import ReaderError
from pipeline.runner import build_writer, main, run_pipeline
from pipeline.writers import LocalFileWriter

SAMPLE = Path(__file__).resolve().parent.parent / "data" / "sample_records.csv"


def test_load_config_uses_defaults() -> None:
    config = load_config({})

    assert config.writer == "local"
    assert config.input_path == Path("data/sample_records.csv")
    assert config.output_dir == Path("output")


def test_load_config_reads_environment() -> None:
    config = load_config(
        {
            "PIPELINE_INPUT_PATH": "in.csv",
            "PIPELINE_OUTPUT_DIR": "out",
            "PIPELINE_WRITER": "LOCAL",
        }
    )

    assert config == PipelineConfig(input_path=Path("in.csv"), output_dir=Path("out"), writer="local")


def test_load_config_rejects_unknown_writer() -> None:
    with pytest.raises(ConfigError, match="Unsupported writer"):
        load_config({"PIPELINE_WRITER": "carrier-pigeon"})


def test_build_writer_returns_local_writer(tmp_path: Path) -> None:
    config = PipelineConfig(input_path=SAMPLE, output_dir=tmp_path, writer="local")

    assert isinstance(build_writer(config), LocalFileWriter)


def test_build_writer_rejects_unregistered_writer(tmp_path: Path) -> None:
    config = PipelineConfig(input_path=SAMPLE, output_dir=tmp_path, writer="mystery")

    with pytest.raises(ConfigError, match="No writer implementation"):
        build_writer(config)


def test_run_pipeline_writes_all_sample_records(tmp_path: Path) -> None:
    config = PipelineConfig(input_path=SAMPLE, output_dir=tmp_path)

    result = run_pipeline(config)

    output = tmp_path / "sample_records.jsonl"
    assert result.records_written == 10
    assert result.destination == str(output)
    lines = output.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 10
    assert json.loads(lines[0])["record_id"] == "r-0001"


def test_run_pipeline_propagates_reader_errors(tmp_path: Path) -> None:
    config = PipelineConfig(input_path=tmp_path / "nope.csv", output_dir=tmp_path)

    with pytest.raises(ReaderError):
        run_pipeline(config)


def test_main_returns_zero_on_success(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PIPELINE_INPUT_PATH", str(SAMPLE))
    monkeypatch.setenv("PIPELINE_OUTPUT_DIR", str(tmp_path))

    assert main([]) == 0
    assert (tmp_path / "sample_records.jsonl").exists()


def test_main_returns_one_on_failure(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PIPELINE_INPUT_PATH", str(tmp_path / "nope.csv"))
    monkeypatch.setenv("PIPELINE_OUTPUT_DIR", str(tmp_path))

    assert main([]) == 1
