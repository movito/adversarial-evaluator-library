# AEL-0001: Write Project README

**Status**: Todo
**Priority**: medium
**Assigned To**: feature-developer
**Estimated Effort**: 2-3 hours
**Created**: 2026-01-31
**Target Completion**: 2026-02-01

## Related Tasks

**Depends On**: AEL-0002 (smoke tests should pass first)
**Related**: AEL-0003 (CI workflow)

## Overview

Write comprehensive documentation for the adversarial-evaluator-library. The README should explain the library's purpose, list available evaluators, and provide usage examples.

**Context**: This is a library of adversarial evaluators for AI-assisted document review. It includes 9 evaluators across 3 providers (Google, Mistral, OpenAI) organized into 6 categories.

## Requirements

### Functional Requirements
1. Clear project overview explaining adversarial evaluation concept
2. List all 9 evaluators with their purposes and categories
3. Installation instructions (pip install, API key setup)
4. Usage examples showing how to run evaluators
5. Configuration documentation (evaluator.yml structure)
6. Contributing guidelines for adding new evaluators

### Non-Functional Requirements
- [ ] README should be scannable (good headings, tables)
- [ ] Examples should be copy-paste ready
- [ ] Should work for both library users and contributors

## Implementation Plan

### Content Structure

```markdown
# adversarial-evaluator-library

[Badge section - build status, version, license]

## Overview
What this library does and why

## Quick Start
pip install, set API keys, run first evaluation

## Available Evaluators
Table of all 9 evaluators with:
- Name, Provider, Model, Category, Description

## Categories
- quick-check
- deep-reasoning
- adversarial
- knowledge-synthesis
- cognitive-diversity
- code-review

## Usage
### Running an Evaluator
### Evaluator Configuration
### Adding Custom Evaluators

## API Keys
Environment variables for each provider

## Development
### Running Tests
### Contributing

## License
```

### Files to Modify

1. `README.md` - Complete rewrite
   - Current: 4 lines
   - Target: ~150-200 lines

### Files to Reference

1. `evaluators/index.json` - Evaluator metadata
2. `evaluators/openai/fast-check/evaluator.yml` - Example config
3. `tests/test_evaluators.py` - Test commands

## Acceptance Criteria

### Must Have ✅
- [ ] Project purpose clearly explained
- [ ] All 9 evaluators listed with descriptions
- [ ] Installation instructions work
- [ ] At least one usage example
- [ ] API key setup documented

### Should Have 🎯
- [ ] Badges (CI status, version)
- [ ] Table of evaluators by category
- [ ] Contributing section

### Nice to Have 🌟
- [ ] Architecture diagram
- [ ] Comparison table of evaluators

## Success Metrics

### Quantitative
- README length: 150-200 lines
- All evaluators documented: 9/9
- Working code examples: ≥2

### Qualitative
- New users can run their first evaluation in <5 minutes
- Structure follows best practices for library READMEs

## Notes

- Keep "Built with Agentive Starter Kit" footer
- Use evaluators/index.json as source of truth for evaluator list
- Include both quick-start and detailed sections

---

**Template Version**: 1.0.0
