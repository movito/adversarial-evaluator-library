# Feedback: Workflow Resolver Ignores Evaluator Model Field

**From**: adversarial-evaluator-library team
**Date**: 2026-02-06
**Workflow Version**: 0.9.2
**Severity**: Medium (blocks library evaluator updates)

---

## Summary

The workflow's `resolver.py` has hardcoded model mappings that **override** the model field from evaluator files. This means library updates to model IDs have no effect.

## Evidence

### Library Evaluator File
```yaml
# .adversarial/evaluators/anthropic-claude-quick.yml
model: anthropic/claude-haiku-4-5  # Current model (Feb 2026)
```

### What `list-evaluators` Shows
```
claude-quick   Fast validation using Claude Haiku 4.5
  model: anthropic/claude-haiku-4-5  ✅ Correct
```

### What `evaluate` Uses
```
CLAUDE-QUICK: Using model anthropic/claude-4-haiku-20260115  ❌ Wrong
```

### Root Cause

```python
# adversarial_workflow/evaluators/resolver.py
"models": ["claude-4-haiku-20260115"],  # Hardcoded!
"prefix": "anthropic/",
```

The resolver has a static model registry that takes precedence over the evaluator file's `model` field.

## Impact

1. **Library model updates are ignored** - Updating `model:` in evaluator YAMLs has no effect
2. **Anthropic testing blocked** - Can't verify new model IDs work
3. **Model deprecation breaks silently** - When Anthropic deprecates `claude-4-haiku-20260115`, evaluators will fail even if library has updated IDs

## Expected Behavior

The `evaluate` command should use the `model:` field from the evaluator file, not hardcoded mappings.

```python
# Current (broken)
model = resolver.lookup(evaluator.family, evaluator.tier)  # Returns hardcoded ID

# Expected
model = evaluator.model  # Use what the file says
```

## Workaround

**Fixed in v0.9.3** (ADV-0032, released 2026-02-07). Upgrade to `adversarial-workflow>=0.9.3`. The resolver now respects the explicit `model` field in evaluator files.

## Suggested Fix

### Option A: Use evaluator's model field directly

```python
def resolve_model(evaluator_config):
    # Just use what the evaluator says
    return evaluator_config.get("model")
```

### Option B: Make resolver a fallback only

```python
def resolve_model(evaluator_config):
    # Prefer evaluator's model field
    if "model" in evaluator_config:
        return evaluator_config["model"]
    # Fall back to resolver for legacy evaluators
    return resolver.lookup(...)
```

## Test Case

```bash
# Create evaluator with custom model
cat > .adversarial/evaluators/test-model.yml << 'EOF'
name: test-model
model: anthropic/claude-haiku-4-5
api_key_env: ANTHROPIC_API_KEY
prompt: "Test {content}"
EOF

# Check list-evaluators
adversarial list-evaluators | grep test-model
# Shows: model: anthropic/claude-haiku-4-5 ✅

# Run evaluate
adversarial evaluate --evaluator test-model test.md
# Uses: anthropic/claude-4-haiku-20260115 ❌ (resolver override)
```

## Current Models (February 2026)

Per https://platform.claude.com/docs/en/about-claude/models/overview:

| Tier | Current Model ID | Old ID (deprecated) |
|------|-----------------|---------------------|
| Opus | `claude-opus-4-6` | `claude-4-opus-20260115` |
| Sonnet | `claude-sonnet-4-5` | `claude-4-sonnet-20260115` |
| Haiku | `claude-haiku-4-5` | `claude-4-haiku-20260115` |

---

**Priority**: Medium - Blocks library evaluator updates from taking effect
