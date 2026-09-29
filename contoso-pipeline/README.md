# contoso-pipeline

A small Python data pipeline used in the Hypervelocity Engineering (HVE) lab. It reads records from a CSV file and writes them as JSON Lines using a pluggable writer.

## Setup

```
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
```

## Run the tests

```
pytest -q
```

## Run the pipeline

```
python -m pipeline.runner
```

Run from the repository root with `PYTHONPATH=src` (or install the package). Output is written to `output/sample_records.jsonl`.

## Layout

See `docs/architecture.md` for the design and `docs/conventions.md` for the team coding conventions.
