# Changelog

All notable changes to the gpt5-diversity evaluator will be documented in this file.

## [1.1.0] - 2026-04-28

### Deprecated
- `gpt5-diversity` is deprecated in favor of `gpt55-diversity` (GPT-5.5).
- The new evaluator preserves the prompt and output schema verbatim — only the underlying model changes (`gpt-5.4` → `gpt-5.5`).
- This evaluator continues to function and will be retired in a future release. Migrate consumers to `gpt55-diversity`.

## [1.0.0] - 2026-02-02

### Added

- Initial release of GPT-5 Turbo cognitive diversity evaluator
- Alternative perspective prompt adapted from mistral-content
- Focus on assumption auditing and blind spot detection
- Standardized output format with severity labels (CRITICAL/HIGH/MEDIUM/LOW)
- Support for OPENAI_API_KEY environment variable
- 180-second timeout (standard category)

### Notes

- Part of AEL-0005: Phase 1 Evaluator Implementation
- Provides OpenAI coverage for cognitive-diversity category (2nd provider)
