# AEL-0005: Phase 1 Evaluator Implementation

**Status**: Todo
**Priority**: high
**Assigned To**: feature-developer
**Estimated Effort**: 4-6 hours
**Created**: 2026-02-01
**Target Completion**: 2026-02-03

## Related Tasks

**Depends On**: None (ADR-0002 approved)
**Related**: ADR-0002-evaluator-expansion-strategy

## Overview

Implement the 6 evaluators defined in ADR-0002 Phase 1 to achieve multi-provider coverage across all categories. This adds Anthropic as a Tier 1 provider and fills single-provider gaps.

**Context**: The library currently has 12 evaluators across 3 providers (OpenAI, Google, Mistral). Phase 1 adds 6 evaluators to reach 18 total across 4 providers, ensuring every category has 2+ providers for cognitive diversity.

## Requirements

### Evaluators to Implement

| Evaluator | Provider | Category | Model |
|-----------|----------|----------|-------|
| `claude-adversarial` | Anthropic | adversarial | claude-4-opus-20260115 |
| `claude-code` | Anthropic | code-review | claude-4-sonnet-20260115 |
| `claude-quick` | Anthropic | quick-check | claude-4-haiku-20260115 |
| `gemini-code` | Google | code-review | gemini-3-pro-20260101 |
| `gpt5-diversity` | OpenAI | cognitive-diversity | gpt-5-turbo-2025-11-01 |
| `gpt5-synthesis` | OpenAI | knowledge-synthesis | gpt-5-turbo-2025-11-01 |

### Per-Evaluator Deliverables

Each evaluator requires:
1. `evaluators/{provider}/{name}/evaluator.yml` - Configuration
2. `evaluators/{provider}/{name}/README.md` - Documentation
3. `evaluators/{provider}/{name}/CHANGELOG.md` - Version history

### Functional Requirements

1. Each evaluator.yml must include:
   - `name`, `description`, `model` (pinned version)
   - `api_key_env`, `output_suffix`, `timeout`
   - `prompt` with `{content}` placeholder

2. Each README.md must include:
   - Use cases and expected behavior
   - Comparison with similar evaluators
   - Example output

3. Update `evaluators/index.json` with all 6 new evaluators

### Non-Functional Requirements

- [ ] All evaluators pass Tier 1 config validation tests
- [ ] All evaluators successfully evaluate `sample_secure.py`
- [ ] All evaluators detect issues in `sample_vulnerable.py`
- [ ] Response times documented (<120s for standard tier)

## Implementation Plan

### Phase 1: Anthropic Evaluators (claude-*)

```
evaluators/anthropic/
├── claude-adversarial/
│   ├── evaluator.yml
│   ├── README.md
│   └── CHANGELOG.md
├── claude-code/
│   └── ...
└── claude-quick/
    └── ...
```

**Prompt Strategy**:
- `claude-adversarial`: Adapt from gpt52-reasoning prompt (adversarial review)
- `claude-code`: Adapt from o1-code-review prompt (code security/quality)
- `claude-quick`: Adapt from fast-check prompt (rapid validation)

### Phase 2: Google Evaluator (gemini-code)

```
evaluators/google/gemini-code/
├── evaluator.yml
├── README.md
└── CHANGELOG.md
```

**Prompt Strategy**: Adapt from existing code-review evaluators

### Phase 3: OpenAI Evaluators (gpt5-*)

```
evaluators/openai/
├── gpt5-diversity/
│   └── ...
└── gpt5-synthesis/
    └── ...
```

**Prompt Strategy**:
- `gpt5-diversity`: Cognitive diversity focus (alternative perspectives)
- `gpt5-synthesis`: Knowledge synthesis (cross-reference, completeness)

### Phase 4: Integration

1. Update `evaluators/index.json`
2. Run full test suite
3. Update README evaluator count (12 → 18)

## Acceptance Criteria

### Must Have
- [ ] All 6 evaluators created with valid YAML configs
- [ ] All 6 evaluators pass config validation tests
- [ ] All 6 evaluators return valid output on test fixtures
- [ ] `evaluators/index.json` updated with all entries
- [ ] Each evaluator has README.md with use cases

### Should Have
- [ ] Prompts tailored to each category's purpose
- [ ] Response times documented in README
- [ ] CHANGELOG.md initialized for each evaluator

### Nice to Have
- [ ] Disagreement testing results vs existing evaluators
- [ ] Cost per evaluation documented

## Success Metrics

### Quantitative
- Evaluators implemented: 6/6
- Config validation tests pass: 6/6
- Categories with 2+ providers: 6/6 (all)
- Total evaluator count: 18

### Qualitative
- Prompts demonstrate category-appropriate evaluation focus
- Documentation enables immediate use

## Testing Approach

```bash
# Config validation
pytest tests/test_evaluators.py -v -k "config"

# Behavioral tests (requires API keys)
pytest tests/test_evaluators.py -v -k "behavioral" --run-api-tests

# Individual evaluator test
adversarial claude-adversarial tests/fixtures/code_samples/sample_vulnerable.py
```

## Dependencies

- ANTHROPIC_API_KEY environment variable (for claude-* evaluators)
- Access to claude-4-opus, claude-4-sonnet, claude-4-haiku models
- Existing evaluator configs as prompt references

## Reference Files

- `docs/decisions/adr/ADR-0002-evaluator-expansion-strategy.md` - Strategy and principles
- `docs/EVALUATOR-TESTING-GUIDE.md` - Testing requirements
- `evaluators/openai/gpt52-reasoning/evaluator.yml` - Adversarial prompt reference
- `evaluators/openai/o1-code-review/evaluator.yml` - Code review prompt reference
- `evaluators/openai/fast-check/evaluator.yml` - Quick check prompt reference

## Notes

- Use pinned model versions per ADR-0002 Principle 3
- Follow naming convention: `{model-family}-{category}`
- Timeout guidelines: quick-check 60s, standard 120-180s, deep 300-400s
- Copy evaluator.yml to `.adversarial/evaluators/` to test locally

---

**Template Version**: 1.0.0
