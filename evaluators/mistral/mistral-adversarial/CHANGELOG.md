# Changelog — mistral-adversarial

## [1.0.0] - 2026-04-01

### Added
- Initial evaluator configuration
- 5-phase adversarial analysis protocol (Factual Verification, Logical Structure, Counterarguments, Risk Assessment, Strength Assessment)
- Prompt injection guard for untrusted content
- Severity-categorized findings (CRITICAL/HIGH/MEDIUM/LOW)
- Strengths preservation section to prevent over-criticism
- Three-level verdict: APPROVED, NEEDS_REVISION, REJECT
