# Cross-Provider Evaluation Guide

Use evaluators from different AI providers to get diverse perspectives on your documents and code.

## Why Cross-Provider Evaluation?

Different AI models have different:
- **Training data** - Catch different blind spots
- **Reasoning styles** - Approach problems differently
- **Strengths** - Excel at different tasks

Using evaluators from multiple providers gives you **cognitive diversity** - the AI equivalent of getting a second opinion.

## Quick Start

### 1. Configure API Keys

Add keys for each provider you want to use:

```bash
# .env file
OPENAI_API_KEY=sk-...           # For OpenAI evaluators
ANTHROPIC_API_KEY=sk-ant-...    # For Claude evaluators
GEMINI_API_KEY=...              # For Google evaluators
MISTRAL_API_KEY=...             # For Mistral evaluators
```

### 2. Install Evaluators

```bash
# Install evaluators from different providers
adversarial library install openai/fast-check --yes
adversarial library install anthropic/claude-quick --yes
adversarial library install google/gemini-flash --yes
```

### 3. Run Cross-Provider Evaluation

```bash
# Get perspectives from multiple providers
adversarial evaluate --evaluator fast-check document.md      # OpenAI
adversarial evaluate --evaluator claude-quick document.md    # Anthropic
adversarial evaluate --evaluator gemini-flash document.md    # Google
```

## Using Claude Evaluators with Non-Claude Agents

If your main agent runs on GPT-4, Gemini, or another model, Claude evaluators provide valuable alternative perspectives.

### Recommended Claude Evaluators

| Evaluator | Model | Best For | Cost |
|-----------|-------|----------|------|
| `claude-quick` | Haiku | Fast validation, quick checks | ~$0.001 |
| `claude-code` | Sonnet | Security-focused code review | ~$0.005 |
| `claude-adversarial` | Opus | Critical adversarial analysis | ~$0.015 |

### Example: GPT-4 Agent + Claude Evaluators

```bash
# Your agent uses GPT-4 for development...
# But use Claude for evaluation diversity

# Quick sanity check
adversarial evaluate --evaluator claude-quick my-spec.md

# Security review
adversarial evaluate --evaluator claude-code src/auth.py

# Adversarial stress-test before release
adversarial evaluate --evaluator claude-adversarial release-notes.md
```

### Example: Gemini Agent + Claude Evaluators

```bash
# Gemini for main work, Claude for review
adversarial evaluate --evaluator claude-adversarial architecture.md
```

## Recommended Combinations

### For Document Review

| Phase | Evaluator | Provider | Purpose |
|-------|-----------|----------|---------|
| Quick check | `fast-check` | OpenAI | Catch obvious issues fast |
| Second opinion | `claude-quick` | Anthropic | Different perspective |
| Deep review | `claude-adversarial` | Anthropic | Stress-test arguments |

### For Code Review

| Phase | Evaluator | Provider | Purpose |
|-------|-----------|----------|---------|
| Quick scan | `fast-check` | OpenAI | Syntax and formatting |
| Security | `claude-code` | Anthropic | Vulnerability detection |
| Deep analysis | `o1-code-review` | OpenAI | Logical correctness |

### For Critical Deliverables

Use **all providers** for maximum coverage:

```bash
# Install all quick-check evaluators
adversarial library install openai/fast-check --yes
adversarial library install anthropic/claude-quick --yes
adversarial library install google/gemini-flash --yes
adversarial library install mistral/mistral-fast --yes

# Run all four
for e in fast-check claude-quick gemini-flash mistral-fast; do
  adversarial evaluate --evaluator $e critical-document.md
done
```

## Cost Comparison

| Provider | Cheap | Mid-tier | Premium |
|----------|-------|----------|---------|
| OpenAI | fast-check (~$0.0002) | gpt4o-code (~$0.01) | o1-code-review (~$0.05) |
| Anthropic | claude-quick (~$0.001) | claude-code (~$0.005) | claude-adversarial (~$0.015) |
| Google | gemini-flash (~$0.001) | gemini-pro (~$0.005) | gemini-deep (~$0.01) |
| Mistral | mistral-fast (~$0.0005) | mistral-content (~$0.005) | - |

**Cross-provider quick check (4 evaluators)**: ~$0.003 total

## Troubleshooting

### "Model not found" Error

Ensure the model ID includes the provider prefix:
- ✅ `anthropic/claude-4-opus-20260115`
- ❌ `claude-4-opus-20260115`

### API Key Not Working

Check your `.env` file:
```bash
# Verify key is set
cat .env | grep ANTHROPIC_API_KEY
```

### Rate Limits

If hitting rate limits, add delays between evaluations:
```bash
adversarial evaluate --evaluator claude-quick doc.md
sleep 2
adversarial evaluate --evaluator claude-code doc.md
```

## Best Practices

1. **Start cheap, go deep** - Use quick-check evaluators first, then premium for issues
2. **Mix providers** - Don't use all evaluators from one provider
3. **Match evaluator to task** - Use code evaluators for code, adversarial for specs
4. **Compare outputs** - When evaluators disagree, investigate

## See Also

- [Testing Procedure](../verification/TESTING-PROCEDURE.md)
- [ADR-0006: Anthropic Cross-Provider Usage](../decisions/adr/ADR-0006-anthropic-cross-provider-usage.md)
