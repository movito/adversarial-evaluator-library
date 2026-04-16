# Changelog

All notable changes to the Adversarial Evaluator Library will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.7.0] - 2026-04-17

### Added

- **`gpt54-pro` evaluator** (OpenAI GPT-5.4 Pro) — Extended reasoning for complex multi-step analysis, risk assessment, and decision framework evaluation. Complements o3-chain with GPT-family extended reasoning.
- **`gpt5-codex` evaluator** (OpenAI GPT-5.3 Codex) — Code-specialized review using OpenAI's purpose-built code model. Deep code comprehension, algorithm correctness, and complexity analysis.
- **GPT-5.4 family** in provider registry — gpt-5.4, gpt-5.4-pro, gpt-5.4-mini, gpt-5.4-nano, gpt-5.3-codex

### Changed

- **5 evaluators upgraded to GPT-5.4**: `fast-check` (nano→5.4-nano), `gpt4o-code` (5→5.4), `gpt5-diversity` (5→5.4), `gpt5-synthesis` (5→5.4), `gpt52-reasoning` (5.2→5.4)
- **Provider registry v1.0.4** — Added GPT-5.4 family, marked gpt-5/5.2/5-nano/5-mini as legacy
- **25 evaluators across 4 providers** — Anthropic (4), Google (6), OpenAI (11), Mistral (4)

## [0.6.1] - 2026-04-17

### Fixed

- **`magistral-reasoning` invalid model ID** — `magistral-medium-2507` was retired Nov 2025; updated to `magistral-medium-2509` (Magistral Medium 1.2)
- **`gpt5-diversity` invalid model ID** — `gpt-5-turbo-2025-11-01` never existed in OpenAI's API; updated to `gpt-5`
- **`gpt5-synthesis` invalid model ID** — Same fix as gpt5-diversity
- **Provider registry phantom entry** — Removed non-existent `gpt-5-turbo-2025-11-01` from registry

### Changed

- **Provider registry v1.0.3** — Added `magistral-medium-2509`, marked `magistral-medium-2507` as deprecated
- **Bumped `adversarial-workflow` dependency** to `>=1.0.0`

## [0.6.0] - 2026-04-16

### Added

- **`claude-arch` evaluator** (Anthropic Opus 4.7) — Architectural review from Anthropic's perspective, filling the cross-provider arch-review gap. Includes prompt-injection guard.
- **`magistral-reasoning` evaluator** (Mistral Magistral Medium) — Deep reasoning using Mistral's dedicated reasoning model for multi-step logical analysis and assumption stress-testing. Includes prompt-injection guard.
- **Magistral model family** in provider registry — `magistral-medium-2507` and `magistral-small-2507`
- **Mistral Small 4** (`mistral-small-2603`) in provider registry — 6.5B active / 119B total MoE params

### Changed

- **Model upgrades across all 4 providers**:
  - Anthropic: `claude-adversarial` Opus 4.6 → 4.7, `claude-code` Sonnet 4.5 → 4.6
  - OpenAI: `arch-review` and `code-reviewer` o1 → o3, `o1-mini-code` o1-mini → o4-mini, `gpt4o-code` gpt-4o → gpt-5, `fast-check` gpt-4o-mini → gpt-5-nano
  - Mistral: `mistral-content` Large 2411 → 2512, `mistral-fast` Small 2503 → 2603 (Small 4)
- **Provider registry v1.0.2** — Added Claude Opus 4.7, Claude Sonnet 4.6, o4-mini, gpt-5, gpt-5-mini, gpt-5-nano, Mistral Small 4, Magistral family. Marked legacy: gpt-4o, gpt-4o-mini, o1-mini, Claude Opus 4.6, Claude Sonnet 4.5, Mistral Large 2411, Mistral Small 2503.
- **23 evaluators across 4 providers** — Anthropic (4), Google (6), OpenAI (9), Mistral (4)
- **Integration tests updated** — Aligned with new model versions and registry schema

### Removed

- **`o1-code-review` evaluator** — Retired as duplicate of `code-reviewer` (both used o1, now o3)

### Fixed

