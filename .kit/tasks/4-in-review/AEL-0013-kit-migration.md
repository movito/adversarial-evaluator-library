# AEL-0013: Migrate to .kit/ Directory Layout

**Status**: In Review
**Priority**: Medium
**Type**: Infrastructure
**Estimated Effort**: 2-3 hours
**Created**: 2026-03-31
**Subsumes**: AEL-0012 (scripts/core/ restructure)
**Parent**: KIT-MIGRATION-PLAYBOOK v1.0.0

## Summary

Migrate adversarial-evaluator-library from the legacy `delegation/` + `.kit/context/` + flat `scripts/` layout to the `.kit/` directory structure defined in agentive-starter-kit v0.5.0+. This combines the scripts restructure (AEL-0012) with the full kit migration into a single atomic PR.

## Context

The agentive-starter-kit has adopted a `.kit/` builder layer that cleanly separates builder infrastructure from project code. All downstream repos need to migrate. AEL has a moderate reference count (~85 delegation/, ~83 .kit/context/, ~50 docs/decisions/) making this a medium-sized migration.

**Reference**: `/Volumes/Macintosh HD/Users/broadcaster_three/Github/agentive-starter-kit/.kit/docs/KIT-MIGRATION-PLAYBOOK.md`

## Pre-Flight Survey (Completed)

| Check | Result |
|-------|--------|
| `delegation/` | Tasks (1-backlog through 9-reference) + empty handoffs/ |
| `.kit/context/` | 20+ files: handoffs, reviews, workflows, templates, state JSON |
| `agents/` at root | Launchers: launch, onboarding, preflight |
| `.claude/agents/` templates | AGENT-TEMPLATE.md, TASK-STARTER-TEMPLATE.md, OPERATIONAL-RULES.md |
| `scripts/` | Flat (11 files, NOT restructured) |
| `docs/decisions/` | adr/ (7 project ADRs) + starter-kit-adr/ (20 kit ADRs) |
| `.dispatch/` | Does NOT exist — skip dispatch config |
| `delegation/` ref count | ~85 files |
| `.kit/context/` ref count | ~83 files |
| `docs/decisions/` ref count | ~50 files |

## Scope

### Phase A: Scripts Restructure (from AEL-0012)

1. Create `scripts/core/`, `scripts/local/`, `scripts/optional/`
2. Copy 12 canonical core scripts from agentive-starter-kit `scripts/core/`
3. Move `verify-v0.4.0.sh` → `scripts/local/`
4. Move Linear sync scripts → `scripts/optional/` (not actively used)
5. Remove old flat scripts from `scripts/` root
6. Create `.core-manifest.json`

### Phase B: Create .kit/ Skeleton

```bash
mkdir -p .kit/{adr,context/{reviews,retros,templates,workflows},docs,launchers,skills,tasks/{1-backlog,2-todo,3-in-progress,4-in-review,5-done,6-canceled,7-blocked,8-archive,9-reference},templates}
```

### Phase C: Move Files (git mv for history)

1. **Tasks**: `.kit/tasks/*` → `.kit/tasks/*`
2. **Context**: `.kit/context/` contents → `.kit/context/` (structured subdirs first, then remaining)
3. **Launchers**: `agents/{launch,onboarding,preflight}` → `.kit/launchers/`
4. **Templates**: `.claude/agents/{AGENT-TEMPLATE,TASK-STARTER-TEMPLATE,OPERATIONAL-RULES}.md` → `.kit/templates/`
5. **Kit ADRs**: `.kit/adr/*` → `.kit/adr/`
6. **Project ADRs**: `docs/adr/*` → `docs/adr/`

### Phase D: Clean Up Empty Directories

Remove `delegation/`, `.kit/context/`, `agents/`, `docs/decisions/` (only if empty after moves).

### Phase E: Rewrite Path References

Bulk sed for the ~218 file references, then manual verification for:
- Python code (`validate_task_status.py` — hardcoded `TASK_DIR`)
- `.pre-commit-config.yaml` hook paths
- `.claude/commands/` slash commands
- `.claude/agents/` agent definitions
- `.coderabbitignore` / `.gitignore`
- `CLAUDE.md` directory structure section
- `.claude/settings.local.json` permission patterns (gitignored, update locally)

### Phase F: Post-Migration Verification

1. `pytest tests/ -v` — all tests pass
2. `pre-commit run --all-files` — hooks pass with new paths
3. `adversarial list-evaluators` — evaluator CLI still works
4. Zero stale references (grep verification, excluding historical/archive content)

## Acceptance Criteria

- [x] `.kit/` directory structure matches target layout from playbook
- [x] `scripts/core/` contains canonical scripts from ASK
- [x] `scripts/local/` contains AEL-specific scripts
- [x] All task files preserved with git history (`git mv`)
- [x] All .agent-context files moved to `.kit/context/` with correct subdirectory structure
- [x] Launchers moved to `.kit/launchers/`
- [x] Templates moved to `.kit/templates/`
- [x] ADRs split: project → `docs/adr/`, kit → `.kit/adr/`
- [x] `validate_task_status.py` updated to use `.kit/tasks`
- [x] Zero stale `delegation/`, `.kit/context/`, `docs/decisions/` references in active files
- [x] All tests pass (189 passed, 38 skipped)
- [x] Pre-commit hooks pass
- [ ] Single atomic PR (no half-migrated state)
- [x] N/A — `CLAUDE.md` does not exist in this repo (no update needed)
- [x] AEL-0012 marked as superseded/canceled

