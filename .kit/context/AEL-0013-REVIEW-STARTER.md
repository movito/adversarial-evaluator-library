# Review Starter: AEL-0013 — Migrate to .kit/ Directory Layout

**PR**: #14
**Branch**: `feature/AEL-0013-kit-migration`
**Task**: `.kit/tasks/3-in-progress/AEL-0013-kit-migration.md`
**Evaluator Review**: `.kit/context/reviews/AEL-0013-evaluator-review.md`

## Summary

Migrated adversarial-evaluator-library from legacy directory layout (`delegation/`, `.agent-context/`, flat `scripts/`) to the `.kit/` directory structure (Agentive Starter Kit standard). Single atomic PR with 227 files changed.

## What Changed

1. **Scripts restructured**: `scripts/` → `scripts/core/` (canonical), `scripts/optional/`, `scripts/local/`
2. **Context migrated**: `.agent-context/` → `.kit/context/` (workflows, reviews, handoffs)
3. **Tasks migrated**: `delegation/tasks/` → `.kit/tasks/` (numbered folders)
4. **ADRs migrated**: `docs/starter-kit-adr/` → `.kit/adr/`
5. **Launchers migrated**: `agents/` → `.kit/launchers/` (with PROJECT_ROOT depth fix)
6. **Templates created**: `.kit/templates/` (agent, task starter, operational rules)
7. **All path references updated**: Python imports, mock targets, CI workflows, agent files, commands

## Review Focus Areas

- [ ] **Python imports**: `scripts.core.X` and `scripts.optional.X` correct everywhere
- [ ] **Launcher scripts**: PROJECT_ROOT uses double dirname for `.kit/launchers/` depth
- [ ] **CI workflow**: `sync-to-linear.yml` triggers and script paths correct
- [ ] **Coverage config**: `pyproject.toml` omit list matches new paths
- [ ] **No stale references**: No remaining `delegation/`, `.agent-context/`, or `scripts/project` references

## Test Evidence

- 200 tests passing, 27 skipped
- 93% coverage (threshold: 80%)
- CI green on GitHub Actions
- CodeRabbit: APPROVED
- BugBot: All findings addressed (83 threads total, 83 resolved)

## Bot Review Summary

- **Total threads**: 83
- **Fixed**: 13 (real migration bugs — stale paths, launcher depth, mock targets)
- **Resolved without fix**: 70 (pre-existing issues, cosmetic, false positives)
