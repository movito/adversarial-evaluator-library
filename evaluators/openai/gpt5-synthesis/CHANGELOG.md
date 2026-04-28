# Changelog

All notable changes to the gpt5-synthesis evaluator will be documented in this file.

## [1.1.0] - 2026-04-28

### Deprecated
- `gpt5-synthesis` is deprecated in favor of `gpt55-synthesis` (GPT-5.5).
- The new evaluator preserves the prompt and output schema verbatim — only the underlying model changes (`gpt-5.4` → `gpt-5.5`).
- This evaluator continues to function and will be retired in a future release. Migrate consumers to `gpt55-synthesis`.

## [1.0.0] - 2026-02-02

### Added

- Initial release of GPT-5 Turbo knowledge synthesis evaluator
- Cross-referencing and completeness prompt adapted from gemini-pro
- Focus on consistency, coverage, and synthesis opportunities
- Standardized output format with severity labels (CRITICAL/HIGH/MEDIUM/LOW)
- Support for OPENAI_API_KEY environment variable
- 180-second timeout (standard category)

### Notes

- Part of AEL-0005: Phase 1 Evaluator Implementation
- Provides OpenAI coverage for knowledge-synthesis category (2nd provider)
