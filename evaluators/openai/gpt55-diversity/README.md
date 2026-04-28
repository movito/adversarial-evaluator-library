# GPT-5.5 Cognitive Diversity Evaluator

Alternative perspective analysis using GPT-5.5 to surface blind spots and challenge assumptions.

## Use Cases

- Cross-checking other model outputs
- Alternative perspective analysis
- Bias detection in recommendations
- Assumption challenging
- Multi-viewpoint validation
- Stakeholder impact analysis

## Performance

| Metric | Value |
| -------- | ----- |
| Typical response time | 25-45 seconds |
| Timeout setting | 180 seconds |
| Cost | ~$0.02-0.06 per evaluation |

## When to Use

**Best for:**
- Final review after other evaluators
- Detecting groupthink in recommendations
- Surfacing unconsidered perspectives
- Validating inclusivity of solutions
- Cross-checking AI-generated content

**Not ideal for:**
- Technical correctness (use code reviewers)
- Quick validation (use `fast-check`)
- Factual verification (use `gpt55-adversarial`)

## Cognitive Diversity Value

This evaluator specifically looks for:
- Implicit assumptions
- Underrepresented stakeholder views
- Edge cases others might miss
- Contrarian perspectives
- Domain knowledge gaps

## Why GPT-5.5 for Diversity?

Using OpenAI's flagship for cognitive diversity provides a different "thinking style" than Mistral's `mistral-content`. Running both gives maximum coverage of alternative viewpoints. GPT-5.5 brings ~60% fewer hallucinations than GPT-5.4, which matters when surfacing speculative perspectives.

## Configuration

```yaml
api_key_env: OPENAI_API_KEY
model: gpt-5.5
```

## Example Usage

```bash
adversarial evaluate --evaluator gpt55-diversity proposal-document.md
```

## Output Format

Findings use standardized severity labels:
- **CRITICAL**: Major blind spot affecting core validity
- **HIGH**: Significant perspective gap to address
- **MEDIUM**: Notable assumption worth examining
- **LOW**: Minor alternative viewpoint to consider

Each finding includes the overlooked perspective and how to incorporate it.

## Replaces

This evaluator replaces `gpt5-diversity` (GPT-5.4). The prompt and output schema are identical; only the underlying model has changed. `gpt5-diversity` is deprecated as of 2026-04-28 and will be retired in a future release.

## Related Evaluators

- `mistral-content` — Mistral alternative perspective (European training)
- `gpt55-adversarial` — Adversarial analysis (same provider)
- `claude-adversarial` — Anthropic critical review
