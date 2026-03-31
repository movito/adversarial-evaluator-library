# AEL-0013: Migrate to .kit/ Directory Layout - Implementation Handoff

**Date**: 2026-03-31
**From**: Coordinator
**To**: feature-developer-v5
**Task**: `.kit/tasks/2-todo/AEL-0013-kit-migration.md`
**Status**: Ready for implementation
**Evaluation**: Gemini Flash — no gaps found. GPT-4o evaluate — NEEDS_REVISION x3 (nitpicky, all concerns addressed in spec).

---

## Task Summary

Migrate adversarial-evaluator-library from the legacy directory layout (`delegation/`, `.kit/context/`, flat `scripts/`, `docs/decisions/`) to the `.kit/` builder layer structure. This also subsumes AEL-0012 (scripts restructure). Single atomic PR.

## Playbook

The authoritative migration guide is at:
`/Volumes/Macintosh HD/Users/broadcaster_three/Github/agentive-starter-kit/.kit/docs/KIT-MIGRATION-PLAYBOOK.md`

Read it before starting. The task spec (AEL-0013) has AEL-specific survey results and edge cases already documented.

## Execution Order

Follow these phases in order. Do NOT skip ahead.

### Phase A: Scripts Restructure

Source for canonical core scripts:
`/Volumes/Macintosh HD/Users/broadcaster_three/Github/agentive-starter-kit/scripts/core/`

1. `mkdir -p scripts/{core,local,optional}`
2. Copy all files from ASK `scripts/core/` → AEL `scripts/core/`
3. `git mv scripts/verify-v0.4.0.sh scripts/local/`
4. `git mv scripts/linear_sync_utils.py scripts/optional/`
5. `git mv scripts/sync_tasks_to_linear.py scripts/optional/`
6. Move remaining shared scripts (`validate_task_status.py`, `ci-check.sh`, `verify-ci.sh`, `verify-setup.sh`, `project`, `logging_config.py`) — these should be replaced by the ASK canonical versions in `scripts/core/`
7. Remove `scripts/README.md` and `scripts/__init__.py` if they exist at root level (the core/ versions replace them)
8. Copy `.core-manifest.json` from ASK `scripts/`

### Phase B: Create .kit/ Skeleton

```bash
mkdir -p .kit/{adr,context/{reviews,retros,templates,workflows},docs,launchers,skills,tasks/{1-backlog,2-todo,3-in-progress,4-in-review,5-done,6-canceled,7-blocked,8-archive,9-reference},templates}
```

### Phase C: Move Files

All moves use `git mv` to preserve history. Suppress errors for empty dirs with `2>/dev/null`.

**Tasks** (.kit/tasks/ → .kit/tasks/):
```bash
git mv .kit/tasks/1-backlog/* .kit/tasks/1-backlog/ 2>/dev/null
git mv .kit/tasks/2-todo/* .kit/tasks/2-todo/ 2>/dev/null
# ... repeat for all status folders
git mv .kit/tasks/README.md .kit/tasks/ 2>/dev/null
```

**Context** (.kit/context/ → .kit/context/):
```bash
# Structured subdirs first
git mv .kit/context/workflows/* .kit/context/workflows/ 2>/dev/null
git mv .kit/context/reviews/* .kit/context/reviews/ 2>/dev/null
git mv .kit/context/retros/* .kit/context/retros/ 2>/dev/null
git mv .kit/context/templates/* .kit/context/templates/ 2>/dev/null
# Then remaining files
git mv .kit/context/*.md .kit/context/ 2>/dev/null
git mv .kit/context/*.json .kit/context/ 2>/dev/null
```

**Launchers** (agents/ → .kit/launchers/):
```bash
git mv .kit/launchers/launch .kit/launchers/
git mv .kit/launchers/onboarding .kit/launchers/
git mv .kit/launchers/preflight .kit/launchers/
```

**Templates** (.claude/agents/ → .kit/templates/):
```bash
git mv .claude/agents/AGENT-TEMPLATE.md .kit/templates/
git mv .claude/agents/TASK-STARTER-TEMPLATE.md .kit/templates/
git mv .claude/agents/OPERATIONAL-RULES.md .kit/templates/
```

**ADRs**:
```bash
mkdir -p docs/adr
git mv docs/adr/* docs/adr/
git mv .kit/adr/* .kit/adr/
```

### Phase D: Clean Up

Remove empty directories: `delegation/`, `.kit/context/`, `agents/`, `docs/decisions/`. Only if completely empty — investigate anything remaining.

### Phase E: Path Rewrites

Run the bulk sed command from the playbook. Then manually fix:

1. `scripts/core/validate_task_status.py` line 106: `".kit/tasks/"` → `".kit/tasks/"`
2. `.pre-commit-config.yaml` line 63: `^.kit/tasks/.*\.md$` → `^\.kit/tasks/.*\.md$`
3. `.pre-commit-config.yaml` line 61: `entry: python scripts/validate_task_status.py` → `entry: python scripts/core/validate_task_status.py`
4. `CLAUDE.md`: update directory structure section

### Phase F: Verification

1. `pytest tests/ -v`
2. `pre-commit run --all-files`
3. `adversarial list-evaluators`
4. Grep verification for stale references

## Critical Gotchas

- **Do NOT move `.adversarial/`, `.dispatch/`, `.serena/`, `.claude/`** — hardcoded paths
- **Do NOT delete historical references** in retros, changelogs, done/archive task files
- **Do NOT split into multiple PRs** — atomic migration only
- **After sed, grep for bare names** (`delegation`, `agent-context`, `decisions`) not just full paths
- **`.claude/settings.local.json`** is gitignored but has permission path globs — update locally
- **AEL-0012**: Move to `6-canceled/` with a note that it was superseded by AEL-0013
- **The `.kit/context/reviews/` directory** has PR review files — check for the untracked `PR-4-review*.md` files in git status

## Resources

- Migration playbook: `/Volumes/Macintosh HD/Users/broadcaster_three/Github/agentive-starter-kit/.kit/docs/KIT-MIGRATION-PLAYBOOK.md`
- ASK scripts/core/ (source of truth): `/Volumes/Macintosh HD/Users/broadcaster_three/Github/agentive-starter-kit/scripts/core/`
- Task spec: `.kit/tasks/2-todo/AEL-0013-kit-migration.md`
- AEL-0012 (superseded): `.kit/tasks/2-todo/AEL-0012-scripts-core-restructure.md`

---

**Task File**: `.kit/tasks/2-todo/AEL-0013-kit-migration.md`
**Handoff Date**: 2026-03-31
