# mistral-deep

Deep reasoning evaluation using Mistral Large 3 - multi-step analysis and verification.

## Overview

This evaluator uses Mistral Large 3 (`mistral-large-2512`, 256K context) for methodical, step-by-step reasoning through complex analysis. It independently verifies calculations, maps assumption dependencies, tests sensitivity, and checks internal consistency.

Provides a third independent perspective alongside `o3-chain` (OpenAI) and `gemini-deep` (Google) for deep reasoning tasks.

## Use Cases

- **Calculation verification**: Independently work through numerical claims step-by-step
- **Multi-step logical analysis**: Verify reasoning chains, find skipped steps
- **Assumption mapping**: Surface implicit assumptions and test their sensitivity
- **Scenario analysis**: What happens when key assumptions change?
- **Internal consistency checking**: Do aggregates match components? Are definitions stable?
- **Cross-provider reasoning panel**: Pair with `o3-chain` and `gemini-deep`

## Model

- **Model**: `mistral/mistral-large-2512` (Mistral Large 3)
- **Provider**: Mistral AI
- **Category**: deep-reasoning
- **Timeout**: 480s

## Cost Estimate

~$0.03-0.10 per evaluation depending on content complexity. Comparable to `o3-chain`, cheaper than `gemini-deep` for most documents (Gemini Pro pricing at scale).

## Example Usage

```bash
# Verify a financial analysis
adversarial evaluate --evaluator mistral-deep docs/financial-model.md

# Cross-provider deep reasoning panel
adversarial evaluate --evaluator o3-chain docs/analysis.md
adversarial evaluate --evaluator gemini-deep docs/analysis.md
adversarial evaluate --evaluator mistral-deep docs/analysis.md
```

## Output

The evaluator produces:

1. **Analysis Summary** — what was analyzed and overall reasoning quality
2. **Verification Results** — table of claims vs. independent assessment
3. **Reasoning Findings** — categorized as LOGIC, CALCULATION, ASSUMPTION, or CONSISTENCY
4. **Assumption Risk Map** — sensitivity and likelihood-of-change for key assumptions
5. **What's Sound** — well-reasoned aspects worth preserving
6. **Verdict**: SOUND, NEEDS_REVISION, or UNRELIABLE

## Prompt Design

5-phase protocol optimized for methodical verification:

1. **Decomposition** — break content into verifiable claims and calculations
2. **Independent Verification** — rework each claim step-by-step, show work
3. **Assumption Sensitivity** — test what happens when assumptions shift
4. **Internal Consistency** — cross-check aggregates, definitions, related sections
5. **Reasoning Chain Completeness** — find gaps, unstated conclusions, alternative explanations

## When to Use

| Scenario | Use mistral-deep? |
|----------|-------------------|
| Cross-provider deep reasoning panel | Yes |
| Independent calculation verification | Yes |
| Assumption sensitivity testing | Yes |
| Deepest possible reasoning (single model) | No, use o3-chain (dedicated reasoning model) |
| Large document analysis (>100K tokens) | Yes — 256K context handles it |
| Quick check | No, use mistral-fast |
| Adversarial stress-testing | No, use mistral-adversarial |

## See Also

- [o3-chain](../../openai/o3-chain/) — Chain-of-thought reasoning (OpenAI o3)
- [gemini-deep](../../google/gemini-deep/) — Extended reasoning (Google Gemini 2.5 Pro)
- [mistral-adversarial](../mistral-adversarial/) — Adversarial review (Mistral Large 3)
- [mistral-arch](../mistral-arch/) — Architectural review (Mistral Large 3)
