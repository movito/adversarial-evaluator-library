# Test Results Directory

This directory contains results from code evaluator validation tests.

## Generated Files

When tests run with `OPENAI_API_KEY` set, the following files are generated:

### Individual Results
- `{evaluator}_{sample}_output.md` — Full evaluator output
- `{evaluator}_{sample}_{timestamp}.json` — Metrics (duration, verdict, etc.)

### Benchmark Summaries
- `benchmark_summary_{timestamp}.json` — All evaluators × all samples

## Running Tests

```bash
# Run all code evaluator tests (requires API key)
export OPENAI_API_KEY=sk-...
pytest tests/test_code_evaluators.py -v

# Run only fixture validation (no API needed)
pytest tests/test_code_evaluators.py::TestCodeEvaluatorFixtures -v

# Skip slow tests (o1 reasoning)
pytest tests/test_code_evaluators.py -v -m "not slow"

# Run full benchmark
pytest tests/test_code_evaluators.py::TestPerformanceBenchmark -v -s
```

## Expected Results

| Evaluator | sample_secure | sample_vulnerable | sample_buggy | sample_messy |
|-----------|---------------|-------------------|--------------|--------------|
| o1-code-review | APPROVED | REJECT | CHANGES_REQUESTED | CHANGES_REQUESTED |
| o1-mini-code | APPROVED | CHANGES_REQUESTED | CHANGES_REQUESTED | CHANGES_REQUESTED |
| gpt4o-code | APPROVED | CHANGES_REQUESTED | CHANGES_REQUESTED | CHANGES_REQUESTED |

## Cost Estimates

Per full benchmark run (12 evaluations):
- o1-code-review: ~$0.60-2.00
- o1-mini-code: ~$0.04-0.20
- gpt4o-code: ~$0.04-0.12
- **Total**: ~$0.70-2.50

## Interpreting Results

### Verdicts
- **APPROVED**: Code passes review with no/minor issues
- **CHANGES_REQUESTED**: Issues found that need addressing
- **REJECT**: Critical issues, code should not be used

### Detection Validation
Tests verify evaluators detect:
- SQL injection, command injection, hardcoded secrets (security)
- Off-by-one errors, resource leaks, null handling (bugs)
- Naming issues, code duplication, magic numbers (quality)
