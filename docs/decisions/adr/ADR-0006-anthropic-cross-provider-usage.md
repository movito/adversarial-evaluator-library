# ADR-0006: Anthropic Cross-Provider Usage

**Status**: Draft

**Date**: 2026-02-06

**Deciders**: adversarial-evaluator-library team

## Context

### Problem Statement

Users often run their core agents on one provider (e.g., OpenAI GPT-4, Google Gemini) but want to use Claude models as evaluators for:

1. **Cognitive diversity** - Different models catch different issues
2. **Adversarial perspective** - Claude's reasoning style differs from other models
3. **Specialized capabilities** - Claude excels at certain evaluation tasks

We need to make cross-provider usage straightforward.

### Current State

We have 3 Anthropic evaluators:

| Evaluator | Model | Use Case |
|-----------|-------|----------|
| claude-adversarial | Claude 4 Opus | Critical adversarial review |
| claude-code | Claude 4 Sonnet | Security-focused code review |
| claude-quick | Claude 4 Haiku | Fast validation checks |

### Issues Identified

**1. Model ID Format Inconsistency**

Current Anthropic evaluators use native model IDs:
```yaml
model: claude-4-opus-20260115
```

But litellm (used by adversarial-workflow) requires the `anthropic/` prefix:
```yaml
model: anthropic/claude-4-opus-20260115
```

Other providers are already correctly prefixed:
- Mistral: `mistral/mistral-large-2411` ✅
- Google: `gemini/gemini-2.5-flash` ✅
- OpenAI: No prefix needed (default provider) ✅

**2. Documentation Gap**

No guide exists for users who want to:
- Use Claude evaluators alongside a non-Claude agent
- Configure multiple API keys for cross-provider workflows
- Understand why cognitive diversity in evaluation matters

**3. API Key Clarity**

Users need `ANTHROPIC_API_KEY` but this isn't prominently documented for the cross-provider use case.

## Decision

### 1. Fix Model ID Format

Update all Anthropic evaluators to use litellm-compatible model IDs:

```yaml
# Before
model: claude-4-opus-20260115

# After
model: anthropic/claude-4-opus-20260115
```

### 2. Add Cross-Provider Documentation

Create `docs/guides/CROSS-PROVIDER-EVALUATION.md` covering:

- Why use multiple providers for evaluation
- How to configure API keys
- Recommended evaluator combinations
- Cost considerations

### 3. Verify with Testing

Test the Anthropic evaluators using the same procedure as OpenAI/Google/Mistral.

## Implementation

### Phase 1: Fix Model IDs

Update 3 files:
- `evaluators/anthropic/claude-adversarial/evaluator.yml`
- `evaluators/anthropic/claude-code/evaluator.yml`
- `evaluators/anthropic/claude-quick/evaluator.yml`

### Phase 2: Documentation

Create cross-provider guide with:

```markdown
## Recommended Cross-Provider Combinations

### For OpenAI/GPT Users
Use Claude evaluators for:
- `claude-adversarial` - Different reasoning approach catches blind spots
- `claude-code` - Security-focused review with different perspective

### For Google/Gemini Users
Use Claude evaluators for:
- `claude-quick` - Fast second-opinion validation
- `claude-adversarial` - Rigorous adversarial challenge

### API Key Setup
```bash
# .env file
OPENAI_API_KEY=sk-...      # For your main agent
ANTHROPIC_API_KEY=sk-ant-... # For Claude evaluators
```
```

### Phase 3: Testing

```bash
# Install Claude evaluator
adversarial library install anthropic/claude-quick --yes

# Test with a document
adversarial evaluate --evaluator claude-quick /tmp/test-document.md
echo $?  # Should be 0
```

## Consequences

### Positive

- ✅ Claude evaluators work out-of-the-box with litellm
- ✅ Cross-provider usage is documented and straightforward
- ✅ Users get cognitive diversity in their evaluation pipeline

### Negative

- ⚠️ Breaking change for anyone using old model IDs directly
- ⚠️ Requires users to have Anthropic API key

### Neutral

- 📊 Anthropic API costs apply (~$0.015/1K input for Opus, less for Sonnet/Haiku)

## Alternatives Considered

### A. Keep Native IDs, Let Workflow Handle Prefix

The workflow could auto-add prefixes based on provider detection.

**Rejected**: Adds complexity to workflow, inconsistent with other providers in library.

### B. Support Both Formats

Allow both `claude-4-opus` and `anthropic/claude-4-opus`.

**Rejected**: Confusing, maintenance burden, doesn't solve the core issue.

## Related Decisions

- ADR-0004: Evaluator Definition / Model Routing Separation
- ADR-0005: Library-Workflow Interface Contract

## References

- [litellm Anthropic Documentation](https://docs.litellm.ai/docs/providers/anthropic)
- [Anthropic API Pricing](https://anthropic.com/pricing)
