# magistral-reasoning

Deep reasoning using Magistral Medium - Mistral's dedicated reasoning model.

## Overview

This evaluator uses Magistral Medium (`magistral-medium-2507`), Mistral's purpose-built reasoning model, for methodical multi-step analysis. Unlike Mistral Large 3 (a general-purpose model applied to reasoning), Magistral is architecturally optimized for chain-of-thought reasoning tasks.

Adds a genuinely different reasoning architecture to the deep-reasoning panel alongside `o3-chain` (OpenAI), `gemini-deep` (Google), and `mistral-deep` (Mistral Large 3).

## Use Cases

- **Complex multi-step logical analysis**: Extended reasoning chains with shown work
- **Calculation verification**: Independent step-by-step reworking of numerical claims
- **Assumption stress-testing**: Sensitivity analysis on key assumptions
- **Scenario analysis**: What-if testing when assumptions shift
- **Cross-provider reasoning panel**: Pair with `o3-chain`, `gemini-deep`, and `mistral-deep`

## Model

- **Model**: `mistral/magistral-medium-2507` (Magistral Medium 1.2)
- **Provider**: Mistral AI
- **Category**: deep-reasoning
- **Timeout**: 480s

## Cost Estimate

~$0.03-0.08 per evaluation. Comparable to `mistral-deep` but uses a reasoning-specialized architecture.

## Example Usage

```bash
# Deep reasoning analysis
adversarial evaluate --evaluator magistral-reasoning docs/analysis.md

# Cross-provider reasoning panel
adversarial evaluate --evaluator o3-chain docs/analysis.md
adversarial evaluate --evaluator gemini-deep docs/analysis.md
adversarial evaluate --evaluator magistral-reasoning docs/analysis.md
```

## Output

The evaluator produces:

1. **Analysis Summary** — what was analyzed and overall reasoning quality
2. **Verification Results** — table of claims vs. independent assessment
3. **Reasoning Findings** — categorized as LOGIC, CALCULATION, ASSUMPTION, or CONSISTENCY
4. **Assumption Risk Map** — sensitivity and likelihood-of-change for key assumptions
5. **Verdict**: SOUND, NEEDS_REVISION, or UNRELIABLE

## When to Use

| Scenario | Use magistral-reasoning? |
|----------|--------------------------|
| Dedicated reasoning model perspective | Yes |
| Cross-provider reasoning panel | Yes |
| Assumption sensitivity testing | Yes |
| General-purpose Mistral perspective | No, use mistral-deep |
| Adversarial stress-testing | No, use mistral-adversarial |
| Quick check | No, use mistral-fast |

## See Also

- [o3-chain](../../openai/o3-chain/) — Chain-of-thought reasoning (OpenAI o3)
- [gemini-deep](../../google/gemini-deep/) — Extended reasoning (Google Gemini 2.5 Pro)
- [mistral-deep](../mistral-deep/) — Deep reasoning (Mistral Large 3)
