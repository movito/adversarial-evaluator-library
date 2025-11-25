---
description: Verify GitHub Actions CI/CD status for a branch
---

# Check CI/CD Status

Verify that GitHub Actions workflows have passed for a specific branch.

## Usage

```
/check-ci [branch-name]
```

If no branch is specified, checks the current branch.

## Task

Please verify the CI/CD status for the specified branch using the `verify-ci.sh` script:

1. **Run verification script**:
   ```bash
   ./scripts/verify-ci.sh {{branch-name or current branch}}
   ```

2. **Report results**:
   - ✅ PASS: All workflows completed successfully
   - ❌ FAIL: One or more workflows failed (provide failure details)
   - ⏱️ TIMEOUT: Workflows still running after timeout

3. **If failures detected**:
   - Show which workflows failed
   - Provide command to view detailed logs: `gh run view <run-id> --log-failed`
   - Summarize next steps for the user

## Context

This command is used to verify that pushed code passes all CI/CD checks before marking tasks complete. It's particularly important because local tests may pass while CI fails due to:

- Environment differences (Python versions, dependencies)
- Race conditions
- GitHub Actions-specific configuration
- Network-dependent tests

## Example Output

```
✅ CI/CD Status: PASS

All workflows completed successfully for branch 'feature/new-feature':
- Python tests: ✅ PASS
- Type checking: ✅ PASS
- Linting: ✅ PASS

Safe to proceed with task completion.
```

Or:

```
❌ CI/CD Status: FAIL

Workflow failures detected for branch 'feature/xyz':
- Python tests: ❌ FAIL (job: test-suite)
- Type checking: ✅ PASS
- Linting: ✅ PASS

View failure details:
  gh run view <run-id> --log-failed

Fix the failing tests before completing your task.
```
