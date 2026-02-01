# AEL-0005 Handoff: Phase 1 Evaluator Implementation

**Task**: Implement 6 evaluators per ADR-0002 Phase 1
**Agent**: feature-developer
**Created**: 2026-02-01

## Quick Context

You're adding 6 new evaluators to achieve multi-provider coverage. The library currently has 12 evaluators across 3 providers. After this task: 18 evaluators across 4 providers.

## Critical Details

### Model Versions (MUST use pinned versions)

| Evaluator | Model ID |
|-----------|----------|
| claude-adversarial | `claude-4-opus-20260115` |
| claude-code | `claude-4-sonnet-20260115` |
| claude-quick | `claude-4-haiku-20260115` |
| gemini-code | `gemini-3-pro-20260101` |
| gpt5-diversity | `gpt-5-turbo-2025-11-01` |
| gpt5-synthesis | `gpt-5-turbo-2025-11-01` |

### Directory Structure

```
evaluators/
├── anthropic/           # NEW PROVIDER
│   ├── claude-adversarial/
│   ├── claude-code/
│   └── claude-quick/
├── google/
│   └── gemini-code/     # NEW
├── openai/
│   ├── gpt5-diversity/  # NEW
│   └── gpt5-synthesis/  # NEW
```

### API Key Environment Variables

| Provider | Env Var |
|----------|---------|
| Anthropic | `ANTHROPIC_API_KEY` |
| Google | `GEMINI_API_KEY` |
| OpenAI | `OPENAI_API_KEY` |

## Prompt References

Copy and adapt prompts from these existing evaluators:

| New Evaluator | Reference | Adapt From |
|---------------|-----------|------------|
| claude-adversarial | `evaluators/openai/gpt52-reasoning/evaluator.yml` | Adversarial review structure |
| claude-code | `evaluators/openai/o1-code-review/evaluator.yml` | Code review checklist |
| claude-quick | `evaluators/openai/fast-check/evaluator.yml` | Rapid validation format |
| gemini-code | `evaluators/mistral/codestral-code/evaluator.yml` | Code-focused review |
| gpt5-diversity | `evaluators/mistral/mistral-content/evaluator.yml` | Alternative perspective |
| gpt5-synthesis | `evaluators/google/gemini-pro/evaluator.yml` | Knowledge synthesis |

## Evaluator Template

```yaml
# {Name} Evaluator
# {Description}
#
# Provider: {provider}
# Use cases:
#   - {use case 1}
#   - {use case 2}

name: {evaluator-name}
description: {One-line description}
model: {pinned-model-version}
api_key_env: {API_KEY_ENV}
output_suffix: -{evaluator-name}.md
timeout: {60|120|180|300}

prompt: |
  {Evaluation prompt}

  {content}

  {Output format instructions}
```

## Testing Commands

```bash
# 1. Start task
./scripts/project start AEL-0005

# 2. After creating each evaluator, copy to .adversarial/evaluators/ for testing
cp evaluators/anthropic/claude-adversarial/evaluator.yml .adversarial/evaluators/claude-adversarial.yml

# 3. Test against fixtures
adversarial claude-adversarial tests/fixtures/code_samples/sample_vulnerable.py

# 4. Run config validation
pytest tests/test_evaluators.py -v -k "config"

# 5. Update index.json
# Add entries for all 6 new evaluators

# 6. Final validation
pytest tests/test_evaluators.py -v
```

## index.json Entry Format

```json
{
  "name": "claude-adversarial",
  "provider": "anthropic",
  "model": "claude-4-opus-20260115",
  "category": "adversarial",
  "description": "Adversarial review using Claude 4 Opus",
  "path": "evaluators/anthropic/claude-adversarial"
}
```

## Timeout Guidelines

| Category | Timeout | Rationale |
|----------|---------|-----------|
| quick-check | 60s | Fast validation |
| code-review | 120-180s | Detailed analysis |
| adversarial | 180s | Deep critique |
| cognitive-diversity | 180s | Alternative perspectives |
| knowledge-synthesis | 300-400s | Large context processing |
| deep-reasoning | 300-600s | Extended analysis |

## Completion Checklist

- [ ] Created 6 evaluator directories with evaluator.yml
- [ ] Created README.md for each evaluator
- [ ] Created CHANGELOG.md for each evaluator
- [ ] Updated evaluators/index.json (6 new entries)
- [ ] All config validation tests pass
- [ ] Tested at least one evaluator from each provider against fixtures
- [ ] Updated main README.md evaluator count (12 → 18)

## Resources

- ADR-0002: `docs/decisions/adr/ADR-0002-evaluator-expansion-strategy.md`
- Testing Guide: `docs/EVALUATOR-TESTING-GUIDE.md`
- Test Fixtures: `tests/fixtures/code_samples/`
