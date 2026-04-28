# GPT-5.5 Knowledge Synthesis Evaluator

Cross-reference and completeness validation using GPT-5.5 for comprehensive knowledge synthesis.

## Use Cases

- Synthesizing information across documents
- Cross-referencing multiple sources
- Knowledge gap identification
- Consistency checking across deliverables
- Research completeness verification
- Multi-document coherence analysis

## Performance

| Metric | Value |
| -------- | ----- |
| Typical response time | 25-50 seconds |
| Timeout setting | 180 seconds |
| Cost | ~$0.02-0.06 per evaluation |

## When to Use

**Best for:**
- Multi-section document review
- Verifying internal consistency
- Finding coverage gaps
- Cross-referencing claims
- Research synthesis validation

**Not ideal for:**
- Quick checks (use `fast-check`)
- Code review (use code-focused evaluators)

## Synthesis Capabilities

This evaluator identifies:
- Internal contradictions
- Coverage gaps
- Inconsistent terminology
- Missing cross-references
- Unsynthesized patterns

## Why GPT-5.5 for Synthesis?

GPT-5.5 provides strong analytical capabilities with a 1,050K context window (128K output) and ~60% fewer hallucinations than GPT-5.4. For very large document sets, you can also combine with `gemini-pro` (Gemini 3.1 Pro Preview, 1M context) for cross-provider synthesis verification.

## Configuration

```yaml
api_key_env: OPENAI_API_KEY
model: gpt-5.5
```

## Example Usage

```bash
adversarial evaluate --evaluator gpt55-synthesis research-report.md
```

## Output Format

Findings use standardized severity labels:
- **CRITICAL**: Major inconsistency or critical gap
- **HIGH**: Significant coverage issue to address
- **MEDIUM**: Notable gap worth filling
- **LOW**: Minor synthesis opportunity

Each finding identifies the inconsistency or gap and how to address it.

## Replaces

This evaluator replaces `gpt5-synthesis` (GPT-5.4). The prompt and output schema are identical; only the underlying model has changed. `gpt5-synthesis` is deprecated as of 2026-04-28 and will be retired in a future release.

## Related Evaluators

- `gemini-pro` — Google synthesis with 1M context window
- `gpt55-diversity` — Alternative perspective analysis (same provider)
- `mistral-content` — Content structure review
