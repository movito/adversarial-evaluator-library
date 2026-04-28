# Gemini Flash v2 Evaluator

Fast, cost-effective evaluator for quick document assessment, using Google's Gemini 3 Flash.

## Use Cases

- Quick document reviews and assessments
- Fast preliminary evaluations
- Cost-effective bulk processing
- Initial quality checks before deep review

## Performance

| Metric | Value |
|--------|-------|
| Typical response time | 5-15 seconds |
| Timeout setting | 180 seconds |
| Cost | ~$0.001-0.005 per evaluation |

## When to Use

**Best for:**
- First-pass review of any document
- High-volume processing where cost matters
- Quick sanity checks before submission

**Not ideal for:**
- Deep reasoning or complex analysis (use `gemini-deep-v2` or `claude-adversarial`)
- Adversarial review (use `o3-chain` or `claude-adversarial`)
- Large documents (use `gemini-pro`)

## Configuration

```yaml
api_key_env: GEMINI_API_KEY
model: gemini/gemini-3-flash-preview
```

Requires Google AI API key. Set in environment:

```bash
export GEMINI_API_KEY="your-key-here"
```

## Model Note

The underlying model `gemini-3-flash-preview` is currently in preview at Google. This matches the precedent set by `gemini-pro` and `gemini-code` running on `gemini-3.1-pro-preview`. When Google promotes Flash to a stable ID we will release a v3 evaluator and deprecate this one.

## Example Usage

```bash
adversarial evaluate --evaluator gemini-flash-v2 document.md
```

## Replaces

This evaluator replaces `gemini-flash` (Gemini 2.5 Flash). The prompt and output schema are identical; only the underlying model has changed. `gemini-flash` is deprecated as of 2026-04-28 and will be retired in a future release.

## Related Evaluators

- `gemini-pro` — For larger documents and knowledge synthesis
- `gemini-deep-v2` — For extended reasoning tasks
- `fast-check` (OpenAI) — Alternative fast evaluator
- `claude-quick` — Anthropic alternative fast evaluator
