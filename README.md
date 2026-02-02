# adversarial-evaluator-library

[![CI](https://github.com/movito/adversarial-evaluator-library/actions/workflows/ci.yml/badge.svg)](https://github.com/movito/adversarial-evaluator-library/actions/workflows/ci.yml)
[![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)](https://github.com/movito/adversarial-evaluator-library/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**A library of adversarial evaluators for AI-assisted document review.**

## Overview

Adversarial evaluation is the practice of using AI models to critically review documents, code, and specifications *before* they're finalized. Rather than waiting for bugs or issues to surface in production, adversarial evaluators stress-test your content by looking for gaps, inconsistencies, and potential problems.

This library provides **18 pre-configured evaluators** across **4 providers** (Anthropic, Google, OpenAI, Mistral), organized into **6 categories**. Each evaluator is tuned for specific review tasks—from quick formatting checks to deep reasoning analysis.

**Why use this library?**

- **Catch issues early**: Find problems in specs, docs, and code before implementation
- **Multi-model perspectives**: Different AI models catch different issues
- **Cost-optimized**: Choose fast/cheap evaluators for quick checks, powerful ones for critical reviews
- **Ready to use**: Pre-configured prompts and settings for common review tasks

## Quick Start

### 1. Clone and Install

```bash
git clone https://github.com/movito/adversarial-evaluator-library.git
cd adversarial-evaluator-library
pip install -e .
```

### 2. Set Up API Keys

Copy the environment template and add your API keys:

```bash
cp .env.template .env
```

Edit `.env` with your keys:

```bash
ANTHROPIC_API_KEY=sk-ant-...  # For Anthropic evaluators
OPENAI_API_KEY=sk-...         # For OpenAI evaluators
GEMINI_API_KEY=...            # For Google evaluators
MISTRAL_API_KEY=...           # For Mistral evaluators
```

### 3. Run Your First Evaluation

```bash
# Run a quick check on a document
adversarial evaluate --evaluator fast-check your-document.md

# Or use the default evaluator
adversarial evaluate your-document.md
```

## Available Evaluators

| Evaluator | Provider | Model | Category | Description |
|-----------|----------|-------|----------|-------------|
| `claude-quick` | Anthropic | claude-4-haiku | quick-check | Fast validation using Claude 4 Haiku |
| `fast-check` | OpenAI | gpt-4o-mini | quick-check | Fast validation for formatting and basic issues |
| `gemini-flash` | Google | gemini-2.5-flash | quick-check | Fast, cost-effective document assessment |
| `mistral-fast` | Mistral | mistral-small-2409 | quick-check | Fast Mistral review for large documents |
| `gemini-deep` | Google | gemini-2.5-flash | deep-reasoning | Extended reasoning for complex analysis |
| `o3-chain` | OpenAI | o3 | deep-reasoning | Chain-of-thought for numerical verification |
| `claude-adversarial` | Anthropic | claude-4-opus | adversarial | Adversarial review for critical analysis |
| `gpt52-reasoning` | OpenAI | gpt-5.2 | adversarial | Deep adversarial reasoning for critical review |
| `gemini-pro` | Google | gemini-3-pro | knowledge-synthesis | Large-context knowledge synthesis (1M tokens) |
| `gpt5-synthesis` | OpenAI | gpt-5-turbo | knowledge-synthesis | Knowledge synthesis for cross-referencing |
| `gpt5-diversity` | OpenAI | gpt-5-turbo | cognitive-diversity | Alternative perspectives and assumption auditing |
| `mistral-content` | Mistral | mistral-large-2411 | cognitive-diversity | Content review with European perspective |
| `claude-code` | Anthropic | claude-4-sonnet | code-review | Security-focused code review |
| `gemini-code` | Google | gemini-3-pro | code-review | Code review for security and quality |
| `o1-code-review` | OpenAI | o1 | code-review | Deep reasoning code review |
| `o1-mini-code` | OpenAI | o1-mini | code-review | Cost-effective reasoning-based code review |
| `gpt4o-code` | OpenAI | gpt-4o | code-review | Fast comprehensive code quality review |
| `codestral-code` | Mistral | codestral-latest | code-review | Code-focused review for scripts and configs |

## Categories

### quick-check
Fast, cost-effective evaluators for initial review. Use these for:
- Pre-commit sanity checks
- Formatting validation
- Spelling and grammar review
- **Evaluators**: `claude-quick`, `fast-check`, `gemini-flash`, `mistral-fast`

### deep-reasoning
Extended analysis for complex content requiring careful thought:
- Technical specifications
- Architecture documents
- Complex logic verification
- **Evaluators**: `gemini-deep`, `o3-chain`

### adversarial
Stress-testing and critical review to find edge cases:
- Security review
- Specification completeness
- Assumption validation
- **Evaluators**: `claude-adversarial`, `gpt52-reasoning`

### knowledge-synthesis
Large-context cross-referencing for comprehensive analysis:
- Documentation consistency
- Cross-document references
- Knowledge base review
- **Evaluators**: `gemini-pro`, `gpt5-synthesis`

### cognitive-diversity
Alternative model perspectives for broader coverage:
- Second-opinion reviews
- Cultural/regional considerations
- Bias detection
- **Evaluators**: `gpt5-diversity`, `mistral-content`

### code-review
Specialized code and configuration analysis:
- Code quality review
- Security vulnerability detection
- Configuration validation
- Script analysis
- **Evaluators**: `claude-code`, `gemini-code`, `o1-code-review`, `o1-mini-code`, `gpt4o-code`, `codestral-code`

## Usage Examples

### Basic Evaluation

```bash
# Evaluate a document with default settings
adversarial evaluate README.md

# Use a specific evaluator
adversarial evaluate --evaluator gemini-deep spec.md

# Evaluate multiple files
adversarial evaluate --evaluator fast-check docs/*.md
```

### Using Category-Based Selection

```bash
# Run all quick-check evaluators
adversarial evaluate --category quick-check document.md

# Run deep analysis
adversarial evaluate --category deep-reasoning architecture.md
```

### Programmatic Usage

```python
from adversarial_evaluator import Evaluator

# Load an evaluator
evaluator = Evaluator.load("fast-check")

# Run evaluation
result = evaluator.evaluate("path/to/document.md")

# Check results
print(result.verdict)  # PASSED, NEEDS_REVISION, or BLOCKED
print(result.findings)
```

## Configuration

Each evaluator is configured via a YAML file in `evaluators/<provider>/<name>/evaluator.yml`.

### Evaluator Configuration Structure

```yaml
name: fast-check
description: Fast validation using GPT-4o-mini
model: gpt-4o-mini
api_key_env: OPENAI_API_KEY
output_suffix: -fast-check.md
timeout: 180

prompt: |
  Your evaluation prompt here.

  {content}

  Include specific checks and output format.
```

### Configuration Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique evaluator identifier |
| `description` | Yes | Human-readable description |
| `model` | Yes | Model identifier |
| `api_key_env` | Yes | Environment variable for API key |
| `output_suffix` | No | Suffix for output files |
| `timeout` | No | Max execution time in seconds |
| `prompt` | Yes | Evaluation prompt with `{content}` placeholder |

### Adding Custom Evaluators

1. Create a new directory: `evaluators/<provider>/<name>/`
2. Add `evaluator.yml` with your configuration
3. Add `README.md` documenting the evaluator
4. Update `evaluators/index.json` with metadata

## API Keys

| Provider | Environment Variable | Get Key |
|----------|---------------------|---------|
| Anthropic | `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com/settings/keys) |
| OpenAI | `OPENAI_API_KEY` | [platform.openai.com](https://platform.openai.com/api-keys) |
| Google | `GEMINI_API_KEY` | [aistudio.google.com](https://aistudio.google.com/app/apikey) |
| Mistral | `MISTRAL_API_KEY` | [console.mistral.ai](https://console.mistral.ai/codestral) |

**Cost estimates per evaluation:**
- Quick-check evaluators: ~$0.001-0.01
- Deep-reasoning evaluators: ~$0.05-0.20
- Knowledge-synthesis: ~$0.01-0.05

## Development

### Running Tests

```bash
# Run all tests (requires API keys)
pytest tests/ -v

# Run tests without API calls
pytest tests/ -v -m "not requires_api"

# Run specific test file
pytest tests/test_evaluators.py -v
```

### Project Structure

```
evaluators/
├── index.json           # Evaluator registry
├── anthropic/           # Anthropic/Claude evaluators
│   ├── claude-adversarial/
│   ├── claude-code/
│   └── claude-quick/
├── google/              # Google/Gemini evaluators
│   ├── gemini-flash/
│   ├── gemini-pro/
│   ├── gemini-deep/
│   └── gemini-code/
├── openai/              # OpenAI evaluators
│   ├── fast-check/
│   ├── gpt52-reasoning/
│   ├── gpt5-diversity/
│   ├── gpt5-synthesis/
│   ├── o1-code-review/
│   ├── o1-mini-code/
│   ├── gpt4o-code/
│   └── o3-chain/
└── mistral/             # Mistral evaluators
    ├── mistral-fast/
    ├── mistral-content/
    └── codestral-code/
```

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-evaluator`
3. Add your evaluator following the configuration structure above
4. Add tests for your evaluator
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) for details.

---

Built with [Agentive Starter Kit](https://github.com/movito/agentive-starter-kit)