- **GPT-5 Turbo LiteLLM routing** (issue #20) — Added explicit `openai/` prefix for `gpt-5-turbo-2025-11-01` model IDs in `gpt5-diversity` and `gpt5-synthesis`
- **`fast-check` tier mismatch** — Changed `tier: nano` → `tier: mini` (nano tier doesn't exist in registry)
- **`gpt4o-code` tier mismatch** — Changed `tier: standard` → `tier: flagship` (gpt-5 is in flagship tier)
- **Missing `flake8` dev dependency** — Added `flake8>=7.3.0` to pyproject.toml, fixing CI workflow

## [0.5.3] - 2026-03-08

### Fixed

- **gemini-code untrusted-content guard** — Added prompt injection guardrail matching claude-adversarial pattern
- **gemini-flash/gemini-pro README** — Replaced invalid `gpt52-reasoning` references with canonical evaluator names
- **code-reviewer-fast docstring** — Removed hardcoded `openai/code-reviewer` path reference
- **mistral-fast README** — Corrected evaluator name `mistral-large` → `mistral-content`

## [0.5.2] - 2026-03-08

### Fixed

- **URGENT: gemini-3-pro deprecation** — Migrated `gemini-pro` and `gemini-code` from deprecated `gemini-3-pro` to `gemini-3.1-pro-preview` before March 9 shutdown deadline
- **claude-adversarial prompt injection** — Added untrusted-input guardrail to prevent reviewed content from hijacking evaluator behavior
- **claude-adversarial APPROVED verdict** — Changed from subjective "arguments are sound, evidence is strong" to objective "no critical or high issues found"
- **code-reviewer-fast non-code gap** — Added fallback for config, YAML, and markdown inputs; added `INTERACTION` finding label
- **arch-review-fast header** — Corrected "Gemini Deep Think" → "Gemini Flash" in evaluator.yml
- **arch-review-fast README** — Replaced project-specific example paths with generic `your_project`
- **Markdown formatting** — Fixed heading blank lines and code block language tags across multiple READMEs and CHANGELOGs

### Changed

- **Provider registry** — Added `gemini-3.1-pro-preview` to pro tier; marked `gemini-3-pro` as deprecated
- **index.json** — Updated model IDs and descriptions for gemini-pro and gemini-code
- **README.md evaluator table** — Corrected model names for gemini-pro and gemini-code

## [0.5.1] - 2026-03-07

### Fixed

- **gemini-deep model mismatch** — Was using `gemini-2.5-flash` (identical to gemini-flash); upgraded to `gemini-2.5-pro` with correct pro tier
- **mistral-fast retired model** — Updated from retired `mistral-small-2409` to `mistral-small-2503` (128k context)
- **claude-code speculative findings** — Added `## Context Required / Unverifiable` section to separate missing-context notes from severity-graded findings
- **claude-quick clean check as LOW finding** — Changed to neutral `### Clean Check` format with `Result`/`Next step` fields
- **mistral-content output schema** — Added structured findings format, no-findings branch, and required `**Verdict**:` output field
- **code-reviewer-fast Python-centric prompt** — Made language-agnostic (`file.py` → `file`, "function" → "function or method")
- **gemini-code README** — Added missing `gemini/` prefix in config example
- **claude-quick docs** — Fixed "Claude 4 Haiku" → "Claude Haiku 4.5" in README and CHANGELOG
- **mistral-content regional claims** — Replaced unsupported "European training data emphasis" with vendor-neutral wording
- **gemini-deep README cost estimate** — Replaced unsubstantiated fixed cost with reference to Google pricing
- **Markdown formatting** — Fixed MD022 (blank line after heading) in 4 CHANGELOGs, MD040 (fenced code language tag) in claude-quick README

### Changed

- **Provider registry** — Added `gemini-2.5-pro` to pro tier, `mistral-small-2503` to small tier; marked `mistral-small-2409` as deprecated
- **index.json** — Updated model references for gemini-deep, mistral-fast, and mistral-content description
- **README.md evaluator table** — Corrected model names for claude-quick, claude-code, claude-adversarial, gemini-deep, mistral-fast, and mistral-content

## [0.5.0] - 2026-02-27

### Added

- **`code-reviewer` evaluator** (OpenAI o1) — Adversarial correctness review that finds edge-case bugs, boundary conditions, and logic errors that checklist reviews miss. 4-phase protocol: attack surface identification, execution path tracing, test cross-referencing, interaction analysis. Battle-tested on 7+ PRs in dispatch-kit.
- **`code-reviewer-fast` evaluator** (Google Gemini Flash) — Fast variant of code-reviewer for small changes and iteration cycles. Same adversarial mindset, condensed protocol. ~$0.003-0.01/run.
- **`arch-review` evaluator** (OpenAI o1) — Deep architectural review using o1 reasoning for structural and design analysis.
- **`arch-review-fast` evaluator** (Google Gemini Flash) — Fast architectural review using extended reasoning.
- **arch-review category** — New evaluator category for structural and architectural code analysis.

### Changed

- **22 evaluators across 4 providers** — OpenAI (10), Google (6), Anthropic (3), Mistral (3)
- **7 categories** — Added arch-review category
- **Registry schema version 1.5.0** — Updated for new evaluator additions

### Fixed

- **README accuracy** — Version badge, category count (6→7), missing arch-review entries in table and directory tree

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

[Unreleased]: https://github.com/movito/adversarial-evaluator-library/compare/v0.7.0...HEAD
[0.7.0]: https://github.com/movito/adversarial-evaluator-library/compare/v0.6.1...v0.7.0
[0.6.1]: https://github.com/movito/adversarial-evaluator-library/compare/v0.6.0...v0.6.1
[0.6.0]: https://github.com/movito/adversarial-evaluator-library/compare/v0.5.3...v0.6.0
[0.5.3]: https://github.com/movito/adversarial-evaluator-library/compare/v0.5.2...v0.5.3
[0.5.2]: https://github.com/movito/adversarial-evaluator-library/compare/v0.5.1...v0.5.2
[0.5.1]: https://github.com/movito/adversarial-evaluator-library/compare/v0.5.0...v0.5.1
[0.5.0]: https://github.com/movito/adversarial-evaluator-library/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/movito/adversarial-evaluator-library/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/movito/adversarial-evaluator-library/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/movito/adversarial-evaluator-library/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/movito/adversarial-evaluator-library/releases/tag/v0.1.0
