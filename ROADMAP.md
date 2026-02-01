# Roadmap

## Vision

A **starter kit** of adversarial evaluators that demonstrates cognitive diversity across AI providers. Projects clone this library and extend it with their own specialized evaluators.

**Not a goal**: Exhaustive coverage of every model and provider.

## Current State (v1.0.0)

**12 evaluators** across 3 providers:
- OpenAI: 6 evaluators
- Google: 3 evaluators
- Mistral: 3 evaluators

**Coverage gaps**:
- Several categories have single-provider coverage

**Why no Anthropic?** Claude serves as the authoring agent in agentive-starter-kit. We use other model families (OpenAI, Google, Mistral) as adversarial critics to ensure genuine cognitive diversity.

## Phases

### Phase 1: Fill Critical Gaps (Next)

Ensure each category has 2+ providers for cognitive diversity.

| Evaluator | Provider | Category | Priority |
|-----------|----------|----------|----------|
| `gemini-adversarial` | Google | adversarial | High |
| `gemini-code` | Google | code-review | High |
| `gpt5-diversity` | OpenAI | cognitive-diversity | Medium |
| `gpt5-synthesis` | OpenAI | knowledge-synthesis | Medium |

**Target**: 16 evaluators, 3 providers

### Phase 2: Tier 2 Providers

Add Cohere for enterprise/RAG perspective.

| Evaluator | Provider | Category |
|-----------|----------|----------|
| `cohere-reasoning` | Cohere | deep-reasoning |
| `cohere-synthesis` | Cohere | knowledge-synthesis |

**Target**: 19 evaluators, 5 providers

### Phase 3: Specialists (Optional)

Add emerging providers with specific strengths.

| Evaluator | Provider | Specialty |
|-----------|----------|-----------|
| `deepseek-code` | DeepSeek | Code analysis |
| `llama-baseline` | Groq | Open source baseline |

**Target**: ~22-25 evaluators

## Principles

1. **Minimum Viable Diversity**: Each category has 2+ providers
2. **Pinned Versions**: Use specific model versions for reproducibility
3. **Cost Ladder**: Budget/Standard/Premium options per category
4. **Extensibility First**: Projects add their own evaluators

## Non-Goals

- Complete coverage of all models
- Automatic model updates (pinned versions preferred)
- Provider-specific optimizations
- Evaluator runtime/SDK (use `adversarial-workflow` CLI)

## Contributing

See [ADR-0002](docs/decisions/adr/ADR-0002-evaluator-expansion-strategy.md) for expansion principles.

To add an evaluator:
1. Follow naming convention: `{model-family}-{category}`
2. Use pinned model version
3. Include README.md and CHANGELOG.md
4. Add to `evaluators/index.json`
5. Run tests: `pytest tests/test_evaluators.py -v`
