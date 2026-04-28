# Changelog - code-reviewer-fast

All notable changes to this evaluator will be documented in this file.

## [Deprecated] - 2026-04-28

- Marked `deprecated`; superseded by `code-reviewer-fast-v2` (running on `gemini-3-flash-preview`)
- Behavior unchanged; remains callable until retirement
- Per the evaluator versioning policy, retirement date will be announced ahead of removal

## [1.0.0] - 2026-02-27

### Added

- Initial release
- Condensed adversarial review protocol (edge cases, tracing, test gaps, interactions)
- Optimized for Gemini Flash speed and cost (~$0.003-0.01/run)
- PASS/CONCERNS/FAIL verdict system
- Finding categories: CORRECTNESS, ROBUSTNESS, TESTING

### Origin

- Fast variant of openai/code-reviewer
- Battle-tested on dispatch-kit as iteration evaluator
- Used for re-checking after fixes and pre-push sanity checks
