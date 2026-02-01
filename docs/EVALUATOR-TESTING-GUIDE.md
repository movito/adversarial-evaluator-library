# Evaluator Testing Guide

How to test new and existing evaluators in the adversarial-evaluator-library.

## Overview

Testing evaluators follows a **tiered approach** (see [ADR-0001](decisions/adr/ADR-0001-evaluator-testing-strategy.md)):

| Tier | What | Cost | When |
|------|------|------|------|
| **Tier 1** | Configuration validation | Free | Every commit |
| **Tier 2** | Behavioral testing | API costs | Main branch, manual |
| **Tier 3** | Cross-model comparison | API costs | New evaluators |

## Quick Start

```bash
# Tier 1: Validate all evaluator configs (free, fast)
pytest tests/test_evaluators.py -v -m "not requires_api"

# Tier 2: Test with API calls (requires keys)
pytest tests/test_code_evaluators.py -v

# Test a specific evaluator manually
adversarial evaluate --evaluator gpt4o-code tests/fixtures/code_samples/sample_secure.py
```

## Tier 1: Configuration Tests

These tests validate evaluator structure **without making API calls**. Run them frequently during development.

### What Gets Tested

| Check | File | Description |
|-------|------|-------------|
| YAML validity | `test_evaluators.py` | Can the config be parsed? |
| Required fields | `test_evaluators.py` | name, description, model, api_key_env, prompt |
| Prompt placeholder | `test_evaluators.py` | Does prompt contain `{content}`? |
| Index consistency | `test_evaluators.py` | Is evaluator in index.json? |
| Path existence | `test_evaluators.py` | Do all index paths exist? |
| README exists | `test_evaluators.py` | Does evaluator have documentation? |
| CHANGELOG exists | `test_evaluators.py` | Does evaluator have version history? |

### Running Tier 1 Tests

```bash
# All config tests
pytest tests/test_evaluators.py -v -m "not requires_api"

# Just YAML validation
pytest tests/test_evaluators.py::TestEvaluatorYAML -v

# Just index checks
pytest tests/test_evaluators.py::TestIndex -v

# Just documentation checks
pytest tests/test_evaluators.py::TestDocumentation -v
```

### Expected Output

```
tests/test_evaluators.py::TestEvaluatorYAML::test_yaml_is_valid[evaluator0] PASSED
tests/test_evaluators.py::TestEvaluatorYAML::test_required_fields_present[evaluator0] PASSED
tests/test_evaluators.py::TestEvaluatorYAML::test_prompt_has_content_placeholder[evaluator0] PASSED
...
```

## Tier 2: Behavioral Tests

These tests verify evaluator output against **known code samples**. They require API keys and cost money.

### Test Fixtures

Located in `tests/fixtures/code_samples/`:

| Sample | Expected Behavior | Purpose |
|--------|-------------------|---------|
| `sample_secure.py` | APPROVED | Clean code with good practices |
| `sample_vulnerable.py` | CHANGES_REQUESTED | SQL injection, hardcoded secrets |
| `sample_buggy.py` | CHANGES_REQUESTED | Off-by-one errors, logic bugs |
| `sample_messy.py` | CHANGES_REQUESTED | Poor style, no docs |

### Running Tier 2 Tests

```bash
# Set API keys
export OPENAI_API_KEY="sk-..."
export GEMINI_API_KEY="..."
export MISTRAL_API_KEY="..."

# Run all code evaluator tests
pytest tests/test_code_evaluators.py -v

# Run specific evaluator tests
pytest tests/test_code_evaluators.py -k "gpt4o" -v

# Skip slow reasoning models
pytest tests/test_code_evaluators.py -v -m "not slow"
```

### Test Markers

```python
@pytest.mark.requires_api      # Needs API key to run
@pytest.mark.slow              # Takes >30 seconds (reasoning models)
@pytest.mark.skipif(...)       # Skip if specific key unavailable
```

### Expected Results by Evaluator

| Evaluator | sample_secure | sample_vulnerable | sample_buggy | Timeout |
|-----------|---------------|-------------------|--------------|---------|
| gpt4o-code | APPROVED | CHANGES_REQUESTED | CHANGES_REQUESTED | 180s |
| o1-mini-code | APPROVED | CHANGES_REQUESTED | CHANGES_REQUESTED | 300s |
| o1-code-review | APPROVED | REJECT | CHANGES_REQUESTED | 600s |

