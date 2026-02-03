# AEL-0006: Add model_requirement to Existing Evaluators

**Status**: In Review
**Priority**: high
**Assigned To**: feature-developer
**Estimated Effort**: 2-3 hours
**Created**: 2026-02-03
**Target Completion**: 2026-02-05

## Related Tasks

**Depends On**:
- ADR-0005 (Interface Contract) - ✅ Accepted
- `providers/registry.yml` - ✅ Published

**Related**:
- [ADR-0004](../../docs/decisions/adr/ADR-0004-evaluator-definition-model-routing-separation.md) - Layered architecture
- [ADR-0005](../../docs/decisions/adr/ADR-0005-library-workflow-interface-contract.md) - Interface contract
- ADV-0013 (adversarial-workflow) - Library CLI integration
- ADV-0015 (adversarial-workflow) - Resolution engine

## Overview

Update all 18 existing evaluators to include the `model_requirement` field alongside existing `model` and `api_key_env` fields. This enables the Phase 2 resolution engine in adversarial-workflow while maintaining backwards compatibility.

**Context**: ADR-0005 establishes a dual-field migration period where evaluators include both:
- Legacy fields (`model`, `api_key_env`) for workflow < 0.8.0
- New field (`model_requirement`) for workflow ≥ 0.8.0

## Requirements

### Evaluators to Update (18 total)

**OpenAI (6 evaluators)**:
| Evaluator | Family | Tier | Min Version |
|-----------|--------|------|-------------|
| `gpt52-reasoning` | gpt | flagship | 5.2 |
| `o3-chain` | o | flagship | 3 |
| `o1-code-review` | o | flagship | 1 |
| `o1-mini-code` | o | mini | 1 |
| `gpt4o-code` | gpt | standard | 4o |
| `fast-check` | gpt | mini | 4o-mini |

**Anthropic (3 evaluators)**:
| Evaluator | Family | Tier | Min Version |
|-----------|--------|------|-------------|
| `claude-adversarial` | claude | opus | 4 |
| `claude-code` | claude | sonnet | 4 |
| `claude-quick` | claude | haiku | 4 |

**Google (3 evaluators)**:
| Evaluator | Family | Tier | Min Version |
|-----------|--------|------|-------------|
| `gemini-pro` | gemini | pro | 3 |
| `gemini-flash` | gemini | flash | 2.5 |
| `gemini-deep` | gemini | flash | 2.5 |

**Mistral (6 evaluators)**:
| Evaluator | Family | Tier | Min Version |
|-----------|--------|------|-------------|
| `mistral-content` | mistral | large | large-2411 |
| `mistral-fast` | mistral | small | small-2409 |
| `codestral-code` | codestral | latest | latest |
| `gemini-code` | gemini | pro | 3 |
| `gpt5-diversity` | gpt | flagship | 5 |
| `gpt5-synthesis` | gpt | flagship | 5 |

### Per-Evaluator Changes

Add `model_requirement` block to each `evaluator.yml`:

```yaml
# BEFORE (legacy only)
name: claude-adversarial
model: claude-4-opus-20260115
api_key_env: ANTHROPIC_API_KEY
timeout: 180
prompt: |
  ...

# AFTER (dual field - Phase 2 ready)
name: claude-adversarial
model: claude-4-opus-20260115           # Legacy (keep for backwards compat)
api_key_env: ANTHROPIC_API_KEY          # Legacy (keep for backwards compat)
model_requirement:                       # NEW - Phase 2
  family: claude
  tier: opus
  min_version: "4"
timeout: 180
prompt: |
  ...
```

### Field Mapping Rules

| Legacy `model` | `family` | `tier` | `min_version` |
|----------------|----------|--------|---------------|
| `gpt-5.2` | gpt | flagship | 5.2 |
| `gpt-5-turbo-*` | gpt | flagship | 5 |
| `gpt-4o` | gpt | standard | 4o |
| `gpt-4o-mini` | gpt | mini | 4o-mini |
| `o3` | o | flagship | 3 |
| `o1` | o | flagship | 1 |
| `o1-mini` | o | mini | 1 |
| `claude-4-opus-*` | claude | opus | 4 |
| `claude-4-sonnet-*` | claude | sonnet | 4 |
| `claude-4-haiku-*` | claude | haiku | 4 |
| `gemini-3-pro*` | gemini | pro | 3 |
| `gemini-2.5-flash` | gemini | flash | 2.5 |
| `mistral-large-*` | mistral | large | large-2411 |
| `mistral-small-*` | mistral | small | small-2409 |
| `codestral-*` | codestral | latest | latest |

### Validation

After updates, verify:
- [ ] All 18 evaluators have `model_requirement` block
- [ ] `family` matches entry in `providers/registry.yml`
- [ ] `tier` matches tier name in registry
- [ ] `min_version` is a string (quoted in YAML)
- [ ] Legacy `model` and `api_key_env` fields preserved

## Acceptance Criteria

### Must Have
- [ ] All 18 evaluators updated with `model_requirement` field
- [ ] All `family` values exist in `providers/registry.yml`
- [ ] All `tier` values exist under their family in registry
- [ ] Config validation tests pass
- [ ] Existing behavioral tests still pass (backwards compat)

### Should Have
- [ ] Consistent field ordering (model_requirement after api_key_env)
- [ ] CHANGELOG updated with schema change note

### Nice to Have
- [ ] Script to validate model_requirement against registry

## Testing Approach

```bash
# 1. Config validation (should still pass)
pytest tests/test_evaluators.py -v -k "config"

# 2. Verify backwards compatibility
# Workflow < 0.8.0 should ignore model_requirement and use model field
adversarial gpt52-reasoning tests/fixtures/code_samples/sample_secure.py

# 3. Validate against registry (manual or script)
# Check that each family/tier combo exists in providers/registry.yml
```

## Implementation Notes

- **Field ordering**: Place `model_requirement` after `api_key_env`, before `timeout`
- **Version strings**: Always quote versions in YAML (e.g., `"4"` not `4`)
- **No context requirement**: Only add `min_context` if evaluator needs large context

## Example Update

```yaml
# evaluators/anthropic/claude-adversarial/evaluator.yml

# Claude Adversarial Evaluator
# Adversarial review using Claude Opus
#
# Provider: anthropic
# Use cases:
#   - Critical document review
#   - Stress-testing arguments
#   - Final review before publication

name: claude-adversarial
description: Adversarial review using Claude Opus
model: claude-4-opus-20260115
api_key_env: ANTHROPIC_API_KEY
model_requirement:
  family: claude
  tier: opus
  min_version: "4"
output_suffix: -claude-adversarial.md
timeout: 180

prompt: |
  You are a senior analyst conducting a rigorous adversarial review.
  ...
```

## Dependencies

- `providers/registry.yml` must be published (✅ Done)
- ADR-0005 accepted by workflow team (✅ Done)

## Reference Files

- `providers/registry.yml` - Model family/tier definitions
- `docs/decisions/adr/ADR-0005-library-workflow-interface-contract.md` - Schema spec
- `evaluators/index.json` - List of all evaluators

---

**Template Version**: 1.1.0
