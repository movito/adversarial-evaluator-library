# mistral-adversarial

Adversarial review using Mistral Large 3 - independent third-provider stress-testing.

## Overview

This evaluator uses Mistral Large 3 (`mistral-large-2512`, 256K context) to perform rigorous adversarial review of documents, proposals, and deliverables. It challenges claims, surfaces hidden assumptions, and stress-tests arguments.

The primary value of this evaluator is **provider diversity for adversarial panels**. Different model families have genuinely different blind spots — an issue that GPT-5.2 and Claude Opus both miss may be caught by Mistral, and vice versa. This completes the three-provider adversarial triangle.

## Use Cases

- **Cross-provider adversarial panel**: Pair with `gpt52-reasoning` and `claude-adversarial` for maximum blind-spot coverage
- **Critical argument stress-testing**: Challenge claims, find logical gaps
- **High-stakes deliverable review**: Final check before publication or implementation
- **Red-teaming**: Surface risks and unintended consequences
- **Independent second opinion**: When you want a different model family's perspective

## Model

- **Model**: `mistral/mistral-large-2512` (Mistral Large 3)
- **Provider**: Mistral AI
- **Category**: adversarial
- **Timeout**: 300s

## Cost Estimate

~$0.02-0.08 per review depending on document size. Comparable to `gpt52-reasoning`, significantly cheaper than `claude-adversarial` (Opus pricing).

## Example Usage

```bash
# Standalone adversarial review
adversarial evaluate --evaluator mistral-adversarial docs/proposal.md

# Three-provider adversarial panel (maximum coverage)
adversarial evaluate --evaluator gpt52-reasoning docs/proposal.md
adversarial evaluate --evaluator claude-adversarial docs/proposal.md
adversarial evaluate --evaluator mistral-adversarial docs/proposal.md
# Consensus issues (found by 2+ models) are high-confidence findings
```

## Output

The evaluator produces:

1. **Findings** — categorized as CRITICAL, HIGH, MEDIUM, or LOW severity
2. **Strengths Worth Preserving** — what's already strong
3. **Verdict**: APPROVED, NEEDS_REVISION, or REJECT with summary

## Prompt Design

The prompt uses a 5-phase protocol:

1. **Factual Verification** — challenge claims, demand evidence, flag vague quantifiers
2. **Logical Structure** — map argument structure, find reasoning gaps
3. **Counterarguments** — strongest opposing view, edge cases, missing perspectives
4. **Risk Assessment** — consequences, second-order effects, worst-case scenarios
5. **Strength Assessment** — identify what's already solid (prevents over-criticism)

Includes a prompt injection guard to treat reviewed content as untrusted data.

## When to Use

| Scenario | Use mistral-adversarial? |
|----------|--------------------------|
| Cross-provider adversarial panel | Yes — completes the three-provider set |
| Independent adversarial review | Yes |
| Cost-conscious adversarial review | Yes — cheaper than Claude Opus |
| Deepest possible adversarial (single model) | No, use claude-adversarial or gpt52-reasoning |
| Quick check | No, use mistral-fast |
| Code review | No, use codestral-code |

## See Also

- [gpt52-reasoning](../../openai/gpt52-reasoning/) — Adversarial review (OpenAI GPT-5.2)
- [claude-adversarial](../../anthropic/claude-adversarial/) — Adversarial review (Anthropic Opus 4.6)
- [mistral-deep](../mistral-deep/) — Deep reasoning (Mistral Large 3)
- [mistral-content](../mistral-content/) — Content/cognitive-diversity review (Mistral Large)