## Tier 3: Cross-Model Comparison

When adding a new evaluator, compare it against existing ones to understand its behavior profile.

### Comparison Workflow

```bash
# 1. Create or use a representative sample
cat > /tmp/test-sample.py << 'EOF'
def process_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"  # SQL injection
    return db.execute(query)
EOF

# 2. Run through multiple evaluators
adversarial evaluate --evaluator gpt4o-code /tmp/test-sample.py > /tmp/gpt4o.md
adversarial evaluate --evaluator o1-mini-code /tmp/test-sample.py > /tmp/o1-mini.md
adversarial evaluate --evaluator o1-code-review /tmp/test-sample.py > /tmp/o1-review.md

# 3. Compare outputs
diff /tmp/gpt4o.md /tmp/o1-mini.md
```

### What to Compare

- **Verdict agreement**: Do evaluators reach same conclusion?
- **Issue detection**: Which issues did each find?
- **Severity assessment**: How did they rate the same issues?
- **Response time**: How long did each take?
- **Cost**: What was the token usage?

### Documenting Comparisons

Save comparison results in the evaluator's README:

```markdown
## Comparison with Other Evaluators

| Aspect | This Evaluator | gpt4o-code | o1-code-review |
|--------|----------------|------------|----------------|
| Speed | 45s | 3s | 120s |
| Cost | $0.05 | $0.02 | $0.15 |
| Depth | Deep reasoning | Quick scan | Security focus |
```

## Adding a New Evaluator

### Step 1: Create Evaluator Structure

```bash
# Create directory
mkdir -p evaluators/<provider>/<name>

# Create required files
touch evaluators/<provider>/<name>/evaluator.yml
touch evaluators/<provider>/<name>/README.md
touch evaluators/<provider>/<name>/CHANGELOG.md
```

### Step 2: Configure evaluator.yml

```yaml
name: my-evaluator
description: What this evaluator does
model: model-identifier
api_key_env: PROVIDER_API_KEY
output_suffix: -my-eval.md
timeout: 180

prompt: |
  You are a code reviewer. Analyze the following code:

  {content}

  Provide your assessment with:
  1. Issues found (Critical, Should Fix, Consider)
  2. What's good
  3. Verdict: APPROVED, CHANGES_REQUESTED, or REJECT
```

### Step 3: Add to Index

Edit `evaluators/index.json`:

```json
{
  "evaluators": [
    {
      "name": "my-evaluator",
      "provider": "provider-name",
      "category": "code-review",
      "path": "provider/my-evaluator/evaluator.yml"
    }
  ]
}
```

### Step 4: Run Tier 1 Tests

```bash
pytest tests/test_evaluators.py -v -m "not requires_api"
```

All tests should pass. If not:
- Check YAML syntax
- Verify required fields
- Ensure `{content}` is in prompt
- Confirm index.json entry

### Step 5: Run Behavioral Tests

```bash
# Test against fixtures
adversarial evaluate --evaluator my-evaluator tests/fixtures/code_samples/sample_secure.py
adversarial evaluate --evaluator my-evaluator tests/fixtures/code_samples/sample_vulnerable.py
```

Verify:
- Clean code gets APPROVED
- Vulnerable code gets flagged
- Output format is readable

### Step 6: Document Behavior

Update the evaluator's README.md with:
- Use cases
- Example output
- Comparison with similar evaluators
- Cost estimates
- Known limitations

### Step 7: Add Behavioral Tests (Optional)

For important evaluators, add to `test_code_evaluators.py`:

```python
@pytest.mark.requires_api
@pytest.mark.skipif(
    not os.environ.get("PROVIDER_API_KEY"),
    reason="PROVIDER_API_KEY not set"
)
def test_my_evaluator_detects_vulnerability(self):
    """my-evaluator should flag SQL injection."""
    result = run_evaluator(
        "provider/my-evaluator/evaluator.yml",
        SAMPLE_VULNERABLE,
        timeout=180
    )
    assert result.success
    assert result.verdict in ["CHANGES_REQUESTED", "REJECT"]
```

## Test Fixtures

### Creating New Fixtures

