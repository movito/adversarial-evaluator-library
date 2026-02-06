# Feedback: Exit Code 1 Despite Successful Evaluation

**From**: adversarial-evaluator-library team
**Date**: 2026-02-06
**Workflow Version**: 0.9.1
**Severity**: Low (non-blocking, cosmetic)

---

## Summary

`adversarial evaluate --evaluator <name>` returns exit code 1 with an error message even when evaluations complete successfully and produce valid output.

## Observed Behavior

```bash
$ adversarial evaluate --evaluator fast-check /tmp/test-document.md

Using evaluator: fast-check
Using timeout: 180s (default)
FAST-CHECK: Evaluating /tmp/test-document.md
FAST-CHECK: Using model gpt-4o-mini
FAST-CHECK: Output written to .adversarial/logs/test-document--fast-check.md.md
Evaluation failed: Log file missing evaluation content - no verdict or analysis found

$ echo $?
1
```

**However**, the output file contains valid evaluation results:

```markdown
⚠️ ISSUES FOUND

• Line/Section: Content
• Issue: Spelling error ("Item tree" should be "Item three")
• Fix: Change "Item tree" to "Item three"

Total issues: 1 (Critical: 0, Minor: 1)
```

## Expected Behavior

Exit code 0 when:
- Model was called successfully
- Output file was written
- Content was generated

Exit code 1 only when:
- API call failed
- No output produced
- Actual error occurred

## Root Cause

The workflow's output validator appears to look for specific verdict keywords like:
- `APPROVED` / `NEEDS_REVISION` / `BLOCKED`
- Or specific section headers

Library evaluators use varied output formats based on their purpose (quick-check vs deep-reasoning vs code-review), and don't all include these exact keywords.

## Impact

- **CI/CD integration**: Scripts checking exit codes will incorrectly report failures
- **User experience**: Confusing error message when evaluation succeeded
- **Automation**: Can't reliably use `&&` chaining

## Suggested Fixes

### Option A: Make verdict validation optional (Recommended)

```bash
# Default: no validation
adversarial evaluate --evaluator fast-check doc.md

# Opt-in strict mode
adversarial evaluate --evaluator fast-check --strict doc.md
```

### Option B: Check for any meaningful content

Instead of looking for specific keywords, validate that:
- Output file exists
- Output file has content beyond the header
- Model response was received

### Option C: Library provides verdict format

We could update all 18 evaluators to include a standard verdict block:

```markdown
## Verdict
✅ APPROVED | ⚠️ NEEDS_REVISION | ❌ BLOCKED
```

This is more work and may not suit all evaluator types (e.g., `mistral-fast` is for quick scanning, not pass/fail decisions).

## Test Cases

All three tests below produce valid output but return exit code 1:

| Provider | Evaluator | Model | Output | Exit Code |
|----------|-----------|-------|--------|-----------|
| OpenAI | fast-check | gpt-4o-mini | ✅ Valid | 1 ❌ |
| Google | gemini-flash | gemini-2.5-flash | ✅ Valid | 1 ❌ |
| Mistral | mistral-fast | mistral-small-latest | ✅ Valid | 1 ❌ |

## Workaround

For now, users can:
1. Ignore exit code
2. Check `.adversarial/logs/` for actual output
3. Use `|| true` in scripts if needed

---

**Priority**: Low - evaluations work correctly, this is UX polish

**Recommendation**: Option A (make validation optional) preserves backwards compatibility while fixing the issue for library evaluators.
