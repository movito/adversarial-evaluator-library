# Evaluator Testing Procedure

This document describes how to verify that library evaluators work correctly with adversarial-workflow.

## Prerequisites

1. **API Keys**: Configure at least one provider in `.env`:
   ```bash
   OPENAI_API_KEY=sk-...      # For OpenAI evaluators
   GEMINI_API_KEY=...         # For Google evaluators
   MISTRAL_API_KEY=...        # For Mistral evaluators
   ANTHROPIC_API_KEY=sk-ant-... # For Anthropic evaluators
   ```

2. **Workflow Installed**:
   ```bash
   pip install --upgrade adversarial-workflow
   adversarial --version  # Should show >= 0.9.2
   ```

## Test Procedure

### Step 1: Create Test Document

Create a test document with an intentional error:

```bash
cat > /tmp/test-document.md << 'EOF'
# Test Document

## Purpose
This is a test document for verifying adversarial evaluators.

## Content
- Item one
- Item two
- Item tree  <!-- intentional typo: "tree" should be "three" -->

## Conclusion
The evaluator should catch basic issues like spelling errors.
EOF
```

### Step 2: Install Evaluators

Install one evaluator per provider you want to test:

```bash
# Quick/cheap evaluators (recommended for testing)
adversarial library install openai/fast-check --yes      # ~$0.0002/eval
adversarial library install google/gemini-flash --yes    # ~$0.0012/eval
adversarial library install mistral/mistral-fast --yes   # ~$0.001/eval
```

Verify installation:
```bash
adversarial list-evaluators
```

Expected output:
```
Local Evaluators (.adversarial/evaluators/):
  fast-check     Fast validation using GPT-4o-mini
    model: gpt-4o-mini
  gemini-flash   Fast, cost-effective document assessment
    model: gemini/gemini-2.5-flash
  mistral-fast   Fast Mistral review for large documents
    model: mistral/mistral-small-latest
```

### Step 3: Run Evaluations

Test each evaluator and verify exit code:

```bash
# OpenAI
adversarial evaluate --evaluator fast-check /tmp/test-document.md
echo "Exit code: $?"  # Should be 0

# Google
adversarial evaluate --evaluator gemini-flash /tmp/test-document.md
echo "Exit code: $?"  # Should be 0

# Mistral
adversarial evaluate --evaluator mistral-fast /tmp/test-document.md
echo "Exit code: $?"  # Should be 0
```

### Step 4: Verify Output

Check that evaluators found the typo:

```bash
# Check output files
ls -la .adversarial/logs/test-document--*.md

# View output (should mention "tree" → "three" typo)
cat .adversarial/logs/test-document--fast-check.md.md
```

Expected: Each evaluator should identify the spelling error "tree" → "three".

## Pass Criteria

| Check | Expected |
|-------|----------|
| `adversarial list-evaluators` | Shows installed evaluators without warnings |
| Exit code | 0 for all evaluators |
| Output file | Created in `.adversarial/logs/` |
| Typo detected | Evaluator mentions "tree"/"three" error |

## Quick One-Liner Test

Run all three providers and check exit codes:

```bash
for e in fast-check gemini-flash mistral-fast; do
  echo "Testing $e..."
  adversarial evaluate --evaluator $e /tmp/test-document.md > /dev/null 2>&1
  echo "$e: exit code $?"
done
```

Expected output:
```
Testing fast-check...
fast-check: exit code 0
Testing gemini-flash...
gemini-flash: exit code 0
Testing mistral-fast...
mistral-fast: exit code 0
```

## Troubleshooting

### "No such evaluator"
```bash
adversarial list-evaluators  # Check what's installed
adversarial library install <provider>/<name> --yes
```

### API Key Errors
```bash
# Check which keys are set
cat .env | grep -E "API_KEY" | sed 's/=.*/=***/'
```

### Exit Code 1
If exit code is 1 but output exists, check workflow version:
```bash
adversarial --version  # Should be >= 0.9.2
pip install --upgrade adversarial-workflow
```

## Cost Estimates

| Evaluator | Model | Cost per Eval |
|-----------|-------|---------------|
| fast-check | gpt-4o-mini | ~$0.0002 |
| gemini-flash | gemini-2.5-flash | ~$0.0012 |
| mistral-fast | mistral-small | ~$0.001 |

Running the full test suite (3 evaluators × 1 document) costs approximately **$0.003**.

## Version History

| Workflow Version | Status |
|------------------|--------|
| < 0.9.0 | ❌ No `--evaluator` flag |
| 0.9.0 | ⚠️ Works but shows `_meta` warnings |
| 0.9.1 | ⚠️ No warnings but exit code 1 |
| 0.9.2 | ✅ All issues resolved |
