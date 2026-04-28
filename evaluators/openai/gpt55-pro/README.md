# GPT-5.5 Pro Deep Reasoning Evaluator

Extended reasoning evaluator using OpenAI's GPT-5.5 Pro for complex multi-step analysis.

## Overview

GPT-5.5 Pro is OpenAI's extended reasoning variant of GPT-5.5 (released April 2026). It provides a different reasoning approach from o3, making it valuable for multi-model reasoning panels where diverse perspectives catch different issues. Compared to GPT-5.4 Pro, GPT-5.5 Pro brings a 1,050K context window (128K output) and ~60% fewer hallucinations.

## Use Cases

- Complex multi-step analysis requiring extended thinking
- Architecture and design document deep review
- Risk assessment with scenario modeling
- Cross-document consistency verification
- Decision framework evaluation

## Configuration

```yaml
api_key_env: OPENAI_API_KEY
model: gpt-5.5-pro
```

## Example Usage

```bash
adversarial gpt55-pro architecture-spec.md
adversarial gpt55-pro risk-assessment.md
```

## Output

The evaluator produces:
- Reasoning chain review table
- Findings by category (LOGIC/COMPLETENESS/RISK/CONSISTENCY)
- Risk assessment matrix
- Verdict: SOUND / NEEDS_REVISION / UNRELIABLE

## Replaces

This evaluator replaces `gpt54-pro` (GPT-5.4 Pro). The prompt and output schema are identical; only the underlying model has changed. `gpt54-pro` is deprecated as of 2026-04-28 and will be retired in a future release.

## Comparison

| Evaluator | Model | Approach | Best For |
|-----------|-------|----------|----------|
| `gpt55-pro` | GPT-5.5 Pro | Extended reasoning | Complex analysis, risk modeling |
| `o3-chain` | o3 | Chain-of-thought | Numerical verification, calculations |
| `magistral-reasoning` | Magistral Medium | Dedicated reasoning | Assumption stress-testing |
| `gemini-deep-v2` | Gemini 3.1 Pro Preview | Extended thinking | Large-context analysis |
