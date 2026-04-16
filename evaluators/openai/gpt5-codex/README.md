# GPT-5.3 Codex Code Review Evaluator

Code-specialized review evaluator using OpenAI's GPT-5.3 Codex model for deep code understanding.

## Overview

GPT-5.3 Codex is OpenAI's code-specialized model, purpose-built for code comprehension and analysis. Unlike general-purpose models used for code review, Codex has deeper understanding of programming constructs, algorithms, and code patterns.

## Use Cases

- Deep code comprehension and logic review
- Algorithm correctness verification
- Code generation quality assessment
- Refactoring opportunity identification
- Cross-language code review

## Configuration

```yaml
api_key_env: OPENAI_API_KEY
model: gpt-5.3-codex
```

## Example Usage

```bash
adversarial gpt5-codex src/core/engine.py
adversarial gpt5-codex src/**/*.py
```

## Output

The evaluator produces:
- Code summary and structural analysis
- Correctness findings (BUG/LOGIC/BOUNDARY/RESOURCE/ROBUSTNESS)
- Algorithm assessment table with complexity analysis
- Verdict: APPROVED / CHANGES_REQUESTED / REJECT

## Comparison

| Evaluator | Model | Approach | Best For |
|-----------|-------|----------|----------|
| `gpt5-codex` | GPT-5.3 Codex | Code-specialized | Deep code understanding, algorithms |
| `gpt4o-code` | GPT-5.4 | General-purpose | Quick PR reviews, style, docs |
| `code-reviewer` | o3 | Adversarial reasoning | Edge cases, boundary conditions |
| `claude-code` | Claude Sonnet 4.6 | Security-focused | Security vulnerabilities |
