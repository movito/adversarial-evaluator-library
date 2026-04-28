# Changelog — gpt55-synthesis

## 1.0.0 — 2026-04-28

### Added

- Initial release using GPT-5.5 for knowledge synthesis review
- Replaces `gpt5-synthesis` (GPT-5.4), which is now deprecated
- Prompt and output schema copied verbatim from `gpt5-synthesis` v1.0.0 to preserve consumer contract
- Underlying model upgrade: `gpt-5.4` → `gpt-5.5` (1,050K context, ~60% fewer hallucinations)
