# Defect Log — Student Course Registration System

These are suspected defects identified by comparing the supplied implementation with `REQUIREMENTS.md`. Confirm each with the corresponding failing test output before filing an issue.

| ID | Function | Requirement | Observed implementation problem | Suggested severity |
|---|---|---|---|---|
| D-01 | `check_credit_limit` | FR-01: total credits up to and including 18 are allowed | Uses `< 18`, rejecting exactly 18 | High |
| D-02 | `prerequisites_satisfied` | FR-03: every required course must be completed | Uses any intersection, so one completed prerequisite can incorrectly satisfy multiple requirements | High |
| D-03 | `registration_decision` | FR-04: any positive dues block registration | Blocks only when dues exceed 1000; dues from 1 to 1000 are incorrectly accepted | High |
| D-04 | `registration_decision` | FR-08: a course with enrolled == capacity is full and should be waitlisted | Checks `enrolled > capacity`; this condition is unreachable after validation, so a full course returns REGISTERED | High |
| D-05 | `withdraw_course` | FR-13: withdrawal decrements course enrollment | Removes course from student's set and credits but does not decrement `course.enrolled` | High |

## Reporting
For each confirmed defect, create a GitHub Issue with:
- Title: `[D-0X] short defect description`
- Preconditions / input data
- Steps to reproduce
- Expected result from `REQUIREMENTS.md`
- Actual result from test run
- Evidence: failing pytest test name/output

Do not silently fix the implementation as part of the testing submission unless the instructor explicitly asks for fixes.
