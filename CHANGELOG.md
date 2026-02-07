# Changelog

All notable changes to the Adversarial Evaluator Library will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Workflow v0.9.2 integration verified** - Full end-to-end testing with OpenAI, Google, and Mistral evaluators. All providers return exit code 0 on successful evaluation.
- **Testing procedure documentation** - Added `docs/verification/TESTING-PROCEDURE.md` with step-by-step guide for verifying evaluator functionality.
- **Verification reports** - Added `docs/verification/` directory with workflow integration reports and feedback.
- **Knowledge system updates** - Updated `current-state.json` with `workflow_integration` and `quick_reference` sections for future planners.

### Changed

- **Upgraded adversarial-workflow to v0.9.3** - Now requires `>=0.9.3` with ADV-0032 fix ensuring explicit `model` field takes priority over `model_requirement` resolution. This enables library evaluators with updated model IDs (e.g., `anthropic/claude-opus-4-6`) to work correctly.

### Fixed

- **Exit code now 0 for successful evaluations** - Workflow v0.9.2 fixes the exit code 1 issue reported in our feedback.
- **Model field priority** (ADV-0032) - Workflow v0.9.3 ensures explicit `model` field in evaluator YAML takes priority over `model_requirement` resolution. Previously, `model_requirement` was incorrectly taking precedence even when an explicit model was specified.

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

[Unreleased]: https://github.com/movito/adversarial-evaluator-library/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/movito/adversarial-evaluator-library/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/movito/adversarial-evaluator-library/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/movito/adversarial-evaluator-library/releases/tag/v0.1.0
