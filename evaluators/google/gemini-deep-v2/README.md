# Gemini Deep Think Evaluator (v2)

Extended reasoning evaluator for complex analysis and deep thinking, running on Gemini 3.1 Pro.

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
- Quick checks (use `gemini-flash-v2`)
- Very large documents (use `gemini-pro`)
- Factual verification (use `o3-chain`)

## Configuration

```yaml
api_key_env: GEMINI_API_KEY
model: gemini/gemini-3.1-pro-preview
```

## Model Note

The underlying model `gemini-3.1-pro-preview` is currently in preview at Google. This matches the sibling evaluators `gemini-pro` and `gemini-code`. When Google promotes 3.1 Pro to a stable ID, a v3 evaluator will be released and this one deprecated.

## Replaces

This evaluator replaces `gemini-deep` (which ran on `gemini-2.5-pro`). The prompt and output schema are identical; only the underlying model has changed, and it now aligns with the other Gemini Pro evaluators in this library. `gemini-deep` is deprecated as of 2026-04-28 and will be retired in a future release.

## Related Evaluators

- `gpt55-adversarial` - Alternative deep reasoning (OpenAI)
- `o3-chain` - Chain-of-thought verification
- `gemini-flash-v2` - Quick preliminary check
