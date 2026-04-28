# Codestral Code Review Evaluator (v2)

Code-focused review using Mistral Codestral 2.

## Use Cases

- Script and automation review
- Data processing pipeline validation
- Configuration file analysis
- Calculation and formula verification
- Security review for code

## Performance

| Metric | Value |
|--------|-------|
| Typical response time | 30-60 seconds |
| Timeout setting | 300 seconds |
| Cost | ~$0.01-0.03 per evaluation |
| Context window | 128K tokens |

## When to Use

**Best for:**
- Python, JavaScript, shell scripts
- Configuration files (YAML, JSON, TOML)
- Data processing code
- Financial calculations in code

**Not ideal for:**
- Prose documents (use mistral-content)
- Very large codebases (review file-by-file)

## Configuration

```yaml
api_key_env: MISTRAL_API_KEY
model: mistral/codestral-2
```

## Replaces

This evaluator replaces `codestral-code` (which ran on `mistral/codestral-latest`, ~32K context). The prompt and output schema are identical; the model is now pinned to the explicit `codestral-2` ID and the context window grows to 128K. `codestral-code` is deprecated as of 2026-04-28 and will be retired in a future release.

## Related Evaluators

- `o3-chain` - For numerical verification in docs
- `mistral-content` - For non-code documents
- `fast-check` - For quick formatting checks
