# Code Sample Test Fixtures

This directory contains code samples for testing code review evaluators.
Each sample is designed to trigger specific types of findings.

## Samples

| File | Purpose | Expected Verdict | Key Issues |
|------|---------|------------------|------------|
| `sample_secure.py` | Clean code baseline | APPROVED | None (demonstrates best practices) |
| `sample_vulnerable.py` | Security vulnerabilities | REJECT | SQL injection, hardcoded secrets, command injection |
| `sample_buggy.py` | Logic bugs | CHANGES_REQUESTED | Off-by-one, null handling, race conditions |
| `sample_messy.py` | Code quality issues | CHANGES_REQUESTED | Naming, duplication, magic numbers |

## Usage

These samples are used by `tests/test_evaluators.py` to validate that code review evaluators:

1. **Pass clean code** - `sample_secure.py` should receive APPROVED
2. **Catch security issues** - `sample_vulnerable.py` should flag injections, secrets
3. **Detect logic bugs** - `sample_buggy.py` should find off-by-one, resource leaks
4. **Flag quality issues** - `sample_messy.py` should note naming, duplication

## Adding New Samples

When adding a new sample:

1. Name it `sample_<category>.py`
2. Add a module docstring explaining:
   - What issues it contains
   - Expected evaluator verdict
   - Specific findings expected
3. Comment each intentional issue with `# BUG:`, `# VULNERABILITY:`, or `# QUALITY:`
4. Update this README

## Important Notes

- These files contain **intentional** bad code for testing
- **DO NOT** use this code in production
- Each issue is commented to explain what evaluators should catch
