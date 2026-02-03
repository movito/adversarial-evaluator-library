# AEL-0005: Phase 1 Evaluator Implementation

**Status**: Done
**Priority**: high
**Assigned To**: feature-developer
**Estimated Effort**: 8-10 hours
**Created**: 2026-02-01
**Target Completion**: 2026-02-04

## Related Tasks

**Depends On**: None (ADR-0002 approved)
**Related**: [ADR-0002 Evaluator Expansion Strategy](../../docs/decisions/adr/ADR-0002-evaluator-expansion-strategy.md)

## Overview

Implement the 6 evaluators defined in ADR-0002 Phase 1 to achieve multi-provider coverage across all categories. This adds Anthropic as a Tier 1 provider and fills single-provider gaps.

### Current State (from `evaluators/index.json`)

| Provider | Count | Categories Covered |
|----------|-------|-------------------|
| OpenAI | 6 | quick-check, code-review, deep-reasoning, adversarial |
| Google | 3 | quick-check, deep-reasoning, knowledge-synthesis |
| Mistral | 3 | quick-check, code-review, cognitive-diversity |
| **Total** | **12** | |

### Coverage Gaps (Single-Provider Categories)

| Category | Current Provider | Gap |
|----------|-----------------|-----|
| adversarial | OpenAI only | Need 2nd provider |
| cognitive-diversity | Mistral only | Need 2nd provider |
| knowledge-synthesis | Google only | Need 2nd provider |
| code-review | 3 providers | Need Tier 1 Anthropic |

### Target State (After Phase 1)

| Category | OpenAI | Anthropic | Google | Mistral | Total | Multi-Provider? |
|----------|--------|-----------|--------|---------|-------|-----------------|
| quick-check | 1 | 1 | 1 | 1 | 4 | ✅ Yes (4) |
| code-review | 3 | 1 | 1 | 1 | 6 | ✅ Yes (4) |
| deep-reasoning | 1 | 0 | 1 | 0 | 2 | ✅ Yes (2) |
| adversarial | 1 | 1 | 0 | 0 | 2 | ✅ Yes (2) |
| cognitive-diversity | 1 | 0 | 0 | 1 | 2 | ✅ Yes (2) |
| knowledge-synthesis | 1 | 0 | 1 | 0 | 2 | ✅ Yes (2) |
| **Total** | 8 | 3 | 4 | 3 | **18** | **All ≥2** |

### Tier 1 Provider Definition (ADR-0002)

Tier 1 providers meet these criteria:
1. API stability and uptime (enterprise SLA availability)
2. Model capability benchmarks (MMLU, HumanEval, etc.)
3. Adoption in target user base (developer tools, enterprise)
4. Pricing and availability

**Tier 1**: OpenAI, Anthropic, Google

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

**Config Validation:**
- [ ] All evaluators pass Tier 1 config validation tests
- [ ] Valid YAML with required fields: `name`, `description`, `model`, `api_key_env`, `prompt`
- [ ] Pinned model version (not floating reference)
- [ ] Prompt contains `{content}` placeholder

**Behavioral Testing - sample_secure.py:**
- [ ] Returns non-empty response
- [ ] Response is valid markdown
- [ ] Does not raise false critical issues (low false positive rate)

**Behavioral Testing - sample_vulnerable.py:**
- [ ] Detects at least 2 of 4 seeded vulnerabilities:
  - SQL injection
  - XSS (cross-site scripting)
  - Hardcoded secrets
  - Path traversal
- [ ] Each finding includes: severity level, line reference, remediation suggestion
- [ ] Response includes overall risk assessment

**Output Schema Requirements:**
All evaluator outputs must be parseable markdown with:
1. Findings section with severity labels (CRITICAL/HIGH/MEDIUM/LOW)
2. Line or code references for each finding
3. Overall assessment or verdict

**Timeout Tiers:**
| Category | Target | Hard Timeout |
|----------|--------|--------------|
| quick-check | <60s | 90s |
| standard (code-review, adversarial, cognitive-diversity, knowledge-synthesis) | <120s | 180s |
| deep-reasoning | <180s | 300s |

