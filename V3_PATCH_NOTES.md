# PythonTrader v1.3 repository maturity patch

This patch is intended for the current `PythonTrader` repository after the v2 integration.

It adds:

- a canonical root `pyproject.toml` for the existing `src/` layout;
- Python 3.11/3.12/3.13 CI with Ruff, mypy, pytest and coverage;
- deterministic machine-readable benchmark output;
- async runtime/event-dispatch infrastructure;
- read-only Kraken and Yahoo market-data adapters;
- freshness-aware market-data routing;
- integration tests for runtime and risk paths;
- a web control-plane client with no duplicated Python backend;
- a cleanup script for the legacy `src/datamedicine` tree and duplicated `web/src/pythontrader` tree.

Run `bash tools/apply_v3_cleanup.sh` after extracting this overlay into the repository root.
