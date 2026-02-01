# AEL-0001 Handoff: Write Project README

**Target Agent**: feature-developer
**Created**: 2026-01-31
**Planner**: coordinator

---

## Mission

Write comprehensive documentation for the adversarial-evaluator-library that enables users to understand, install, and use the evaluator library effectively.

## Context

This is a library of adversarial evaluators for AI-assisted document review. It provides 9 pre-configured evaluators across 3 providers, organized into 6 categories.

**Validation Status** (AEL-0002 completed):
- ✅ 48/48 smoke tests passed
- ✅ All 9 evaluators validated
- ✅ CI pipeline clean

## Library Structure

### Providers & Evaluators

| Provider | Evaluator | Model | Category |
|----------|-----------|-------|----------|
| **Google** | gemini-flash | gemini/gemini-2.5-flash | quick-check |
| | gemini-pro | gemini/gemini-3-pro | knowledge-synthesis |
| | gemini-deep | gemini/gemini-2.5-flash | deep-reasoning |
| **OpenAI** | fast-check | gpt-4o-mini | quick-check |
| | gpt52-reasoning | gpt-5.2 | adversarial |
| | o3-chain | o3 | deep-reasoning |
| **Mistral** | mistral-fast | mistral/mistral-small-2409 | quick-check |
| | mistral-content | mistral/mistral-large-2411 | cognitive-diversity |
| | codestral-code | mistral/codestral-latest | code-review |

### Categories

| Category | Purpose |
|----------|---------|
| `quick-check` | Fast, cost-effective initial review |
| `deep-reasoning` | Extended analysis for complex content |
| `adversarial` | Stress-testing and critical review |
| `knowledge-synthesis` | Large-context cross-referencing |
| `cognitive-diversity` | Alternative model perspectives |
| `code-review` | Code and configuration analysis |

### API Keys Required

| Provider | Environment Variable |
|----------|---------------------|
| Google | `GEMINI_API_KEY` |
| OpenAI | `OPENAI_API_KEY` |
| Mistral | `MISTRAL_API_KEY` |

## Current README

```markdown
# adversarial-evaluator-library

A library for adversarial evaluation of AI models.

---

Built with [Agentive Starter Kit](https://github.com/movito/agentive-starter-kit)
```

**Target**: Expand to ~150-200 lines with comprehensive documentation.

## Required Sections

### 1. Header & Badges
- Project title
- Brief tagline
- Badges: CI status, version, license

### 2. Overview (2-3 paragraphs)
- What is adversarial evaluation?
- Why use this library?
- Key benefits

### 3. Quick Start
- Installation command
- API key setup
- Run first evaluation (3-5 commands)

### 4. Available Evaluators
- Table of all 9 evaluators
- Link to individual READMEs

### 5. Categories Explained
- Description of each category
- When to use which

### 6. Usage Examples
- Basic evaluation
- Using specific evaluator
- Evaluator configuration format

### 7. Configuration
- evaluator.yml structure
- Required fields
- Custom evaluators

### 8. Development
- Running tests
- Adding evaluators
- Contributing

### 9. Footer
- License
- "Built with Agentive Starter Kit" credit

## Key Files to Reference

| File | Purpose |
|------|---------|
| `evaluators/index.json` | Complete evaluator metadata |
| `evaluators/openai/fast-check/evaluator.yml` | Example config |
| `evaluators/openai/fast-check/README.md` | Example evaluator docs |
| `tests/test_evaluators.py` | Test commands |
| `.env.template` | Environment setup |

## Evaluator Config Structure

```yaml
name: fast-check
description: Fast validation using GPT-4o-mini
model: gpt-4o-mini
api_key_env: OPENAI_API_KEY
output_suffix: -fast-check.md
timeout: 180

prompt: |
  [Prompt template with {content} placeholder]
```

## Execution Steps

### Step 1: Mark Task In Progress

```bash
./scripts/project start AEL-0001
```

### Step 2: Read Source Materials

1. Read `evaluators/index.json` for complete evaluator list
2. Read one evaluator.yml for config structure example
3. Read `.env.template` for environment setup

### Step 3: Write README

Update `README.md` with all required sections.

### Step 4: Verify

```bash
# Check markdown renders correctly
cat README.md

# Ensure no broken links (if any internal links added)
```

### Step 5: Run Tests

```bash
# Ensure nothing broke
pytest tests/ -v -m "not requires_api"
```

### Step 6: Complete Task

```bash
./scripts/project complete AEL-0001
```

## Success Criteria

| Criterion | Target |
|-----------|--------|
| README length | 150-200 lines |
| All evaluators listed | 9/9 |
| Working examples | ≥2 |
| Sections complete | All 9 required sections |
| Badges | CI status at minimum |

## Style Guidelines

- Use tables for structured data (evaluators, categories)
- Include copy-paste ready code blocks
- Keep explanations concise but complete
- Use consistent heading hierarchy
- Preserve "Built with Agentive Starter Kit" footer

## References

- Task spec: `delegation/tasks/2-todo/AEL-0001-write-project-readme.md`
- Evaluator index: `evaluators/index.json`
- Example config: `evaluators/openai/fast-check/evaluator.yml`
- Test results: AEL-0002 (48/48 passed)
