# SQE Assignment 2 — Test Pack

This pack adds the test suites and documentation. Copy/extract its `tests/` and `docs/` folders into the root of your existing assignment project (the folder containing `registration.py`).

## Run
```bash
python -m pip install pytest
python -m pytest -v
```

The tests intentionally assert the requirements. Some are expected to fail against the starter implementation because the assignment asks you to identify defects.

## Files
- `tests/test_blackbox.py`: ECP, BVA, decision priority, and state-based tests.
- `tests/test_whitebox.py`: function/branch-focused tests.
- `docs/test_plan.md`: scope, strategy, and execution.
- `docs/cfg_mcdc.md`: control-flow graph and MC/DC pairs.
- `docs/defect_log.md`: suspected defects derived from the stated requirements.
