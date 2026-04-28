# Changelog

## [1.0.0] - 2026-04-28

### Added

- Initial release
- Replaces `gemini-deep` (`gemini-2.5-pro`) with `gemini-3.1-pro-preview`
- Aligns the deep-reasoning Pro evaluator with sibling evaluators `gemini-pro` and `gemini-code`, all of which now run on Gemini 3.1 Pro
- Prompt and output schema preserved verbatim from `gemini-deep` 1.0.0
- Timeout: 600s (unchanged)

### Notes

- Underlying model `gemini-3.1-pro-preview` is in preview at Google
- When Google promotes 3.1 Pro to a stable model ID, a v3 evaluator will be released and this one deprecated
- Per the evaluator versioning policy, the predecessor `gemini-deep` is now `deprecated` but remains callable until retirement
