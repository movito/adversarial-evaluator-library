# AEL-0004: Verify CI Workflow Runs on GitHub

**Status**: Todo
**Priority**: high
**Assigned To**: ci-checker
**Estimated Effort**: 15 minutes
**Created**: 2026-01-31
**Target Completion**: 2026-01-31

## Related Tasks

**Depends On**: AEL-0003 (CI workflow exists)
**Related**: AEL-0002 (smoke tests - same tests run in CI)

## Overview

Verify that the inherited CI workflow from agentive-starter-kit runs successfully on the adversarial-evaluator-library GitHub repository. This confirms the project is properly configured for continuous integration.

**Context**: We pushed to GitHub and have a CI workflow at `.github/workflows/test.yml`. We need to confirm it executes without errors on this repository.

## Requirements

### Functional Requirements
1. Trigger a CI run (push or manual workflow dispatch)
2. Verify the `test` job completes successfully
3. Verify the `lint` job completes successfully
4. Confirm coverage threshold is met (80%)
5. Document any failures or warnings

## CI Workflow Details

**File**: `.github/workflows/test.yml`

**Jobs**:
| Job | Purpose | Pass Criteria |
|-----|---------|---------------|
| `test` | Run pytest with coverage | All tests pass, 80%+ coverage |
| `lint` | Black, isort, flake8 | No formatting/linting errors |

**Triggers**:
- Push to main/develop
- PR to main/develop
- Manual dispatch

## Implementation Plan

### Step 1: Check Current CI Status

```bash
# View recent workflow runs
gh run list --limit 5

# Or check specific workflow
gh workflow view test.yml
```

### Step 2: Trigger CI if Needed

If no runs exist or last run is stale:

```bash
# Manual trigger
gh workflow run test.yml --ref main
```

### Step 3: Monitor Run

```bash
# Watch the run
gh run watch

# Or view specific run
gh run view <run-id>
```

### Step 4: Verify Results

Check:
- [ ] `test` job: PASSED
- [ ] `lint` job: PASSED
- [ ] Coverage: ≥80%
- [ ] No warnings in logs

### Step 5: Document Results

If PASSED: Mark task complete
If FAILED: Document failure details, keep in progress

## Acceptance Criteria

### Must Have ✅
- [ ] CI workflow triggered on GitHub
- [ ] `test` job completes successfully
- [ ] `lint` job completes successfully
- [ ] Coverage threshold met (80%)

### Should Have 🎯
- [ ] No warnings in CI logs
- [ ] Run time documented

## Success Metrics

### Quantitative
- Jobs passed: 2/2
- Coverage: ≥80%
- CI run time: <5 minutes (typical)

### Qualitative
- Clean CI logs
- No flaky tests

## Notes

- This is a verification task, not implementation
- If CI fails, create follow-up task for fixes
- The workflow ignores changes to docs/delegation/.claude/.agent-context

---

**Template Version**: 1.0.0
