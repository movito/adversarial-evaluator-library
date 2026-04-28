# GPT-5.5 Adversarial Evaluator

Primary adversarial evaluator for critical document review, using OpenAI's GPT-5.5 (released April 2026).

## Use Cases

- Final document review before publication
- Critical argument stress-testing
- High-stakes deliverable validation
- Complex multi-factor analysis
- Devils-advocate reviews

## Performance

| Metric | Value |
|--------|-------|
| Typical response time | 30-45 seconds |
| Timeout setting | 180 seconds |
| Cost | ~$0.02-0.08 per evaluation |

## When to Use

**Best for:**
- High-stakes final reviews
- Finding logical weaknesses
- Adversarial stress-testing
- Policy and strategy documents

**Not ideal for:**
- Quick checks (use `fast-check`)
- Numerical verification (use `o3-chain`)
- Very large documents (use `gemini-pro`)

## Cognitive Diversity Note

This evaluator provides a different perspective than Claude-based reviews. Use it alongside Claude analysis for maximum blind-spot coverage.

## Configuration

```yaml
api_key_env: OPENAI_API_KEY
model: gpt-5.5
```

## Example Usage

```bash
adversarial evaluate evaluators/openai/gpt55-adversarial/evaluator.yml policy-doc.md
```

## Replaces

This evaluator replaces `gpt52-reasoning`. The old name was a legacy artefact (it referenced gpt-5.2 but had been silently upgraded to gpt-5.4 in 0.7.0); the new name reflects both the actual model (`gpt-5.5`) and the evaluator's category (`adversarial`). The prompt and verdict vocabulary are identical to `gpt52-reasoning` v1.0.0. `gpt52-reasoning` is deprecated as of 2026-04-28 and will be retired in a future release.

## Related Evaluators

- `o3-chain` — Step-by-step logical verification
- `mistral-content` — Alternative perspective (European training)
- `gemini-deep-v2` — Alternative deep reasoning (Google)
- `claude-adversarial` — Anthropic adversarial review
