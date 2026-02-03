# AEL-0006: Add model_requirement to Evaluators - Implementation Handoff

**Date**: 2026-02-03
**From**: Planner
**To**: feature-developer
**Task**: delegation/tasks/2-todo/AEL-0006-add-model-requirement-to-evaluators.md
**Status**: Ready for implementation
**Evaluation**: N/A (mechanical update - no evaluation needed)

---

## Task Summary

Update all 18 existing evaluators to include the `model_requirement` field. This enables Phase 2 model resolution in adversarial-workflow while maintaining backwards compatibility with the legacy `model` and `api_key_env` fields.

## Current Situation

- ADR-0005 established the interface contract between library and workflow
- `providers/registry.yml` has been published with all model family/tier definitions
- Evaluators currently have legacy fields only (`model`, `api_key_env`)
- Workflow v0.8.0 will support the new `model_requirement` field

## Your Mission

Add `model_requirement` block to each evaluator.yml file:

### Phase 1: OpenAI Evaluators (8 files)
Update evaluators in `evaluators/openai/`:
- `gpt52-reasoning/evaluator.yml`
- `o3-chain/evaluator.yml`
- `o1-code-review/evaluator.yml`
- `o1-mini-code/evaluator.yml`
- `gpt4o-code/evaluator.yml`
- `fast-check/evaluator.yml`
- `gpt5-diversity/evaluator.yml`
- `gpt5-synthesis/evaluator.yml`

### Phase 2: Anthropic Evaluators (3 files)
Update evaluators in `evaluators/anthropic/`:
- `claude-adversarial/evaluator.yml`
- `claude-code/evaluator.yml`
- `claude-quick/evaluator.yml`

### Phase 3: Google Evaluators (4 files)
Update evaluators in `evaluators/google/`:
- `gemini-pro/evaluator.yml`
- `gemini-flash/evaluator.yml`
- `gemini-deep/evaluator.yml`
- `gemini-code/evaluator.yml`

### Phase 4: Mistral Evaluators (3 files)
Update evaluators in `evaluators/mistral/`:
- `mistral-content/evaluator.yml`
- `mistral-fast/evaluator.yml`
- `codestral-code/evaluator.yml`

## Acceptance Criteria (Must Have)

- [ ] All 18 evaluators have `model_requirement` block
- [ ] All `family` values exist in `providers/registry.yml`
- [ ] All `tier` values exist under their family in registry
- [ ] All `min_version` values are quoted strings
- [ ] Legacy `model` and `api_key_env` fields preserved (not removed)
- [ ] Field ordering: `model_requirement` placed after `api_key_env`, before `output_suffix`
- [ ] All existing tests pass (`pytest tests/ -v`)

## Success Metrics

**Quantitative**:
- 18/18 evaluators updated with model_requirement
- 0 test failures (all existing tests pass)
- 0 validation errors against registry

**Qualitative**:
- Consistent field ordering across all files
- Clean YAML formatting preserved

## Critical Implementation Details

### 1. Field Mapping Reference

| Legacy `model` Pattern | `family` | `tier` | `min_version` |
|------------------------|----------|--------|---------------|
| `gpt-5.2` | gpt | flagship | "5.2" |
| `gpt-5-turbo-*` | gpt | flagship | "5" |
| `gpt-4o` | gpt | standard | "4o" |
| `gpt-4o-mini` | gpt | mini | "4o-mini" |
| `o3` | o | flagship | "3" |
| `o1` | o | flagship | "1" |
| `o1-mini` | o | mini | "1" |
| `claude-4-opus-*` | claude | opus | "4" |
| `claude-4-sonnet-*` | claude | sonnet | "4" |
| `claude-4-haiku-*` | claude | haiku | "4" |
| `gemini-3-pro*` | gemini | pro | "3" |
| `gemini-2.5-flash` | gemini | flash | "2.5" |
| `mistral-large-*` | mistral | large | "large-2411" |
| `mistral-small-*` | mistral | small | "small-2409" |
| `codestral-*` | codestral | latest | "latest" |

### 2. Before/After Example

**BEFORE** (current format):
```yaml
name: claude-adversarial
description: Adversarial review using Claude 4 Opus
model: claude-4-opus-20260115
api_key_env: ANTHROPIC_API_KEY
output_suffix: -claude-adversarial.md
timeout: 180
```

**AFTER** (with model_requirement):
```yaml
name: claude-adversarial
description: Adversarial review using Claude 4 Opus
model: claude-4-opus-20260115
api_key_env: ANTHROPIC_API_KEY
model_requirement:
  family: claude
  tier: opus
  min_version: "4"
output_suffix: -claude-adversarial.md
timeout: 180
```

### 3. Important Notes

- **Keep legacy fields**: Do NOT remove `model` or `api_key_env` - they're needed for backwards compatibility
- **Quote versions**: Always use quoted strings for `min_version` (e.g., `"4"` not `4`)
- **Field placement**: Insert `model_requirement` block after `api_key_env`, before `output_suffix`
- **No min_context**: Only add `min_context` if evaluator specifically needs large context (most don't)

## Resources for Implementation

- **Registry**: `providers/registry.yml` - Model family/tier definitions
- **Interface Contract**: `docs/decisions/adr/ADR-0005-library-workflow-interface-contract.md`
- **Task Spec**: `delegation/tasks/2-todo/AEL-0006-add-model-requirement-to-evaluators.md`

## Starting Point

```bash
# 1. Move task to in-progress
./scripts/project start AEL-0006

# 2. Open first evaluator file
# evaluators/anthropic/claude-adversarial/evaluator.yml

# 3. Add model_requirement block after api_key_env

# 4. Repeat for all 18 evaluators

# 5. Run tests
pytest tests/ -v

# 6. Commit and push
```

## Verification Steps

After all updates:

```bash
# 1. Check all evaluators have model_requirement
grep -l "model_requirement:" evaluators/*/*/evaluator.yml | wc -l
# Should output: 18

# 2. Run full test suite
pytest tests/ -v

# 3. Verify YAML is valid
python -c "import yaml; import glob; [yaml.safe_load(open(f)) for f in glob.glob('evaluators/*/*/evaluator.yml')]"
```

## Success Looks Like

- All 18 evaluator files have `model_requirement` block
- All tests pass
- Git shows 18 modified files in evaluators/
- Ready for PR merge

## Notes

- This is a mechanical update - no evaluator behavior changes
- Workflow < 0.8.0 will ignore the new field (backwards compatible)
- Workflow >= 0.8.0 will use model_requirement for resolution
- No need to update index.json or other metadata

---

**Task File**: `delegation/tasks/2-todo/AEL-0006-add-model-requirement-to-evaluators.md`
**Handoff Date**: 2026-02-03
**Coordinator**: Planner
