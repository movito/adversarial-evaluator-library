# ADR-0001: Evaluator Testing Strategy

**Status**: Accepted

**Date**: 2026-02-01

**Deciders**: planner, feature-developer

## Context

### Problem Statement

The adversarial-evaluator-library contains multiple evaluators across different AI providers (OpenAI, Google, Mistral). Each evaluator uses different models with varying capabilities, costs, and latencies. We need a systematic approach to:

1. Validate evaluator configurations before deployment
2. Test evaluator behavior against known code samples
3. Ensure new evaluators integrate correctly with the library
4. Balance thorough testing with API cost constraints

### Forces at Play

**Technical Requirements:**
- Evaluators must be validated for correct YAML structure
- Prompts must contain required placeholders (`{content}`)
- Each evaluator needs README.md and CHANGELOG.md
- Evaluators must be registered in `evaluators/index.json`
- API-based tests need to handle timeouts and rate limits

**Constraints:**
- API calls cost money ($0.001 - $0.20+ per evaluation)
- Some models (o1, o3) have long response times (30s - 10min)
- CI/CD should not require API keys for basic validation
- Different providers require different API keys

**Assumptions:**
- Contributors may not have all API keys
- Most configuration errors can be caught without API calls
- Known code samples can verify evaluator behavior patterns

## Decision

We adopt a **tiered testing strategy** that separates configuration validation from behavioral testing:

### Tier 1: Configuration Tests (No API)

Fast, free tests that validate evaluator structure:

```python
# Run without API keys
pytest tests/test_evaluators.py -v -m "not requires_api"
```

**Validates:**
- YAML syntax and parseability
- Required fields present (name, description, model, api_key_env, prompt)
- Prompt contains `{content}` placeholder
- Index.json consistency (all evaluators listed, paths exist)
- Documentation exists (README.md, CHANGELOG.md)

### Tier 2: Behavioral Tests (Requires API)

Tests that verify evaluator output against known samples:

```python
# Requires OPENAI_API_KEY
pytest tests/test_code_evaluators.py -v -m "requires_api"
```

**Sample Categories:**
- `sample_secure.py` - Clean code, should APPROVE
- `sample_vulnerable.py` - Security issues, should flag
- `sample_buggy.py` - Logic bugs, should detect
- `sample_messy.py` - Style issues, should note

### Tier 3: Cross-Model Comparison (Manual)

When adding new evaluators, compare outputs across models:

```bash
# Run same sample through multiple evaluators
adversarial evaluate --evaluator gpt4o-code sample.py
adversarial evaluate --evaluator o1-mini-code sample.py
adversarial evaluate --evaluator o1-code-review sample.py
```

### Core Principles

1. **Fail Fast**: Configuration errors caught immediately, before any API calls
2. **Cost Awareness**: API tests skipped when keys unavailable, not failed
3. **Fixtures Over Live**: Use pre-defined samples with known issues
4. **Document Results**: Save evaluation outputs for comparison

### Implementation Details

**Test file structure:**

```
tests/
├── test_evaluators.py           # Tier 1: Config validation
├── test_code_evaluators.py      # Tier 2: Behavioral tests
├── fixtures/
│   └── code_samples/
│       ├── sample_secure.py     # Known-good code
│       ├── sample_vulnerable.py # SQL injection, etc.
│       ├── sample_buggy.py      # Logic errors
│       └── sample_messy.py      # Style issues
└── results/                     # Saved evaluation outputs
```

**Test markers:**

```python
@pytest.mark.requires_api      # Needs API key
@pytest.mark.slow              # Takes >30 seconds
@pytest.mark.skipif(...)       # Skip if key unavailable
```

**CI configuration:**

```yaml
# Tier 1 runs on every PR (no secrets needed)
- name: Config Tests
  run: pytest tests/test_evaluators.py -m "not requires_api"

# Tier 2 runs on main with secrets
- name: API Tests
  if: github.ref == 'refs/heads/main'
  env:
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
  run: pytest tests/test_code_evaluators.py -m "requires_api"
```

## Consequences

### Positive

- ✅ **Fast feedback**: Config errors caught in <1 second
- ✅ **Cost control**: API tests only run when needed
- ✅ **Contributor-friendly**: No API keys needed for basic contributions
- ✅ **Consistent validation**: All evaluators tested the same way
- ✅ **Behavioral baselines**: Known samples establish expected behavior

### Negative

- ⚠️ **Partial coverage**: Not all model behaviors tested automatically
- ⚠️ **Fixture maintenance**: Sample files need updates as expectations change
- ⚠️ **API drift**: Model behavior can change without test failures

### Neutral

- 📊 **Results archival**: Evaluation outputs saved but not version-controlled
- 📊 **Provider parity**: Not all providers tested equally (depends on keys)

## Alternatives Considered

### Alternative 1: All Tests Require API

**Description**: Every test makes real API calls

**Rejected because**:
- ❌ High cost for CI/CD (every PR costs money)
- ❌ Contributors without keys cannot run tests
- ❌ Slow feedback (minutes vs seconds)
- ❌ Rate limiting issues in parallel runs

### Alternative 2: Mock All API Calls

**Description**: Use mocked responses for all tests

**Rejected because**:
- ❌ Mocks don't catch prompt regressions
- ❌ Model behavior changes go undetected
- ❌ False confidence in test results
- ❌ High maintenance burden for mock data

### Alternative 3: Snapshot Testing

**Description**: Record outputs and compare against snapshots

**Rejected because**:
- ❌ Model outputs are non-deterministic
- ❌ Minor wording changes cause false failures
- ❌ Snapshots become stale quickly

## Related Decisions

- KIT-ADR-0005: Test Infrastructure Strategy (inherited patterns)
- KIT-ADR-0017: API Testing Infrastructure (API testing approach)

## References

- `docs/EVALUATOR-TESTING-GUIDE.md` - Comprehensive testing guide
- `tests/test_evaluators.py` - Tier 1 implementation
- `tests/test_code_evaluators.py` - Tier 2 implementation
- `evaluators/index.json` - Evaluator registry

## Revision History

- 2026-02-01: Initial decision (Accepted)