- [ ] Response times documented (average across 3 runs)

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

**Prompt Strategy:**
- `claude-adversarial`: Adapt from gpt52-reasoning prompt (adversarial review)
- `claude-code`: Adapt from o1-code-review prompt (code security/quality)
- `claude-quick`: Adapt from fast-check prompt (rapid validation)

**Output Format Invariants (MUST preserve when adapting):**
```markdown
## Findings

### [CRITICAL/HIGH/MEDIUM/LOW]: [Finding Title]
- **Location**: [file:line or code reference]
- **Issue**: [Description]
- **Remediation**: [How to fix]

## Overall Assessment
[Risk summary and verdict]
```

These invariants ensure downstream parsers can extract findings programmatically.

### Phase 2: Google Evaluator (gemini-code)

```
evaluators/google/gemini-code/
├── evaluator.yml
├── README.md
└── CHANGELOG.md
```

**Prompt Strategy**: Adapt from existing code-review evaluators (o1-code-review, gpt4o-code)

**Output Format**: Same invariants as Anthropic evaluators (see above)

### Phase 3: OpenAI Evaluators (gpt5-*)

```
evaluators/openai/
├── gpt5-diversity/
│   └── ...
└── gpt5-synthesis/
    └── ...
```

**Prompt Strategy:**
- `gpt5-diversity`: Cognitive diversity focus (alternative perspectives)
- `gpt5-synthesis`: Knowledge synthesis (cross-reference, completeness)

**Output Format**: Same invariants as Anthropic evaluators (see Phase 1 section)

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

- `ANTHROPIC_API_KEY` environment variable (for claude-* evaluators)
- `OPENAI_API_KEY` environment variable (for gpt5-* evaluators)
- `GEMINI_API_KEY` environment variable (for gemini-* evaluators)
- Existing evaluator configs as prompt references

## Reference Files

- `docs/decisions/adr/ADR-0002-evaluator-expansion-strategy.md` - Strategy and principles
- `docs/EVALUATOR-TESTING-GUIDE.md` - Testing requirements
- `evaluators/openai/gpt52-reasoning/evaluator.yml` - Adversarial prompt reference
- `evaluators/openai/o1-code-review/evaluator.yml` - Code review prompt reference
- `evaluators/openai/fast-check/evaluator.yml` - Quick check prompt reference

## Effort Breakdown

| Phase | Deliverables | Est. Time |
|-------|--------------|-----------|
| **Phase 1: Anthropic** | 3 evaluators × (config + README + CHANGELOG) | 3-4 hours |
| **Phase 2: Google** | 1 evaluator × (config + README + CHANGELOG) | 1-1.5 hours |
| **Phase 3: OpenAI** | 2 evaluators × (config + README + CHANGELOG) | 2-2.5 hours |
| **Phase 4: Integration** | index.json, tests, README update | 1.5-2 hours |
| **Total** | 6 evaluators, 18+ files | **8-10 hours** |

**Note**: Effort includes prompt engineering and behavioral testing. Config creation is templated; prompt adaptation requires thought.

## Notes

- Use pinned model versions per ADR-0002 Principle 3
- Follow naming convention: `{model-family}-{category}`
- Copy evaluator.yml to `.adversarial/evaluators/` to test locally
- Model ID validation: Run smoke test before committing (`adversarial <evaluator-name> tests/fixtures/code_samples/sample_secure.py`)

## Model ID Validation

Before committing each evaluator, verify model IDs work with provider APIs:

```bash
# Anthropic (requires ANTHROPIC_API_KEY)
adversarial claude-adversarial tests/fixtures/code_samples/sample_secure.py

# Google (requires GEMINI_API_KEY)  
adversarial gemini-code tests/fixtures/code_samples/sample_secure.py

# OpenAI (requires OPENAI_API_KEY)
adversarial gpt5-diversity tests/fixtures/code_samples/sample_secure.py
```

If model ID fails, check provider documentation and update `evaluator.yml` with correct model identifier.

---

**Template Version**: 1.1.0
