# Pipeline Architecture

The Contoso ingestion pipeline reads source records, groups them into a batch, and writes the batch to an output destination.

```
CSV file  ->  CsvReader  ->  Batch  ->  Writer  ->  destination
                                        (chosen by PIPELINE_WRITER)
```

## Components

| Module | Responsibility |
|---|---|
| `pipeline/runner.py` | Entry point. Loads config, builds the writer, reads the batch, writes it. |
| `pipeline/config.py` | Reads environment variables into a `PipelineConfig`. Lists `SUPPORTED_WRITERS`. |
| `pipeline/models.py` | `Record` and `Batch` data models. |
| `pipeline/readers/csv_reader.py` | Parses a CSV file into a `Batch`. Raises `ReaderError`. |
| `pipeline/writers/base.py` | `WriterBase`, `WriteResult`, `WriterError`. |
| `pipeline/writers/local_writer.py` | `LocalFileWriter`: writes `<batch_id>.jsonl` to a local directory. |

## Writer contract

`WriterBase.write(batch)` is the public entry point. It rejects empty batches, calls the subclass's `_write`, and converts any unexpected exception into `WriterError`. Subclasses implement `_write` and must be atomic (see `docs/conventions.md`).

`LocalFileWriter` achieves atomicity by writing to a `.tmp` file in the output directory and renaming it over the final path only after every record has been written.

## Configuration

| Variable | Default | Meaning |
|---|---|---|
| `PIPELINE_INPUT_PATH` | `data/sample_records.csv` | CSV file to read |
| `PIPELINE_OUTPUT_DIR` | `output` | Directory for the local writer |
| `PIPELINE_WRITER` | `local` | Writer to use. Must appear in `SUPPORTED_WRITERS` |

## Output format

JSON Lines. One object per record, with the fields `record_id`, `customer_id`, `event_type`, `amount` (string, to preserve precision) and `occurred_at` (ISO 8601).

## Known limitation

Output is written to local disk only. Customers have asked for Azure Blob Storage output. The Azure SDK packages are already listed in `requirements.txt`, but no writer uses them yet.
