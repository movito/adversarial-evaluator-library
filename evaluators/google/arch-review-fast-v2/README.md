# arch-review-fast-v2

Fast architectural review using Gemini 3 Flash extended reasoning.

## Overview

A lighter, faster alternative to `arch-review` for quick architectural sanity checks. Uses Gemini 3 Flash to evaluate structural quality: coupling, cohesion, API design, pattern consistency, and growth readiness — all at a fraction of the cost and time of the o1-based evaluator.

## Use Cases

- **Quick sanity check**: Run before a deeper `arch-review` to catch obvious structural issues
- **Pre-merge gate**: Fast architectural check as part of the review workflow
- **During development**: Get rapid feedback on structural decisions while coding
- **Routine PRs**: Architectural check for standard feature work

## Model

- **Model**: `gemini/gemini-3-flash-preview`
- **Provider**: Google
- **Category**: arch-review
- **Timeout**: 180s

## Cost Estimate

~$0.003-0.01 per review. Roughly 30x cheaper than `arch-review`.

## Example Usage

```bash
# Quick architectural check during development
adversarial evaluate --evaluator arch-review-fast-v2 src/your_project/core.py

# Run on another file
adversarial evaluate --evaluator arch-review-fast-v2 src/your_project/models/event.py
```

## Output

The evaluator produces:

1. **Quick Assessment Table** — ratings across 6 dimensions (responsibility, coupling, cohesion, API, patterns, growth)
2. **Findings** — categorized as COUPLING, COHESION, API, PATTERN, or RISK
3. **What's Good** — decisions worth preserving
4. **Verdict**: APPROVED, REVISION_SUGGESTED, or RESTRUCTURE_NEEDED

## When to Use

| Scenario | Use arch-review-fast-v2? |
|----------|--------------------------|
| Routine PR review | Yes |
| Quick check during development | Yes |
| Pre-merge gate | Yes |
| Foundational/critical components | No, use arch-review |
| Security-focused review | No, use claude-code or codestral-code-v2 |
| Line-level bug finding | No, use code-reviewer-fast-v2 |

## Model Note

The underlying model `gemini-3-flash-preview` is currently in preview at Google. This matches
the precedent set by `gemini-pro` and `gemini-code` running on `gemini-3.1-pro-preview`. When
Google promotes Flash to a stable ID we will release a v3 evaluator and deprecate this one.

## Replaces

This evaluator replaces `arch-review-fast` (Gemini 2.5 Flash). The prompt and output schema
are identical; only the underlying model has changed. `arch-review-fast` is deprecated as of
2026-04-28 and will be retired in a future release.

## See Also

- [arch-review](../../openai/arch-review/) - Deep architectural review using o3 (slower, more thorough)
- [gemini-code](../gemini-code/) - Line-level code review using Gemini 3.1 Pro
- [gemini-deep-v2](../gemini-deep-v2/) - General extended reasoning analysis
