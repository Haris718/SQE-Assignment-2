# Test Plan — Student Course Registration System

## Scope
Black-box tests are derived from `REQUIREMENTS.md`; white-box tests exercise the implementation's decision branches. The system is in-memory only. Database, UI, authentication, payments, concurrency, and automatic waitlist promotion are out of scope.

## Strategy
- Equivalence Class Partitioning (ECP): valid/invalid dues, valid/invalid credit values, prerequisites fully met/partially met/not met, already registered/not registered, seats available/full.
- Boundary Value Analysis (BVA): current credits 0 and 18; new course credits 1 and 4; combined credits 18 and 19; dues 0 and 1; enrollment capacity-1 and capacity.
- Decision-table testing: verify priority order: dues → already registered → prerequisites → credit limit → availability.
- State-based testing: verify successful registration, waitlisting, unsuccessful registration, successful withdrawal, and unsuccessful withdrawal.
- White-box testing: exercise true/false outcomes and validation branches in each function.

## Execution
From the project root:
```bash
python -m pip install -r requirements.txt
python -m pytest -v
```
Run suites separately:
```bash
python -m pytest -v tests/test_blackbox.py
python -m pytest -v tests/test_whitebox.py
```

## Expected results
Expected behavior is taken from `REQUIREMENTS.md`, not from the implementation. A failing test is recorded as a suspected defect; do not weaken the assertion to make it pass.