When existing fixtures don't cover a scenario:

```bash
# Create fixture with known issues
cat > tests/fixtures/code_samples/sample_new_scenario.py << 'EOF'
"""
Sample demonstrating [specific issue].
Expected: [expected verdict and findings]
"""

def example():
    # Code with the specific issue
    pass
EOF
```

### Fixture Guidelines

1. **Single purpose**: Each fixture tests one category of issues
2. **Documented**: Include docstring with expected behavior
3. **Realistic**: Use patterns seen in real code
4. **Minimal**: Just enough code to trigger detection

### Current Fixtures

| Fixture | Issues | Expected Verdict |
|---------|--------|------------------|
| `sample_secure.py` | None | APPROVED |
| `sample_vulnerable.py` | SQL injection, hardcoded secrets, path traversal | CHANGES_REQUESTED or REJECT |
| `sample_buggy.py` | Off-by-one, null reference, race condition | CHANGES_REQUESTED |
| `sample_messy.py` | No docs, poor naming, god function | CHANGES_REQUESTED |

## CI/CD Integration

### GitHub Actions Configuration

```yaml
name: Tests

on: [push, pull_request]

jobs:
  config-tests:
    # Runs on every PR - no secrets needed
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -e ".[dev]"
      - run: pytest tests/test_evaluators.py -v -m "not requires_api"

  api-tests:
    # Only on main - uses secrets
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -e ".[dev]"
      - run: pytest tests/test_code_evaluators.py -v
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
          MISTRAL_API_KEY: ${{ secrets.MISTRAL_API_KEY }}
```

### Local Pre-Commit Hook

Add to `.pre-commit-config.yaml`:

```yaml
- repo: local
  hooks:
    - id: evaluator-config-check
      name: Check evaluator configs
      entry: pytest tests/test_evaluators.py -v -m "not requires_api" --tb=short
      language: system
      pass_filenames: false
      files: ^evaluators/.*\.yml$
```

## Troubleshooting

### "YAML parse error"

```bash
# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('evaluators/path/evaluator.yml'))"
```

Common issues:
- Indentation errors
- Missing quotes around strings with special characters
- Invalid YAML syntax in multiline prompts

### "Missing required field"

Check `evaluator.yml` has all required fields:

```yaml
name: required
description: required
model: required
api_key_env: required
prompt: required  # Must contain {content}
```

### "Not in index.json"

Add entry to `evaluators/index.json`:

```json
{
  "name": "evaluator-name",
  "provider": "provider",
  "category": "category",
  "path": "provider/evaluator-name/evaluator.yml"
}
```

### "API timeout"

Increase timeout in `evaluator.yml`:

```yaml
timeout: 600  # 10 minutes for reasoning models
```

Or in tests:

```python
result = run_evaluator(path, sample, timeout=600)
```

### "API key not found"

```bash
# Check key is set
echo $OPENAI_API_KEY

# Set for session
export OPENAI_API_KEY="sk-..."

# Or use .env file
cp .env.template .env
# Edit .env with your keys
```

## Cost Management

### Estimated Costs per Test Run

| Evaluator Type | Per Evaluation | Full Test Suite |
|----------------|----------------|-----------------|
| Quick-check (gpt-4o-mini, gemini-flash) | $0.001-0.01 | ~$0.05 |
| Standard (gpt-4o, gemini-pro) | $0.01-0.05 | ~$0.20 |
| Reasoning (o1, o3) | $0.05-0.20 | ~$0.80 |

### Cost-Saving Tips

1. **Run Tier 1 first**: Catch config errors before API calls
2. **Use `-k` filter**: Test specific evaluators only
3. **Skip slow tests**: Use `-m "not slow"` during development
4. **Reuse outputs**: Save results instead of re-running

```bash
# Save output for later analysis
adversarial evaluate --evaluator gpt4o-code sample.py > results/gpt4o-sample.md
```

## References

- [ADR-0001: Evaluator Testing Strategy](decisions/adr/ADR-0001-evaluator-testing-strategy.md)
- [TESTING.md](TESTING.md) - General testing guide
- [README.md](../README.md) - Library overview
- `tests/test_evaluators.py` - Tier 1 implementation
- `tests/test_code_evaluators.py` - Tier 2 implementation
