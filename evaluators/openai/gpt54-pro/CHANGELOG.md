# Changelog — gpt54-pro

## 1.1.0 — 2026-04-28

### Deprecated
- `gpt54-pro` is deprecated in favor of `gpt55-pro` (GPT-5.5 Pro).
- The new evaluator preserves the prompt and output schema verbatim — only the underlying model changes (`gpt-5.4-pro` → `gpt-5.5-pro`).
- This evaluator continues to function and will be retired in a future release. Migrate consumers to `gpt55-pro`.

## 1.0.0 — 2026-04-17

### Added

- Initial release using GPT-5.4 Pro extended reasoning model
- Deep analysis protocol with 4 phases: structural understanding, logical chain verification, risk/scenario analysis, completeness/consistency
- Prompt injection guard for untrusted content
- Risk assessment matrix in output