## Error Handling & Rollback

**Rollback strategy**: This migration uses `git mv` throughout, so the entire branch can be abandoned and the PR closed with zero impact on `main`. No database migrations, no external service changes, no published artifacts — purely local file moves and text edits.

**Edge cases in path rewrites**:
- `sed` handles ~95% of references. After sed, grep for bare names (`delegation`, `agent-context`, `decisions`) to catch array literals, exclude lists, and partial references
- Python code in `scripts/validate_task_status.py` line 106: change `".kit/tasks/"` → `".kit/tasks/"` in the path check
- `.pre-commit-config.yaml` line 63: change `files: ^.kit/tasks/.*\.md$` → `files: ^\.kit/tasks/.*\.md$`
- `.pre-commit-config.yaml` line 61: update `entry: python scripts/validate_task_status.py` → `entry: python scripts/core/validate_task_status.py` (after scripts restructure)
- JSON files (`.claude/settings.local.json`) need careful path glob updates — this file is gitignored but exists locally
- Historical references in retros, changelogs, and completed task files are left as-is (they describe what was true at the time)

**Known test state**: All tests currently pass on `main`. No known failures. The migration does not change any Python source code except `validate_task_status.py` (one path string), so test breakage risk is minimal.

**Merge conflict strategy**: This migration lands as a single atomic PR on a feature branch. If other branches have concurrent work touching `delegation/` paths, they will need to rebase after this PR merges. Since AEL has low concurrent activity, this risk is minimal.

## Impact Assessment

**What changes**:
- File locations (git history preserved via `git mv`)
- Path strings in ~218 files (md, yml, json, sh, py)
- One Python constant (`TASK_DIR` in `validate_task_status.py`)

**What does NOT change**:
- Any application source code (`adversarial_workflow/`)
- Test logic or test files (only path references inside them if any)
- `.adversarial/` evaluator config or CLI behavior
- `.serena/` LSP config
- `.claude/` agent definitions (only path references inside them)
- Git hooks behavior (same hooks, updated paths)
- CI workflow (`.github/`)

**Breaking change risk**: LOW. This is a documentation/infrastructure migration. The only runtime code change is `validate_task_status.py` path constant. All other changes are in markdown, YAML, and shell scripts read by agents, not by the application.

## Sequence of Changes (Phase E Detail)

The sed replacements MUST run in this order (overlapping patterns):

1. `.kit/tasks/` → `.kit/tasks/` (most specific first)
2. `.kit/context/` → `.kit/context/`
3. `.kit/context/workflows/` → `.kit/context/workflows/`
4. `.kit/context/reviews/` → `.kit/context/reviews/`
5. `.kit/context/retros/` → `.kit/context/retros/`
6. `.kit/context/templates/` → `.kit/context/templates/`
7. `.kit/context/` → `.kit/context/` (catch-all last)
8. `.kit/adr/` → `.kit/adr/`
9. `docs/adr/` → `docs/adr/`
10. `.kit/launchers/launch` → `.kit/launchers/launch`
11. `.kit/launchers/onboarding` → `.kit/launchers/onboarding`
12. `.kit/launchers/preflight` → `.kit/launchers/preflight`

After sed, manually verify and fix:
- `scripts/validate_task_status.py` line 106: `".kit/tasks/"` → `".kit/tasks/"`
- `.pre-commit-config.yaml` line 63: `^.kit/tasks/.*\.md$` → `^\.kit/tasks/.*\.md$`
- `.pre-commit-config.yaml` line 61: update entry path if scripts restructured
- `CLAUDE.md`: update the directory structure section to show `.kit/` layout, remove references to `delegation/` and `.kit/context/` as active directories
- Run verification greps for bare `delegation`, `agent-context`, `decisions` to catch any remaining references
- Run `pre-commit run --all-files` to confirm hooks work with new paths
- Run `pytest tests/ -v` to confirm no test breakage

## Anti-Patterns to Avoid

Per playbook lessons learned (ASK-0044, ASK-0047):
1. Do NOT split into multiple PRs — must land atomically
2. Grep for bare directory names too, not just full paths
3. Don't trust sed for everything — verify context-aware edits manually
4. Do NOT move `.adversarial/` or `.serena/` (CLI hardcoded paths)
5. Don't delete historical references in retros/changelogs
6. Don't forget `.claude/settings.local.json` permission patterns
7. Don't forget `validate_task_status.py` hardcoded path

## Notes

- No `.dispatch/` in AEL — skip dispatch config step
- `.adversarial/` stays at root (CLI hardcodes path)
- `.serena/` stays at root (Serena hardcodes path)
- `.claude/` stays at root (Claude Code constraint)
- ASK-prefixed handoffs in `.kit/context/` are cross-pollination from early days — move as-is
- This is a library repo with minimal scripts footprint
