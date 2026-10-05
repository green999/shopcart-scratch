# AGENTS.md

Instructions for coding agents working in this repository.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Commands

| Task | Command |
| --- | --- |
| Run all tests | `pytest -q` |
| Run one test file | `pytest -q tests/test_cart.py` |
| Lint | `ruff check .` |
| Format | `ruff format .` |

Run tests and lint before opening or updating a pull request. Both must pass.

## Code conventions

- Python 3.10+, type hints on every public function.
- Money is always `decimal.Decimal`. Never use `float` for prices, totals or rates.
- Round only at the edge, with `shopcart.money.round_cents`. Do not round intermediate values.
- Raise `ValueError` for invalid arguments; do not return `None` to signal an error.
- No new runtime dependencies. Dev dependencies go in `pyproject.toml` under `dev`.
- Public functions have a docstring that states behaviour at boundaries (zero, empty, exact thresholds).

## Tests

- Every behaviour change needs a test in `tests/`, in the file matching the module.
- A bug fix starts with a test that fails before the fix and passes after it.
- Cover boundaries explicitly: empty input, zero, and values exactly on a threshold.
- Do not delete or weaken an existing test to make a change pass. If a test is wrong, say why in the PR.

## Pull requests

- One logical change per PR, on a branch off `main`. Never push to `main`.
- The description states what changed, why, and how it was tested.
- For a bug fix, include the root cause in one or two sentences.
- Do not edit `.github/workflows/` unless the task asks for it.

## Review guidelines

When reviewing a PR in this repo, prioritise in this order:

1. Correctness, especially boundary conditions and behaviour that existing callers rely on.
2. Money handling: any `float`, early rounding or lost precision is a blocking finding.
3. Missing tests for changed behaviour.
4. Readability and naming. Do not comment on style that `ruff` already enforces.
