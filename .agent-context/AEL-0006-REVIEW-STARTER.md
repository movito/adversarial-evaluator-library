# Review Starter: AEL-0006

**Task**: AEL-0006 - Add model_requirement to Existing Evaluators
**Task File**: `delegation/tasks/4-in-review/AEL-0006-add-model-requirement-to-evaluators.md`
**Branch**: ael-0006-model-requirement → main
**PR**: https://github.com/movito/adversarial-evaluator-library/pull/3

## Implementation Summary

Added `model_requirement` blocks to all 18 evaluator.yml files to enable Phase 2 model resolution in adversarial-workflow v0.8.0. This is a mechanical update that adds new fields while preserving backwards compatibility with legacy `model` and `api_key_env` fields.

- Added `model_requirement` block with `family`, `tier`, and `min_version` fields to each evaluator
- All values verified against `providers/registry.yml` for correctness
- Field placement consistent: after `api_key_env`, before `output_suffix`

## Files Changed

### Modified Files (18 evaluator.yml files)

**OpenAI (8 files)**:
- `evaluators/openai/gpt52-reasoning/evaluator.yml` - Added gpt/flagship/5.2
- `evaluators/openai/o3-chain/evaluator.yml` - Added o/flagship/3
- `evaluators/openai/o1-code-review/evaluator.yml` - Added o/flagship/1
- `evaluators/openai/o1-mini-code/evaluator.yml` - Added o/mini/1
- `evaluators/openai/gpt4o-code/evaluator.yml` - Added gpt/standard/4o
- `evaluators/openai/fast-check/evaluator.yml` - Added gpt/mini/4o-mini
- `evaluators/openai/gpt5-diversity/evaluator.yml` - Added gpt/flagship/5
- `evaluators/openai/gpt5-synthesis/evaluator.yml` - Added gpt/flagship/5

**Anthropic (3 files)**:
- `evaluators/anthropic/claude-adversarial/evaluator.yml` - Added claude/opus/4
- `evaluators/anthropic/claude-code/evaluator.yml` - Added claude/sonnet/4
- `evaluators/anthropic/claude-quick/evaluator.yml` - Added claude/haiku/4

**Google (4 files)**:
- `evaluators/google/gemini-pro/evaluator.yml` - Added gemini/pro/3
- `evaluators/google/gemini-flash/evaluator.yml` - Added gemini/flash/2.5
- `evaluators/google/gemini-deep/evaluator.yml` - Added gemini/flash/2.5
- `evaluators/google/gemini-code/evaluator.yml` - Added gemini/pro/3

**Mistral (3 files)**:
- `evaluators/mistral/mistral-content/evaluator.yml` - Added mistral/large/large-2411
- `evaluators/mistral/mistral-fast/evaluator.yml` - Added mistral/small/small-2409
- `evaluators/mistral/codestral-code/evaluator.yml` - Added codestral/latest/latest

## Test Results

```
pytest tests/ -v
156 passed, 31 skipped in 1.44s

./scripts/ci-check.sh
167 passed, 20 skipped in 1.89s
Coverage: 93.04% (required: 80%)

GitHub Actions CI: All checks passed
- Lint & Format Check: 36s
- Run Tests: 46s
```

## Areas for Review Focus

1. **Registry Alignment**: Verify all `family` and `tier` values match entries in `providers/registry.yml`
2. **Version Format**: Confirm all `min_version` values are quoted strings (YAML requirement)
3. **Field Ordering**: Check consistency - `model_requirement` should appear after `api_key_env` and before `output_suffix` in all files
4. **Backwards Compatibility**: Ensure legacy `model` and `api_key_env` fields are preserved (not removed)

## Related Documentation

- **Task file**: `delegation/tasks/4-in-review/AEL-0006-add-model-requirement-to-evaluators.md`
- **ADRs**:
  - ADR-0004 (Evaluator Definition / Model Routing Separation)
  - ADR-0005 (Library-Workflow Interface Contract)
- **Handoff**: `.agent-context/AEL-0006-HANDOFF-feature-developer.md`
- **Registry**: `providers/registry.yml`

## Pre-Review Checklist (Implementation Agent)

Before requesting review, verify:

- [x] All acceptance criteria from task file are implemented
- [x] Tests written and passing (156 passed)
- [x] CI passes (GitHub Actions: all green)
- [x] Task moved to `4-in-review/`
- [x] No debug code or console.logs left behind
- [x] N/A - No new public APIs added (YAML config only)

## Automated Review Status

- **CodeRabbit**: APPROVED (no issues found)
- **CI**: All checks passing
- **BugBot**: Not configured

---

**Ready for code-reviewer agent in new tab**

To start review:
1. Open new Claude Code tab
2. Run: `agents/launch code-reviewer`
3. Reviewer will auto-detect this starter file
