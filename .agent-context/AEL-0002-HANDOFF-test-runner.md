# AEL-0002 Handoff: Run Smoke Tests to Validate Evaluators

**Target Agent**: test-runner
**Created**: 2026-01-31
**Planner**: coordinator

---

## Mission

Validate that all 9 evaluator configurations in the adversarial-evaluator-library are correctly structured and ready for use.

## Context

This library contains adversarial evaluators for AI-assisted document review:

| Provider | Evaluators |
|----------|------------|
| Google | gemini-flash, gemini-pro, gemini-deep |
| Mistral | mistral-content, mistral-fast, codestral-code |
| OpenAI | gpt52-reasoning, o3-chain, fast-check |

Each evaluator has:
- `evaluator.yml` - Configuration with prompt template
- `README.md` - Usage documentation
- `CHANGELOG.md` - Version history

## Test File Location

```
tests/test_evaluators.py
```

## Test Categories

| Class | Tests | Requires API |
|-------|-------|--------------|
| `TestEvaluatorYAML` | YAML parsing, required fields, prompt placeholder | No |
| `TestIndex` | Index validity, path existence, completeness | No |
| `TestDocumentation` | README/CHANGELOG presence | No |
| `TestEvaluatorExecution` | Actual API calls | Yes |

## Execution Steps

### Step 1: Mark Task In Progress

```bash
./scripts/project start AEL-0002
```

### Step 2: Run Non-API Tests

```bash
pytest tests/test_evaluators.py -v -m "not requires_api"
```

**Expected output**: 9 evaluators × 3 YAML tests + 3 index tests + 9×2 doc tests = ~48 tests

### Step 3: Document Results

Record:
- Total tests run
- Pass/fail count
- Any failures with details

### Step 4: (Optional) Check API Keys

```bash
echo "OPENAI_API_KEY: ${OPENAI_API_KEY:+configured}"
echo "GEMINI_API_KEY: ${GEMINI_API_KEY:+configured}"
echo "MISTRAL_API_KEY: ${MISTRAL_API_KEY:+configured}"
```

### Step 5: (Optional) Run API Tests

Only if keys are available:

```bash
pytest tests/test_evaluators.py -v -m requires_api
```

### Step 6: Complete Task

If all non-API tests pass:

```bash
./scripts/project complete AEL-0002
```

If failures exist, keep task in progress and document issues.

## Required Fields in evaluator.yml

Tests validate these fields exist:
- `name`
- `description`
- `model`
- `api_key_env`
- `prompt` (must contain `{content}` placeholder)

## Success Criteria

| Criterion | Target |
|-----------|--------|
| Non-API test pass rate | 100% |
| Evaluators validated | 9/9 |
| Index consistency | All paths exist |
| Documentation complete | 18/18 files (9 README + 9 CHANGELOG) |

## If Tests Fail

1. Note which evaluator/test failed
2. Check the specific error message
3. Do NOT fix - just document
4. Report findings to planner
5. Keep task in `3-in-progress/`

## References

- Task spec: `delegation/tasks/2-todo/AEL-0002-run-smoke-tests.md`
- Evaluator index: `evaluators/index.json`
- Test file: `tests/test_evaluators.py`
