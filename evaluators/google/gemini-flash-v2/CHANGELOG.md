# Changelog

All notable changes to the gemini-flash-v2 evaluator.

## [1.0.0] - 2026-04-28

### Added

- Initial release
- Replaces `gemini-flash` (Gemini 2.5 Flash) with `gemini-3-flash-preview`
- Prompt and output schema preserved verbatim from `gemini-flash` 1.0.0
- Timeout: 180s (unchanged)

### Notes

- Underlying model `gemini-3-flash-preview` is in preview at Google
- When Google promotes Flash 3 to a stable model ID, a v3 evaluator will be released and this one deprecated
- Per the evaluator versioning policy, the predecessor `gemini-flash` is now `deprecated` but remains callable until retirement
