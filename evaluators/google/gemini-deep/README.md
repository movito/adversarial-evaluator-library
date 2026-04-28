# Gemini Deep Think Evaluator

> **DEPRECATED (2026-04-28)** — superseded by [`gemini-deep-v2`](../gemini-deep-v2/), which runs on `gemini-3.1-pro-preview` (aligning with sibling Gemini Pro evaluators). This evaluator remains callable until retirement; new work should target `gemini-deep-v2`.

Extended reasoning evaluator for complex analysis and deep thinking.

## Use Cases

- Complex policy analysis requiring deep reasoning
- Multi-step logical evaluation
- Critical thinking and assumption testing
- Counter-argument development
- Second-order effect analysis

## Performance

| Metric | Value |
|--------|-------|
| Typical response time | 90-300 seconds |
| Timeout setting | 600 seconds |
| Cost | Varies by input size (token-priced, see Google AI pricing) |

## When to Use

**Best for:**
- Complex arguments needing thorough analysis
- Finding hidden assumptions
- Developing counter-arguments
- Policy document stress-testing

**Not ideal for:**
- Quick checks (use gemini-flash-v2)
- Very large documents (use gemini-pro)
- Factual verification (use o3-chain)

## Configuration

```yaml
api_key_env: GEMINI_API_KEY
```

## Related Evaluators

- `gpt55-adversarial` - Alternative deep reasoning (OpenAI)
- `o3-chain` - Chain-of-thought verification
- `gemini-flash-v2` - Quick preliminary check
