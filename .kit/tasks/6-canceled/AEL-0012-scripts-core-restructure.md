# AEL-0012: Restructure scripts/ to core/ + local/

**Status**: Canceled
**Canceled Reason**: Superseded by AEL-0013 (kit migration, which includes scripts restructure)
**Priority**: Low
**Type**: Infrastructure
**Estimated Effort**: 30 minutes
**Created**: 2026-03-08
**Depends On**: ASK-0042 (core established in agentive-starter-kit)
**Parent**: KIT-0024 (Core Scripts Standardization)

## Summary

Adopt the `scripts/core/` + `scripts/local/` layout in adversarial-evaluator-library.
This repo has a minimal scripts footprint (11 files) and no broken commands,
so this is the lowest-priority downstream migration.

## Current State

- 11 scripts in flat `scripts/` directory
- Has `verify-ci.sh` (unlike adversarial-workflow) — only 1 slash command (`/check-ci`)
- Has `verify-v0.4.0.sh` — AEL-specific migration script
- No bot-management scripts (check-bots, wait-for-bots, etc.)
- Linear sync scripts present but may not be actively used

## Scope

### 1. Create directory structure

```
scripts/
  ├── core/                        ◀── 12 scripts from agentive-starter-kit
  │   └── (same as ASK-0042 core bundle)
  ├── local/                       ◀── AEL-specific scripts
  │   └── verify-v0.4.0.sh
  ├── .core-manifest.json
  └── README.md
```

### 2. Replace shared scripts with canonical versions

Copy all 12 core scripts from `agentive-starter-kit/scripts/core/`.

### 3. Move AEL-specific scripts to local/

- `verify-v0.4.0.sh` → `scripts/local/verify-v0.4.0.sh`

### 4. Handle optional scripts

Linear sync scripts go to `local/` if actively used, otherwise remove:
- `linear_sync_utils.py`
- `sync_tasks_to_linear.py`

### 5. Update references

- `.claude/commands/check-ci.md` — update path
- `.pre-commit-config.yaml` — update hook paths
- Any agent definitions

## Acceptance Criteria

- [ ] `scripts/core/` contains 12 scripts + VERSION (identical to ASK)
- [ ] `scripts/local/` contains AEL-specific scripts
- [ ] No shared scripts at `scripts/` root
- [ ] `/check-ci` works with new path
- [ ] CI passes
- [ ] Pre-commit hooks pass

## Notes

- This repo is intentionally minimal (it's a library, not a full project)
- Many core scripts (check-bots, preflight, etc.) may not be used here,
  but having them ensures consistency and enables future workflow adoption
- The PR automation scripts become useful if/when AEL adopts the full
  agent development workflow
