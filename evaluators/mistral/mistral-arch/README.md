# mistral-arch

Architectural review using Mistral Large - alternative provider perspective on design quality.

## Overview

This evaluator uses Mistral's most capable model (`mistral-large-2512` / Mistral Large 3, 256K context) to perform architectural-level code review. It focuses on structural quality — coupling, cohesion, API design, pattern consistency, and growth readiness — rather than line-level bugs or style.

As a European-headquartered provider, Mistral brings cognitive diversity to architectural review panels. Pairing this evaluator with `arch-review` (OpenAI o1) or `arch-review-fast` (Gemini Flash) in a composition gives genuinely independent structural assessments.

## Use Cases

- **Alternative-provider arch review**: Independent structural assessment from a different model family
- **Coupling analysis**: Detect tight coupling, circular dependencies, layering violations
- **API surface review**: Evaluate whether public APIs are minimal, intuitive, and idiomatic
- **Design conformance**: Verify implementations match their design documents
- **Growth assessment**: Predict how well the current structure will hold under increasing complexity
- **Cross-provider panel**: Use alongside OpenAI/Google arch-review evaluators for cognitive diversity

## Model

- **Model**: `mistral/mistral-large-2512`
- **Provider**: Mistral AI
- **Category**: arch-review
- **Timeout**: 480s

## Cost Estimate

~$0.04-0.12 per review depending on code size. Significantly cheaper than o1-based `arch-review` (~$0.10-0.30) while providing an independent perspective.

## Example Usage

```bash
# Review a core module's architecture
adversarial evaluate --evaluator mistral-arch src/your_project/core.py

# Review a data model's structure
adversarial evaluate --evaluator mistral-arch src/models/event.py

# Use in a cross-provider panel with arch-review
adversarial evaluate --evaluator arch-review src/core.py
adversarial evaluate --evaluator mistral-arch src/core.py
# Compare findings — consensus issues are high-confidence
```

## Output

The evaluator produces:

1. **Architecture Summary** — what the code does and overall structural assessment
2. **Design Quality Assessment** — ratings for responsibility, coupling, cohesion, API surface, pattern consistency, growth readiness
3. **Architectural Findings** — categorized as COUPLING, COHESION, API, PATTERN, BOUNDARY, or RISK
4. **Positive Architecture Decisions** — structural choices worth preserving
5. **Growth Risk Assessment** — low/medium/high-risk areas
6. **Verdict**: APPROVED, REVISION_SUGGESTED, or RESTRUCTURE_NEEDED

## When to Use

| Scenario | Use mistral-arch? |
|----------|-------------------|
| Cross-provider architectural panel | Yes — pair with arch-review or arch-review-fast |
| Independent arch review (alternative to OpenAI/Google) | Yes |
| Cost-conscious arch review (cheaper than o1) | Yes |
| Deepest possible reasoning (o1 chain-of-thought) | No, use arch-review |
| Fastest possible arch check | No, use arch-review-fast |
| Line-level security review | No, use codestral-code or claude-code |

## See Also

- [arch-review](../../openai/arch-review/) — Deep reasoning arch review (OpenAI o1)
- [arch-review-fast](../../google/arch-review-fast/) — Fast arch review (Gemini Flash)
- [codestral-code](../codestral-code/) — Line-level code review (Mistral Codestral)
- [mistral-content](../mistral-content/) — Document/content review (Mistral Large)
