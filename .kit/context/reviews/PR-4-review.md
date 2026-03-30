# Review: PR-4 - Anthropic Cross-Provider Usage

**Reviewer**: code-reviewer
**Date**: 2026-02-08
**Task File**: N/A (Review started from PR-4-REVIEW-STARTER.md)
**Verdict**: CHANGES_REQUESTED
**Round**: 1

## Summary

Implementation adds litellm-compatible model ID prefixes to Anthropic and Google evaluators, updates Anthropic models to current versions (4.5/4.6), and documents the ADV-0032 fix. Created comprehensive cross-provider documentation and updated the provider registry with new Claude model entries.

## Acceptance Criteria Verification

Based on the review starter and implementation analysis:

- [x] **litellm prefixes added** - Verified in 3 Anthropic evaluators (`anthropic/`) and 1 Google evaluator (`gemini/`)
- [x] **Model IDs updated** - Anthropic evaluators now use current model IDs (Opus 4.6, Sonnet 4.5, Haiku 4.5)
- [x] **ADR-0006 created** - Decision record documents cross-provider usage
- [x] **Cross-provider guide** - Comprehensive user guide created
- [x] **Registry updated** - Claude 4.5/4.6 models added to provider registry
- [x] **CI passes** - Main branch CI is passing (feature branch has no push-triggered workflows)

## Code Quality Assessment

| Aspect | Rating | Notes |
|--------|--------|-------|
| Patterns | Good | Consistent litellm prefix application across evaluators |
| Testing | Needs Work | No automated tests for new model IDs |
| Documentation | Good | Comprehensive cross-provider guide and ADR |
| Architecture | Good | Follows ADR-0005 interface contract |

## Findings

### HIGH: Inconsistent Model Version Metadata
**File**: `providers/registry.yml:112-162`
**Issue**: Registry entries for Claude 4.5/4.6 models have mismatched version and ID fields. For example, `claude-opus-4-6` has `version: "4.6"` but `claude-haiku-4-5` also claims version `"4.5"` when it should be consistent with the ID format.
**Suggestion**: Verify all version fields match the model ID format. If `claude-opus-4-6` represents version 4.6, then the version field should consistently reflect this across all models.
**ADR Reference**: ADR-0005 (registry schema requirements)

### HIGH: Missing min_version Alignment Verification
**File**: `evaluators/anthropic/*/evaluator.yml`
**Issue**: Review starter mentions verifying `min_version` fields (4.6 for opus, 4.5 for sonnet/haiku) match registry entries, but this wasn't explicitly verified during review.
**Suggestion**: Confirm that `min_version: "4.6"` in claude-adversarial aligns with `version: "4.6"` in registry, and same for 4.5 models.

### MEDIUM: Cost Estimates Need Verification
**File**: `docs/guides/CROSS-PROVIDER-EVALUATION.md:52-58`
**Issue**: Cost estimates (~$0.001, ~$0.005, ~$0.015) are marked "per-evaluation estimates" but should be verified against current Anthropic pricing.
**Suggestion**: Verify these estimates match current Anthropic API pricing at https://anthropic.com/pricing or add disclaimer that prices may change.

### MEDIUM: Registry Schema Version Consistency
**File**: `providers/registry.yml:10`
**Issue**: Registry uses `schema_version: "1.0"` but this is the first time Claude 4.5/4.6 models are added. Per ADR-0005, adding new models should increment patch version.
**Suggestion**: Consider if schema version should be `"1.0.1"` for the new model additions, or clarify if this is still considered part of 1.0.0.

### LOW: Code Block Formatting
**File**: `docs/guides/CROSS-PROVIDER-EVALUATION.md:20`
**Issue**: Code block with environment variables could be more readable with shell highlighting.
**Suggestion**: Change `\`\`\`bash` to `\`\`\`bash` for syntax highlighting.

## Recommendations

1. **Add integration test** - Consider adding a basic test that verifies the new model IDs can be loaded by adversarial-workflow
2. **Pricing update process** - Document how cost estimates in the guide will be maintained as provider pricing changes
3. **Version alignment checker** - Consider a script that validates min_version fields in evaluators match registry entries

## Decision

**Verdict**: CHANGES_REQUESTED

**Rationale**: Implementation is well-structured and follows architectural decisions correctly. However, there are data consistency issues in the registry (model versions) and missing verification of the min_version alignment that could cause resolution issues.

**Required Changes**:
1. Fix registry model version consistency - ensure version fields match model ID format
2. Verify min_version fields in evaluators align with registry entries
3. Verify or add disclaimer for cost estimates in documentation

Once these issues are addressed, this implementation will provide excellent cross-provider support for Claude evaluators.
