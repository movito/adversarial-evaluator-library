# Agent Integration Guide

How to use evaluators from Claude agents.

## Basic Pattern

Agents can invoke evaluators via the Bash tool:

```bash
adversarial evaluate evaluators/<provider>/<name>/evaluator.yml <document>
```

Output appears in `.adversarial/logs/`.

## Agent Prompt Template

Add this section to agent definitions that need evaluation:

```markdown
## External Evaluation (Cognitive Diversity)

For independent review, invoke external evaluators via Bash:

**Quick check:**
```bash
adversarial evaluate evaluators/openai/fast-check/evaluator.yml <file>
```

**Deep review:**
```bash
adversarial evaluate evaluators/openai/gpt52-reasoning/evaluator.yml <file>
```

**Read results:**
```bash
cat .adversarial/logs/<filename>-gpt52-reasoning.md
```
```

## Example: Devils-Advocate Agent

The devils-advocate agent demonstrates the hybrid pattern:

```markdown
## Hybrid Model Architecture

1. **You (Claude) orchestrate** - determine what to review
2. **External models critique** - via evaluators
3. **You synthesize** - combine findings with context

**Workflow:**
1. Receive document to review
2. Read and understand content
3. Invoke external evaluator(s)
4. Read evaluator output
5. Synthesize with your own analysis
6. Produce final review
```

## Evaluator Selection in Agents

Guide agents on which evaluator to use:

```markdown
**When to use which evaluator:**

| Situation | Evaluator | Rationale |
|-----------|-----------|-----------|
| Quick sanity check | `fast-check` | Speed, low cost |
| Policy documents | `gpt52-reasoning` | Deep reasoning |
| European context | `mistral-content` | Training emphasis |
| Complex logic | `o3-chain` | Chain-of-thought |
| High-stakes | Run multiple | Cognitive diversity |
```

## Multi-Evaluator Pattern

For important reviews, run multiple evaluators:

```bash
# Run panel
adversarial evaluate evaluators/openai/gpt52-reasoning/evaluator.yml doc.md
adversarial evaluate evaluators/mistral/mistral-content/evaluator.yml doc.md

# Synthesize (agent does this)
# - Issues found by both = HIGH priority
# - Single-model issues = review for validity
```

## Reading Results

Evaluator outputs go to `.adversarial/logs/`:

```bash
# List recent evaluations
ls -lt .adversarial/logs/ | head -10

# Read specific result
cat .adversarial/logs/document-gpt52-reasoning.md
```

## Error Handling

If evaluation fails:

```bash
# Check for timeout (increase if needed)
# Check API key is set
echo $OPENAI_API_KEY | head -c 10

# Retry with different evaluator
adversarial evaluate evaluators/google/gemini-flash/evaluator.yml doc.md
```

## Best Practices

1. **Always read the output** - don't just run and forget
2. **Synthesize, don't copy** - add your judgment to evaluator findings
3. **Use appropriate evaluator** - match to document type
4. **Consider cost** - quick-check first for routine docs
5. **Document your process** - note which evaluators were run
