# Changelog

All notable changes to the gemini-flash evaluator.

## [Deprecated] - 2026-04-28

- Marked `deprecated`; superseded by `gemini-flash-v2` (running on `gemini-3-flash-preview`)
- Behavior unchanged; remains callable until retirement
- Per the evaluator versioning policy, retirement date will be announced ahead of removal

## [1.0.0] - 2025-01-31

### Added

- Initial release
- Fast document assessment prompt
- Validated timeout setting (180s)
- Tested on documents up to 15k tokens

### Validated

- GTX-0006: Response times 6-23 seconds on large documents
- Cost: $0.0038 per evaluation (11k token document)
