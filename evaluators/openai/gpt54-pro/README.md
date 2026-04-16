# GPT-5.4 Pro Deep Reasoning Evaluator

Extended reasoning evaluator using OpenAI's GPT-5.4 Pro for complex multi-step analysis.

## Overview

GPT-5.4 Pro is OpenAI's extended reasoning variant of GPT-5.4. It provides a different reasoning approach from o3, making it valuable for multi-model reasoning panels where diverse perspectives catch different issues.

## Use Cases

- Complex multi-step analysis requiring extended thinking
- Architecture and design document deep review
- Risk assessment with scenario modeling
- Cross-document consistency verification
- Decision framework evaluation

## Configuration

```yaml
api_key_env: OPENAI_API_KEY
model: gpt-5.4-pro
```

## Example Usage

```bash
adversarial gpt54-pro architecture-spec.md
adversarial gpt54-pro risk-assessment.md
```

## Output

The evaluator produces:
- Reasoning chain review table
- Findings by category (LOGIC/COMPLETENESS/RISK/CONSISTENCY)
- Risk assessment matrix
- Verdict: SOUND / NEEDS_REVISION / UNRELIABLE

## Comparison

| Evaluator | Model | Approach | Best For |
|-----------|-------|----------|----------|
| `gpt54-pro` | GPT-5.4 Pro | Extended reasoning | Complex analysis, risk modeling |
| `o3-chain` | o3 | Chain-of-thought | Numerical verification, calculations |
| `magistral-reasoning` | Magistral Medium | Dedicated reasoning | Assumption stress-testing |
| `gemini-deep` | Gemini 2.5 Pro | Extended thinking | Large-context analysis |
