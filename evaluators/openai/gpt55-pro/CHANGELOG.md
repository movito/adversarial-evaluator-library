# Changelog — gpt55-pro

## 1.0.0 — 2026-04-28

### Added

- Initial release using GPT-5.5 Pro extended reasoning model
- Replaces `gpt54-pro` (GPT-5.4 Pro), which is now deprecated
- Prompt and output schema copied verbatim from `gpt54-pro` v1.0.0 to preserve consumer contract
- Underlying model upgrade: `gpt-5.4-pro` → `gpt-5.5-pro` (1,050K context, ~60% fewer hallucinations vs GPT-5.4)
