# AEL-0005 Handoff: Phase 1 Evaluator Implementation

**Task**: `delegation/tasks/2-todo/AEL-0005-phase1-evaluator-implementation.md`
**Agent**: feature-developer
**Created**: 2026-02-01
**Updated**: 2026-02-02
**Evaluation**: 2 rounds with GPT-5.2 adversarial evaluator ($0.07 total)

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

## Output Format Invariants (CRITICAL)

All prompts MUST produce output matching this schema for downstream parser compatibility:

```markdown
## Findings

### [CRITICAL/HIGH/MEDIUM/LOW]: [Finding Title]
- **Location**: [file:line or code reference]
- **Issue**: [Description]
- **Remediation**: [How to fix]

## Overall Assessment
[Risk summary and verdict]
```

## Behavioral Test Requirements

**sample_secure.py**:
- Returns non-empty markdown
- No false critical issues

**sample_vulnerable.py**:
- Detects at least 2 of 4 seeded vulnerabilities:
  - SQL injection
  - XSS (cross-site scripting)
  - Hardcoded secrets
  - Path traversal
- Each finding includes: severity, line reference, remediation

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

## Timeout Tiers (Revised)

| Category | Target | Hard Timeout |
|----------|--------|--------------|
| quick-check | <60s | 90s |
| standard (code-review, adversarial, cognitive-diversity, knowledge-synthesis) | <120s | 180s |
| deep-reasoning | <180s | 300s |

## Completion Checklist

- [ ] Created 6 evaluator directories with evaluator.yml
- [ ] Created README.md for each evaluator
- [ ] Created CHANGELOG.md for each evaluator
- [ ] Updated evaluators/index.json (6 new entries)
- [ ] All config validation tests pass
- [ ] Tested at least one evaluator from each provider against fixtures
- [ ] Updated main README.md evaluator count (12 → 18)

## Refinements from Evaluation (Nice-to-Have)

The following were noted in GPT-5.2 evaluation but deferred to implementation:

1. **Model IDs are "proposed until validated"** - Verify each works before committing
2. **Behavioral test scoring** - Define pass/fail clearly when implementing tests
3. **Schema validation** - Consider adding test that parses output for required sections

## Resources

- ADR-0002: `docs/decisions/adr/ADR-0002-evaluator-expansion-strategy.md`
- Testing Guide: `docs/EVALUATOR-TESTING-GUIDE.md`
- Test Fixtures: `tests/fixtures/code_samples/`
- Task File: `delegation/tasks/2-todo/AEL-0005-phase1-evaluator-implementation.md`

---

**Ready for implementation. Run `./scripts/project start AEL-0005` to begin.**
