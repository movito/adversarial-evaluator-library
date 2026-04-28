# Changelog

## [1.1.0] - 2026-04-28

### Deprecated
- `gpt52-reasoning` is deprecated in favor of `gpt55-adversarial` (GPT-5.5).
- The new evaluator preserves the prompt and verdict vocabulary verbatim.
- The new name better reflects the actual model and the `adversarial` category — the legacy `gpt52-reasoning` name had been running on `gpt-5.4` since v0.7.0 (a violation of the evaluator-versioning policy now adopted in `.claude/skills/evaluator-versioning/SKILL.md`).
- This evaluator continues to function and will be retired in a future release. Migrate consumers to `gpt55-adversarial`.

## [1.0.0] - 2025-01-31

### Added
- Initial release
- Adversarial review prompt
- Validated timeout (180s, typical 30-45s)
- Tested on policy and technical documents

### Validated
- GTX-0005: Response times consistently under 45 seconds
- Output quality verified for adversarial use cases
