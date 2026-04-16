# claude-arch

Architectural review using Claude Opus 4.7 for structural quality analysis.

## Overview

This evaluator uses Claude Opus 4.7 (`claude-opus-4-7`), Anthropic's most capable model, for deep architectural analysis. It evaluates code structure, coupling, cohesion, API surface quality, and growth readiness.

Fills the arch-review coverage gap for Anthropic, joining `arch-review` (OpenAI o3), `arch-review-fast` (Google Gemini Flash), and `mistral-arch` (Mistral Large 3) for full 4-provider architectural review coverage.

## Use Cases

- **Design document conformance**: Verify code matches its design intent
- **Coupling and cohesion analysis**: Evaluate component boundaries and dependencies
- **API surface quality**: Check public API intuitiveness, consistency, and minimality
- **Growth readiness assessment**: Will the structure hold at 2-3x complexity?
- **Cross-provider architectural panel**: Pair with `arch-review`, `arch-review-fast`, or `mistral-arch`

## Model

- **Model**: `anthropic/claude-opus-4-7` (Claude Opus 4.7)
- **Provider**: Anthropic
- **Category**: arch-review
- **Timeout**: 300s

## Cost Estimate

~$0.05-0.15 per evaluation. Premium tier (Opus pricing) but provides the deepest Anthropic analysis.

## Example Usage

```bash
# Architectural review
adversarial evaluate --evaluator claude-arch src/core/

# Cross-provider architectural panel
adversarial evaluate --evaluator arch-review src/core/
adversarial evaluate --evaluator claude-arch src/core/
adversarial evaluate --evaluator mistral-arch src/core/
```

## Output

The evaluator produces:

1. **Architecture Summary** — role and overall structural quality assessment
2. **Design Adherence** — ratings for independence, API quality, coupling, cohesion, pattern consistency
3. **Architectural Findings** — categorized as STRUCTURAL, COUPLING, API, or PATTERN
4. **Positive Architecture Decisions** — well-made choices to preserve
5. **Growth Risk Assessment** — low/medium/high risk areas
6. **Verdict**: APPROVED, REVISION_SUGGESTED, or RESTRUCTURE_NEEDED

## Prompt Design

Includes prompt injection guardrails (content treated as untrusted data). 5-phase protocol:

1. **Design Intent** — understand purpose and responsibility
2. **Concept Independence** — coupling, cohesion, boundaries
3. **API Surface Quality** — intuitiveness, predictability, minimality
4. **Pattern Consistency** — alignment with project conventions
5. **Growth and Maintenance** — structural resilience under complexity growth

## When to Use

| Scenario | Use claude-arch? |
|----------|------------------|
| Deep architectural analysis | Yes |
| Cross-provider arch-review panel | Yes |
| Anthropic perspective on structure | Yes |
| Fast architectural check | No, use arch-review-fast |
| Code-level bug finding | No, use claude-code |
| Adversarial stress-testing | No, use claude-adversarial |

## See Also

- [arch-review](../../openai/arch-review/) — Deep architectural review (OpenAI o3)
- [arch-review-fast](../../google/arch-review-fast/) — Fast arch review (Gemini 2.5 Flash)
- [mistral-arch](../../mistral/mistral-arch/) — Architectural review (Mistral Large 3)
- [claude-adversarial](../claude-adversarial/) — Adversarial review (Claude Opus 4.7)
