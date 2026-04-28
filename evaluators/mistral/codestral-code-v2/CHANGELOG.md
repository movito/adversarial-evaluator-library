# Changelog

## [1.0.0] - 2026-04-28

### Added

- Initial release
- Replaces `codestral-code` (`mistral/codestral-latest`) with the explicit `mistral/codestral-2` model
- Prompt and output schema preserved verbatim from `codestral-code` 1.0.0
- Context window grows from ~32K (codestral-latest) to 128K
- Timeout: 300s (unchanged)

### Notes

- Per the evaluator versioning policy, the predecessor `codestral-code` is now `deprecated` but remains callable until retirement
