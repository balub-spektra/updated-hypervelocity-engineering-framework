# Team Coding Conventions

These conventions apply to all code under `src/pipeline/` and `tests/`. Reviewers check new code against this document.

## Language and style

- Python 3.11. Every module starts with `from __future__ import annotations`.
- Maximum line length is 120 characters.
- Names: `snake_case` for functions, methods, variables and modules; `PascalCase` for classes; `UPPER_SNAKE_CASE` for module constants.
- Private members are prefixed with a single underscore.
- No `print`. Use a module-level logger: `logger = logging.getLogger(__name__)`.

## Type hints

- All function and method signatures are fully annotated, including return types.
- Use built-in generics (`list[str]`, `dict[str, str]`) and `X | None` rather than `typing.List` or `Optional`.
- Prefer immutable data: `@dataclass(frozen=True)` and tuples for collections on models.

## Docstrings

- Every module, public class and public method has a docstring.
- Use Google style with `Args:`, `Returns:` and `Raises:` sections where they apply.

## Error handling

- Each package defines its own exception type: `ReaderError`, `WriterError`, `ConfigError`.
- Writers report every failure as `WriterError`. Never let a backend exception type (`OSError`, an SDK exception) escape a writer.
- Always chain the original exception: `raise WriterError(...) from exc`.
- Error messages state what was being done and to what, for example the batch id and destination.
- Catch specific exception types. A bare `except Exception` is only permitted at an abstraction boundary that re-raises a typed error, as in `WriterBase.write`.

## Writers

- A writer extends `WriterBase` and implements `_write`. Callers only ever call `write`.
- A writer is **atomic**: if a write fails part-way, no partial output remains at the destination and any existing output is left untouched.
- Constructors take plain values (paths, names), not the whole `PipelineConfig`.
- Writers return a `WriteResult` describing the destination and the record count.
- A new writer is registered in `SUPPORTED_WRITERS` in `config.py` and in `build_writer` in `runner.py`.

## Testing

- Tests use `pytest`, live under `tests/` and mirror the layout of `src/pipeline/`.
- Test names describe behaviour: `test_write_leaves_no_partial_file_when_serialisation_fails`.
- Use the `tmp_path` fixture for filesystem work. Tests never touch the network.
- External services (Azure, for example) are replaced with fakes or `unittest.mock`. Tests must pass with no credentials.
- Every writer has tests for the success path, the empty-batch case, and the partial-write failure path.
