# Code Review: AEL-0013 — Migrate to .kit/ Directory Layout

## PR Summary
PR #14: Migrate adversarial-evaluator-library from legacy `delegation/` + `.agent-context/` + flat `scripts/` layout to the `.kit/` directory structure (Agentive Starter Kit standard).

**Stats**: 227 files changed, 6351 insertions, 1872 deletions

## Changes Overview

### 1. Scripts Restructure (`scripts/`)
- `scripts/project` (674 lines) → deleted, replaced by `scripts/core/project` (1350 lines, ASK canonical)
- `scripts/ci-check.sh` → `scripts/core/ci-check.sh` (ASK canonical)
- `scripts/verify-ci.sh` → `scripts/core/verify-ci.sh` (ASK canonical)
- `scripts/verify-setup.sh` → `scripts/core/verify-setup.sh` (ASK canonical)
- `scripts/validate_task_status.py` → `scripts/core/validate_task_status.py`
- `scripts/logging_config.py` → `scripts/core/logging_config.py`
- `scripts/linear_sync_utils.py` → `scripts/optional/linear_sync_utils.py`
- `scripts/sync_tasks_to_linear.py` → `scripts/optional/sync_tasks_to_linear.py`
- `scripts/verify-v0.4.0.sh` → `scripts/local/verify-v0.4.0.sh`
- New ASK canonical scripts: `check-bots.sh`, `gh-review-helper.sh`, `wait-for-bots.sh`, `preflight-check.sh`, `pattern_lint.py`, `check-sync.sh`
- Added `__init__.py` to `scripts/core/`, `scripts/optional/`, `scripts/local/` for Python imports

### 2. .kit/ Skeleton
- `.agent-context/` → `.kit/context/` (context files, workflows, reviews, handoffs)
- `docs/starter-kit-adr/` → `.kit/adr/` (20 ADR files)
- `delegation/tasks/` → `.kit/tasks/` (task specs in numbered folders)
- `agents/` → `.kit/launchers/` (onboarding, launch, preflight scripts)
- New: `.kit/templates/` (AGENT-TEMPLATE.md, TASK-STARTER-TEMPLATE.md, OPERATIONAL-RULES.md)

### 3. Agent & Command Updates
- All `.claude/agents/*.md` files updated: `./scripts/project` → `./scripts/core/project`, etc.
- Deleted `.claude/agents/feature-developer-v3.md` (superseded by v5)
- New agents: `feature-developer-v5.md`, `planner2.md`
- New commands: `babysit-pr.md`, `check-bots.md`, `check-spec.md`, `commit-push-pr.md`, `preflight.md`, `retro.md`, `start-task.md`, `status.md`, `triage-threads.md`, `wait-for-bots.md`, `wrap-up.md`

### 4. Path Reference Updates
- All Python imports updated (`from scripts.X` → `from scripts.core.X` or `scripts.optional.X`)
- All `patch()` mock targets in tests updated
- `.pre-commit-config.yaml` updated
- `pyproject.toml` coverage config updated
- `.github/workflows/sync-to-linear.yml` updated
- `.github/workflows/test.yml` updated
- Launcher scripts: `PROJECT_ROOT` fixed for new depth, `.agent-context` → `.kit/context`

### 5. Key Risk Areas
- **Python imports**: Scripts moved to subdirectories; imports and `patch()` targets all updated
- **Launcher depth**: `.kit/launchers/` is 2 levels deep vs old `agents/` (1 level); `PROJECT_ROOT` calculation updated
- **Coverage config**: `pyproject.toml` omit list updated for new paths; coverage at 93%
- **CI workflow**: sync-to-linear.yml path triggers and script invocation updated

## Test Results
- 200 tests passing, 27 skipped
- 93% coverage (threshold: 80%)
- CI green on GitHub Actions

## Files to Review (Priority)
1. `scripts/core/project` — New ASK canonical script (1350 lines)
2. `tests/test_linear_sync.py` — Import and patch() target updates
3. `.github/workflows/sync-to-linear.yml` — CI workflow path changes
4. `.kit/launchers/onboarding` — PROJECT_ROOT and state file path fixes
5. `.kit/launchers/launch` — PROJECT_ROOT and CONTEXT_DIR fixes
