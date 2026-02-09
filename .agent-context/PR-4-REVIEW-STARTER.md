# Review Starter: PR #4 - Anthropic Cross-Provider Usage

**Task**: Anthropic Cross-Provider Usage with litellm Prefixes
**Branch**: feature/anthropic-cross-provider-usage → main
**PR**: https://github.com/movito/adversarial-evaluator-library/pull/4

## Implementation Summary

Added litellm-compatible model ID prefixes to Anthropic and Google evaluators, updated Anthropic models to current versions (Opus 4.6, Sonnet 4.5, Haiku 4.5), and documented the ADV-0032 fix that ensures explicit `model` fields take priority over `model_requirement` resolution. Created comprehensive cross-provider documentation.

- Updated 3 Anthropic evaluators with `anthropic/` prefix and current model IDs
- Updated 1 Google evaluator with `gemini/` prefix
- Added ADR-0006 documenting cross-provider usage decision
- Created cross-provider evaluation guide
- Updated registry with Claude 4.5/4.6 models

## Files Changed

### New Files
- `docs/decisions/adr/ADR-0006-anthropic-cross-provider-usage.md` - Decision record for cross-provider changes
- `docs/guides/CROSS-PROVIDER-EVALUATION.md` - User guide for multi-provider evaluation
- `docs/verification/2026-02-06-resolver-bug-feedback.md` - Feedback document about resolver bug

### Modified Files
- `evaluators/anthropic/claude-adversarial/evaluator.yml` - Model ID: `anthropic/claude-opus-4-6`
- `evaluators/anthropic/claude-code/evaluator.yml` - Model ID: `anthropic/claude-sonnet-4-5`
- `evaluators/anthropic/claude-quick/evaluator.yml` - Model ID: `anthropic/claude-haiku-4-5`
- `evaluators/google/gemini-code/evaluator.yml` - Added `gemini/` prefix
- `evaluators/index.json` - Updated model IDs and descriptions
- `providers/registry.yml` - Added Claude 4.5/4.6 model entries
- `docs/decisions/adr/ADR-0005-library-workflow-interface-contract.md` - Clarified resolution priority (ADV-0032)
- `pyproject.toml` - Bumped `adversarial-workflow>=0.9.3`
- `CHANGELOG.md` - Added v0.9.3 upgrade entry

## Test Results

```
CI Status: PASS (all workflows)
- Tests: PASS
- Lint & Format: PASS

Manual verification:
- ADV-0032 fix verified with 5 test cases
- Explicit model field takes priority: PASS
- Empty model falls back to model_requirement: PASS
- litellm prefixes preserved: PASS
```

## Areas for Review Focus

1. **Registry Model Entries**: Verify new Claude 4.5/4.6 entries in `providers/registry.yml` have correct version numbers and IDs
2. **ADR-0005 Algorithm Update**: The resolution algorithm was revised to show explicit `model` takes priority - verify this matches ADV-0032 behavior
3. **Pricing Accuracy**: Cost estimates in `CROSS-PROVIDER-EVALUATION.md` and `ADR-0006` - are they reasonable?
4. **min_version Alignment**: Evaluator `min_version` fields (4.6 for opus, 4.5 for sonnet/haiku) should now match registry entries

## Related Documentation

- **ADRs**: ADR-0005 (interface contract), ADR-0006 (cross-provider usage)
- **Guide**: `docs/guides/CROSS-PROVIDER-EVALUATION.md`
- **Verification**: `docs/verification/2026-02-06-resolver-bug-feedback.md`

## Pre-Review Checklist (Implementation Agent)

Before requesting review, verify:

- [x] All acceptance criteria implemented
- [x] CI passes (Tests + Lint)
- [x] BugBot feedback addressed (registry model entries)
- [x] CodeRabbit feedback addressed (9 issues fixed)
- [x] No debug code left behind
- [x] Documentation complete

## Commits (6 total)

1. `5fb6286` - feat: Add litellm prefixes to Anthropic/Google evaluators
2. `d5f1b13` - feat: Update Anthropic evaluators to current model IDs
3. `0273d2f` - docs: Add resolver bug feedback for workflow team
4. `d4b8be3` - docs: Update for adversarial-workflow v0.9.3 (ADV-0032 fix)
5. `eff60c1` - fix: Address BugBot and CodeRabbit review feedback
6. `b0fda94` - fix: Clarify cost estimates are per-evaluation

---

**Ready for code-reviewer agent in new tab**

To start review:
1. Open new Claude Code tab
2. Invoke `code-reviewer` agent
3. Provide this file path: `.agent-context/PR-4-REVIEW-STARTER.md`
