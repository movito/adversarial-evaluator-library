# Changelog

All notable changes to the Adversarial Evaluator Library will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **`code-reviewer` evaluator** (OpenAI o1) — Adversarial correctness review that finds edge-case bugs, boundary conditions, and logic errors that checklist reviews miss. 4-phase protocol: attack surface identification, execution path tracing, test cross-referencing, interaction analysis. Battle-tested on 7+ PRs in dispatch-kit.
- **`code-reviewer-fast` evaluator** (Google Gemini Flash) — Fast variant of code-reviewer for small changes and iteration cycles. Same adversarial mindset, condensed protocol. ~$0.003-0.01/run.

## [0.4.0] - 2026-02-08

### Added

- **Cross-provider evaluation support** - Anthropic evaluators now work seamlessly with litellm for multi-provider workflows
- **ADR-0006 Cross-Provider Usage** - Decision record documenting Anthropic cross-provider support
- **Cross-provider evaluation guide** - New `docs/guides/CROSS-PROVIDER-EVALUATION.md` with setup instructions and best practices
- **Claude 4.5/4.6 models in registry** - Added `claude-opus-4-6`, `claude-sonnet-4-5`, `claude-haiku-4-5` to provider registry
- **Workflow v0.9.2 integration verified** - Full end-to-end testing with OpenAI, Google, and Mistral evaluators

### Changed

- **Anthropic evaluators updated to current models** - claude-adversarial (Opus 4.6), claude-code (Sonnet 4.5), claude-quick (Haiku 4.5)
- **litellm-compatible model IDs** - All Anthropic evaluators now use `anthropic/` prefix, Google uses `gemini/` prefix
- **Upgraded adversarial-workflow to v0.9.3** - Now requires `>=0.9.3` with ADV-0032 fix ensuring explicit `model` field takes priority over `model_requirement` resolution
- **Registry schema version 1.0.1** - Bumped for new Claude model additions per ADR-0005

### Fixed

- **Model field priority** (ADV-0032) - Workflow v0.9.3 ensures explicit `model` field in evaluator YAML takes priority over `model_requirement` resolution
- **ADR-0005 resolution algorithm** - Clarified that explicit model takes precedence over model_requirement

## [0.3.0] - 2026-02-03

### Added

- **model_requirement field for Phase 2 resolution** (AEL-0006) - All 18 evaluators now include `model_requirement` block with `family`, `tier`, and `min_version` fields. Enables adversarial-workflow resolution engine while maintaining backwards compatibility with legacy `model` and `api_key_env` fields. See ADR-0005 for interface contract.
- **Provider registry** - Added `providers/registry.yml` with 7 model families (gpt, o, claude, gemini, mistral, codestral, llama) and capability tiers.
- **ADR-0005 Interface Contract** - Formalized library-workflow interface with schema specification, resolution algorithm, and version compatibility.

### Changed

- **18 evaluators across 4 providers** - OpenAI (8), Anthropic (3), Google (4), Mistral (3)

## [0.2.0] - 2026-02-02

### Added

- **Phase 1 evaluator implementation** (AEL-0005) - Added 6 new evaluators bringing total to 18
- **Evaluator categories** - quick-check, deep-reasoning, adversarial, knowledge-synthesis, cognitive-diversity, code-review

## [0.1.0] - 2026-01-31

### Added

- Initial release of adversarial-evaluator-library
- 12 evaluators across 4 providers
- CI/CD workflow with pytest and pre-commit
- Project structure based on Agentive Starter Kit

[Unreleased]: https://github.com/movito/adversarial-evaluator-library/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/movito/adversarial-evaluator-library/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/movito/adversarial-evaluator-library/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/movito/adversarial-evaluator-library/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/movito/adversarial-evaluator-library/releases/tag/v0.1.0
