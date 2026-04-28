# code-reviewer-fast-v2

Fast adversarial correctness check using Gemini 3 Flash.

## Overview

This is the fast variant of [code-reviewer](../../openai/code-reviewer/). Same adversarial
mindset (find bugs, not verify acceptance criteria), but with a condensed protocol optimized
for speed and cost.

Use this for small changes, iteration cycles, or as a pre-push sanity check. Use the full
`code-reviewer` for substantial PRs with new logic.

## Use Cases

- **Quick edge case scan** for changes under 50 lines
- **Iteration cycles** — re-run after fixing evaluator findings
- **Pre-push check** — catch obvious boundary issues before bots see the code
- **Cost-sensitive reviews**

## When to Use

| Scenario | Use code-reviewer-fast-v2? |
|----------|----------------------------|
| Small feature PR (<50 lines) | Yes |
| Re-checking after fixes | Yes |
| Pre-push sanity check | Yes |
| Large feature PR (>100 lines) | No, use code-reviewer |
| Security-critical code | No (use claude-code or codestral-code-v2) |

## Model

- **Model**: `gemini/gemini-3-flash-preview`
- **Provider**: Google
- **Category**: code-review
- **Timeout**: 180s

## Cost Estimate

~$0.003–0.01 per review. Extremely cost-effective for iteration.

## Example Usage

```bash
# Quick check on a small change
adversarial code-reviewer-fast-v2 .adversarial/inputs/TASK-001-code-review-input.md

# Read findings
cat .adversarial/logs/TASK-001-code-review-input--code-reviewer-fast-v2.md
```

## Output

The evaluator produces:

1. **Findings** — categorized as CORRECTNESS, ROBUSTNESS, or TESTING
2. **Test Gap Summary** — table of edge cases and coverage status
3. **Verdict**: PASS, CONCERNS, or FAIL

## Model Note

The underlying model `gemini-3-flash-preview` is currently in preview at Google. This matches
the precedent set by `gemini-pro` and `gemini-code` running on `gemini-3.1-pro-preview`. When
Google promotes Flash to a stable ID we will release a v3 evaluator and deprecate this one.

## Replaces

This evaluator replaces `code-reviewer-fast` (Gemini 2.5 Flash). The prompt and output schema
are identical; only the underlying model has changed. `code-reviewer-fast` is deprecated as of
2026-04-28 and will be retired in a future release.

## See Also

- [code-reviewer](../../openai/code-reviewer/) — Full adversarial review
- [gemini-code](../gemini-code/) — Security-focused code review
- [codestral-code-v2](../../mistral/codestral-code-v2/) — Mistral alternative for code review
