# Cognitive Diversity in Evaluation

Why using multiple model families matters.

## The Problem: Shared Blind Spots

Models from the same family (same company, similar training) share:
- Training data biases
- Fine-tuning approaches
- Reasoning patterns
- Systematic blind spots

**If GPT-5.2 misses something, another GPT model probably will too.**

## The Solution: Model Family Diversity

Use evaluators from different families to minimize shared blind spots:

| Family | Provider | Training Emphasis | Evaluators |
|--------|----------|-------------------|------------|
| OpenAI | OpenAI | US-centric, reasoning-heavy | gpt52-reasoning, o3-chain, fast-check |
| Mistral | Mistral AI | European, multilingual | mistral-content, mistral-fast, codestral-code |
| Google | Google | Large-scale web data | gemini-flash, gemini-pro, gemini-deep |
| Anthropic | Anthropic | Constitutional AI, safety | (Your Claude instance) |

## Practical Application

### For Claude Users (You)

Since you're likely using Claude for orchestration:

1. **Don't use Claude to evaluate Claude's work** - same blind spots
2. **Use external evaluators** for independent review
3. **Combine families** for maximum coverage

### Recommended Combinations

**Minimal diversity (2 families):**
- Claude (orchestration) + GPT-5.2 (review)

**Good diversity (3 families):**
- Claude + GPT-5.2 + Mistral

**Maximum diversity (4 families):**
- Claude + GPT-5.2 + Mistral + Gemini

## What Each Family Catches

Based on observed patterns:

### OpenAI (GPT-5.2, o3)
- Strong at: Logical inconsistencies, argument structure
- May miss: Culturally-specific issues, European regulatory nuances

### Mistral
- Strong at: European context, multilingual content
- May miss: US-specific references, some technical jargon

### Google (Gemini)
- Strong at: Factual verification, large-context synthesis
- May miss: Subtle logical flaws, nuanced arguments

### Anthropic (Claude)
- Strong at: Nuanced reasoning, ethical considerations
- May miss: What it was trained to be cautious about

## Synthesis Strategy

When combining outputs from multiple models:

1. **Consensus = High Confidence**
   - If 2+ models flag the same issue, it's almost certainly real
   - Prioritize consensus issues

2. **Contradictions = Investigate**
   - If models disagree, dig deeper
   - May reveal nuanced issues neither fully captured

3. **Unique Findings = Evaluate**
   - Single-model findings may be valid insights
   - Or may be model-specific quirks
   - Use judgment

## Implementation

See `compositions/` for ready-to-use multi-model patterns:

```bash
# High-stakes panel (3 families)
# See compositions/high-stakes-panel.yml

# Adversarial trio
# See compositions/adversarial-trio.yml
```

## References

- ADR-006: Evaluator Library Architecture
- devils-advocate agent: Implements hybrid model pattern
