# Evaluator Selection Guide

Choose the right evaluator for your task.

## Quick Decision Tree

```
Is this a quick sanity check?
├── Yes → fast-check or gemini-flash-v2
└── No
    ├── Is it code/scripts?
    │   └── Yes → codestral-code-v2
    └── No
        ├── Does it have calculations?
        │   └── Yes → o3-chain
        └── No
            ├── Is it high-stakes?
            │   ├── Yes → high-stakes-panel (composition)
            │   └── No
            │       ├── Is it very large (>50k tokens)?
            │       │   └── Yes → gemini-pro
            │       └── No → gpt55-adversarial or gemini-deep-v2
```

## By Use Case

### Quick Checks (< 30 seconds, < $0.01)

| Evaluator | Best For |
|-----------|----------|
| `fast-check` | Formatting, spelling, obvious issues |
| `gemini-flash-v2` | Quick content assessment |
| `mistral-fast` | Large docs with Mistral perspective |

### Deep Analysis (1-2 minutes, $0.02-0.08)

| Evaluator | Best For |
|-----------|----------|
| `gpt55-adversarial` | Adversarial review, logical analysis |
| `gemini-deep-v2` | Complex reasoning, assumptions |
| `o3-chain` | Calculations, step-by-step logic |

### Specialized

| Evaluator | Best For |
|-----------|----------|
| `gemini-pro` | Very large documents (up to 1M tokens) |
| `mistral-content` | European perspective, cognitive diversity |
| `codestral-code-v2` | Code, scripts, configurations |

## By Document Type

### Policy Documents
1. First pass: `fast-check`
2. Deep review: `gpt55-adversarial`
3. Alternative view: `mistral-content`

### Technical Specifications
1. First pass: `fast-check`
2. Logic check: `o3-chain`
3. Deep review: `gemini-deep-v2`

### Code and Scripts
1. `codestral-code-v2` for security and correctness
2. `o3-chain` if calculations involved

### Research Synthesis
1. `gemini-pro` for large context
2. `gpt55-adversarial` for critical review

## Multi-Evaluator Patterns

See `compositions/` for ready-to-use patterns:

- **high-stakes-panel**: Three models for critical docs
- **quick-then-deep**: Fast check, deep only if needed
- **adversarial-trio**: Maximum cognitive diversity

## Cost Optimization

**Budget-conscious workflow:**
1. Always start with `fast-check` ($0.002)
2. Only proceed to deep review if issues found
3. Expected cost: $0.01-0.03 per clean document

**Quality-focused workflow:**
1. Run `quick-then-deep` composition
2. For important docs, add `mistral-content` for diversity
3. Expected cost: $0.05-0.10 per document

**High-stakes workflow:**
1. Run full `high-stakes-panel`
2. Synthesize findings from all three models
3. Expected cost: $0.10-0.20 per document
