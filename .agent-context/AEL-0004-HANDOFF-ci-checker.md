# AEL-0004 Handoff: Verify CI Workflow Runs on GitHub

**Target Agent**: ci-checker
**Created**: 2026-01-31
**Planner**: coordinator

---

## Mission

Verify that the GitHub Actions CI workflow runs successfully on the adversarial-evaluator-library repository after the initial push to GitHub.

## Context

- Repository: `movito/adversarial-evaluator-library` (private)
- Branch: `main`
- CI workflow: `.github/workflows/test.yml`
- Just pushed initial content to GitHub

## CI Workflow Structure

**File**: `.github/workflows/test.yml`

| Job | What it does | Pass criteria |
|-----|--------------|---------------|
| `test` | pytest with coverage | All tests pass, 80%+ coverage |
| `lint` | Black, isort, flake8 | No formatting errors |

## Execution Steps

### Step 1: Check for Existing Runs

```bash
gh run list --workflow=test.yml --limit 5
```

If runs exist, check their status. If the most recent passed, task may already be complete.

### Step 2: Trigger Workflow (if needed)

If no runs or need fresh verification:

```bash
gh workflow run test.yml --ref main
```

### Step 3: Monitor the Run

```bash
# Get the run ID from step 1 or 2, then watch
gh run watch <run-id>

# Or watch the most recent
gh run watch
```

### Step 4: Verify Results

```bash
# View run details
gh run view <run-id>

# If failed, check logs
gh run view <run-id> --log-failed
```

**Check**:
- [ ] `test` job: ✅ PASSED
- [ ] `lint` job: ✅ PASSED
- [ ] Coverage reported: ≥80%

### Step 5: Report Results

**If PASSED**:
- Report success with run URL
- Note any warnings
- Task complete

**If FAILED**:
- Document which job failed
- Include relevant error messages
- Suggest fixes if obvious
- Keep task in progress

## Success Criteria

| Criterion | Target |
|-----------|--------|
| test job | PASSED |
| lint job | PASSED |
| Coverage | ≥80% |
| Run time | <5 minutes |

## Useful Commands

```bash
# List workflows
gh workflow list

# View workflow file
gh workflow view test.yml

# List runs with status
gh run list --workflow=test.yml

# View specific run
gh run view <run-id>

# View failed logs
gh run view <run-id> --log-failed

# Manual trigger
gh workflow run test.yml --ref main
```

## References

- Task spec: `delegation/tasks/2-todo/AEL-0004-verify-ci-workflow.md`
- Workflow file: `.github/workflows/test.yml`
- Repository: https://github.com/movito/adversarial-evaluator-library
