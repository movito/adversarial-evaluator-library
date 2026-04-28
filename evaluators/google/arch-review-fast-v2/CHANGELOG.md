# arch-review-fast-v2 Changelog

## 1.0.0 (2026-04-28)

### Added

- Initial release
- Replaces `arch-review-fast` (Gemini 2.5 Flash) with `gemini-3-flash-preview`
- Prompt and output schema preserved verbatim from `arch-review-fast` 1.0.0
- Timeout: 180s (unchanged)

### Notes

- Underlying model `gemini-3-flash-preview` is in preview at Google
- When Google promotes Flash 3 to a stable model ID, a v3 evaluator will be released and this one deprecated
- Per the evaluator versioning policy, the predecessor `arch-review-fast` is now `deprecated` but remains callable until retirement
