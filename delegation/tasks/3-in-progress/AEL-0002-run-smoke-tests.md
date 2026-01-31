# AEL-0002: Run Smoke Tests to Validate Evaluators

**Status**: In Progress
**Priority**: high
**Assigned To**: test-runner
**Estimated Effort**: 30 minutes
**Created**: 2026-01-31
**Target Completion**: 2026-01-31

## Related Tasks

**Blocks**: AEL-0001 (README should confirm tests pass)
**Related**: AEL-0003 (CI workflow runs these tests)

## Overview

Run the evaluator smoke tests to validate that all evaluator configurations are correct and properly structured. This validates the library's seed content before documentation.

**Context**: The library was initialized with 9 evaluators. We need to verify:
- All YAML files are valid
- Required fields are present
- Index is consistent with files
- Documentation exists for each evaluator

## Requirements

### Functional Requirements
1. Run YAML validation tests (no API keys needed)
2. Run index consistency tests
3. Run documentation presence tests
4. Optionally run API tests if keys available

### Test Categories

| Category | Requires API | Command |
|----------|--------------|---------|
| YAML validation | No | `pytest tests/test_evaluators.py::TestEvaluatorYAML -v` |
| Index tests | No | `pytest tests/test_evaluators.py::TestIndex -v` |
| Documentation | No | `pytest tests/test_evaluators.py::TestDocumentation -v` |
| API execution | Yes | `pytest tests/test_evaluators.py -v -m requires_api` |

## Implementation Plan

### Step 1: Run Non-API Tests

```bash
# Run all tests except API-dependent ones
pytest tests/test_evaluators.py -v -m "not requires_api"
```

**Expected**: All 9 evaluators pass YAML, field, and documentation tests.

### Step 2: Review Results

Document any failures:
- Which evaluator failed
- What the issue is
- Fix required

### Step 3: (Optional) Run API Tests

If API keys are configured:
```bash
# Check which keys are available
echo "OPENAI_API_KEY: ${OPENAI_API_KEY:+set}"
echo "GEMINI_API_KEY: ${GEMINI_API_KEY:+set}"
echo "MISTRAL_API_KEY: ${MISTRAL_API_KEY:+set}"

# Run API tests
pytest tests/test_evaluators.py -v -m requires_api
```

## Acceptance Criteria

### Must Have ✅
- [ ] All YAML validation tests pass
- [ ] All index consistency tests pass
- [ ] All documentation tests pass
- [ ] Test results documented

### Should Have 🎯
- [ ] At least one API test passes (if keys available)
- [ ] No warnings in test output

## Success Metrics

### Quantitative
- Test pass rate: 100% (non-API tests)
- Evaluators validated: 9/9
- Test execution time: <30 seconds

## Notes

- This is a validation task, not implementation
- If tests fail, create follow-up tasks for fixes
- API tests are optional but recommended

---

**Template Version**: 1.0.0
