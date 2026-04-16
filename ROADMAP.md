# Roadmap

## Vision

A **starter kit** of adversarial evaluators that demonstrates cognitive diversity across AI providers. Projects clone this library and extend it with their own specialized evaluators.

**Not a goal**: Exhaustive coverage of every model and provider.

## Current State (v0.6.0)

**26 evaluators** across **4 providers** and **7 categories**:

| Provider | Evaluators | Models |
|----------|-----------|--------|
| OpenAI | 9 | gpt-5.2, o3, o4-mini, gpt-5, gpt-5-nano, gpt-5-turbo |
| Mistral | 7 | mistral-large-2512, mistral-small-2603, magistral-medium-2507, codestral |
| Google | 6 | gemini-2.5-flash, gemini-2.5-pro, gemini-3.1-pro-preview |
| Anthropic | 4 | claude-opus-4-7, claude-sonnet-4-6, claude-haiku-4-5 |

**Category coverage** (all categories have 2+ providers):

| Category | Providers | Count |
|----------|-----------|-------|
| code-review | OpenAI, Google, Mistral, Anthropic | 7 |
| arch-review | OpenAI, Google, Mistral, Anthropic | 4 |
| deep-reasoning | OpenAI, Google, Mistral | 4 |
| quick-check | OpenAI, Google, Mistral, Anthropic | 4 |
| adversarial | OpenAI, Mistral, Anthropic | 3 |
| knowledge-synthesis | OpenAI, Google | 2 |
| cognitive-diversity | OpenAI, Mistral | 2 |

## Completed Milestones

- **Phase 1** (v0.4.0–v0.5.0): Added Anthropic as Tier 1 provider (claude-adversarial, claude-code, claude-quick). All categories now have 2+ providers.
- **Phase 1.5** (v0.5.1–v0.5.3): Evaluator config fixes, prompt injection guardrails, model migrations (gemini-3-pro → gemini-3.1-pro-preview).
- **Mistral expansion** (v0.5.3+): Added mistral-arch, mistral-adversarial, mistral-deep using Mistral Large 3 (2512).
- **Model refresh** (v0.6.0): Comprehensive model update across all providers:
  - Upgraded Anthropic to Opus 4.7 + Sonnet 4.6, added claude-arch (arch-review)
  - Upgraded OpenAI reasoning from o1→o3, o1-mini→o4-mini, gpt-4o→gpt-5, gpt-4o-mini→gpt-5-nano
  - Retired duplicate o1-code-review evaluator
  - Upgraded Mistral from Large 2411→2512, Small 2503→2603 (Small 4)
  - Added magistral-reasoning using Mistral's dedicated reasoning model
  - Fixed GPT-5 Turbo LiteLLM routing (issue #20)

## Next

### Hardening & Quality

Stabilize the existing 26 evaluators before expanding further.

- Fix Mistral/aider whole-edit-format corruption (evaluator pipeline bug)
- Consider Unified Artifact Registry ([ADR-0007](docs/adr/ADR-0007-unified-artifact-registry.md)) for cross-project distribution

### Coverage Gaps (Optional)

Areas where a new evaluator would add meaningful diversity:

| Gap | Candidate | Why |
|-----|-----------|-----|
| Anthropic knowledge-synthesis | `claude-synthesis` | Category has only 2 providers |
| Anthropic cognitive-diversity | `claude-diversity` | Category has only 2 providers |
| Tier 2 provider | Cohere or DeepSeek | A 5th provider adds independent perspective |

### Longer Term

- Unified Artifact Registry (ADR-0007, implementation in agentive-starter-kit)
- Evaluator versioning and update notifications
- Cost tracking and budget-tier recommendations

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

See [ADR-0002](docs/adr/ADR-0002-evaluator-expansion-strategy.md) for expansion principles.

To add an evaluator:
1. Follow naming convention: `{model-family}-{category}`
2. Use pinned model version
3. Include README.md and CHANGELOG.md
4. Add to `evaluators/index.json`
5. Run tests: `pytest tests/test_evaluators.py -v`
