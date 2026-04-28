# AEL-0014: Fix Mistral/aider whole-edit-format source-file corruption

**Status**: Canceled
**Canceled Reason**: Aider has been removed from the evaluator pipeline. `adversarial-workflow` v1.0.1 uses LiteLLM directly (deps: `aiohttp, litellm, python-dotenv, pyyaml` — no aider). The corruption path no longer exists. Legacy `aider` references remain in `.adversarial/scripts/*.sh` and `.adversarial/docs/EVALUATION-WORKFLOW.md`, but those are stale shell scripts from the older workflow, not the current pipeline.
**Canceled Date**: 2026-04-28
**Priority**: high
**Assigned To**: unassigned
**Created**: 2026-04-28
**Target Completion**: TBD

## Overview

Aider's "whole edit format" mode — invoked by Mistral evaluators in the
adversarial pipeline — has been observed writing review output **into the
source file being evaluated** instead of only into the evaluator's log file.
Any evaluator that uses aider's whole-edit-format can silently corrupt the
file it is reviewing.

**Context**: First observed 2026-04-02 while running the `mistral-content`
evaluator on `docs/adr/ADR-0007-unified-artifact-registry.md`. Aider
prepended ~176 lines of review content to the ADR source, reported
`Applied edit to docs/adr/ADR-0007-unified-artifact-registry.md` and
`59 / 449 lines [13%]`, then crashed with
`summarizer unexpectedly failed for all models`. The `--no-auto-commits`
flag prevents git commits but does **not** prevent file writes.

**Why this matters**: Evaluators must be safe to run against any file,
including critical specs and source code. Silent corruption is a
contract-breaking bug.

## Reproduction

1. Check out a clean working tree
2. Run a Mistral evaluator (e.g. `mistral-content`) against any markdown
   file — ADRs and longer documents seem more likely to trigger
3. Observe `git diff` after the run — review content is prepended to the
   source

(Exact reproduction is intermittent; the 2026-04-02 incident may have
been triggered by aider's summarizer fallback path. Investigate before
fixing.)

## Acceptance Criteria

- [ ] Root cause identified (which aider invocation path writes the file?)
- [ ] Mistral evaluators run without ever modifying the input file —
      verified by checksum-before / checksum-after on a regression test
- [ ] Regression test added that runs a Mistral evaluator against a fixture
      file and asserts the fixture is byte-identical afterwards
- [ ] Other evaluators audited for the same risk (any `aider`-based path)

## Approach (suggested)

Two plausible fixes — pick based on root-cause finding:

1. **Pass the input file as `--read-only`** to aider, so its edit format
   physically cannot write back to it.
2. **Sandbox the input** — copy the file to a temp dir, point aider at the
   copy, and never let aider see the original path.

Option 1 is simpler if aider supports `--read-only` reliably for the
calling pattern; option 2 is bulletproof.

## References

- Original incident notes: memory `project_evaluator_bug.md`
  (Mistral whole-edit-format corruption, 2026-04-02)
- Affected evaluator family: `evaluators/mistral/*` (any that route
  through aider)
- Adversarial workflow runner: `adversarial-workflow` package
  (separate repo — fix may live there, not here)

## Notes

- This bug predates the 0.8.0 / 0.9.0 / 0.10.0 model upgrades and is
  unrelated to model choice. The `mistral-large-2411` evaluator was the
  first observed offender; the same path is shared by other Mistral
  evaluators.
- A proper fix may require coordination with the upstream
  `adversarial-workflow` runner. Investigate where the aider invocation
  actually lives before scoping the fix to this repo.
