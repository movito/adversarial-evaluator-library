# Feedback: Evaluator Discovery Structure Mismatch

**From**: adversarial-evaluator-library team (via agentive-starter-kit)
**Date**: 2026-02-08
**Workflow Version**: 0.9.3
**Severity**: Medium (requires manual workaround)

---

## Summary

The `adversarial library install` command clones the library and copies provider directories, but evaluators aren't discovered by `adversarial list-evaluators` without manual intervention.

## Expected vs Actual

### Library Structure
```
evaluators/
├── anthropic/
│   ├── claude-adversarial/
│   │   └── evaluator.yml
│   ├── claude-code/
│   │   └── evaluator.yml
│   └── claude-quick/
│       └── evaluator.yml
└── google/
    └── gemini-code/
        └── evaluator.yml
```

### CLI Expected Structure
```
.adversarial/evaluators/
├── anthropic-claude-adversarial.yml  # Flat, prefixed filename
├── anthropic-claude-code.yml
├── anthropic-claude-quick.yml
└── google-gemini-code.yml
```

## Current Workaround

Users must manually copy and rename:
```bash
# After library install
cp evaluators/anthropic/claude-quick/evaluator.yml \
   .adversarial/evaluators/anthropic-claude-quick.yml
```

## Suggested Fix

### Option A: Fix in `adversarial library install`

The install command should flatten and rename evaluator files:

```python
# Pseudocode
for provider in library/evaluators/:
    for evaluator in provider/:
        src = f"evaluators/{provider}/{evaluator}/evaluator.yml"
        dst = f".adversarial/evaluators/{provider}-{evaluator}.yml"
        copy(src, dst)
```

### Option B: Update CLI discovery to support nested structure

Update `list-evaluators` to also scan:
```
.adversarial/evaluators/{provider}/{name}/evaluator.yml
```

### Option C: Document the manual step

Add to library README:
```bash
# After cloning, run:
./scripts/flatten-evaluators.sh
```

## Impact

- **agentive-starter-kit**: Had to manually copy evaluator YAMLs
- **Other consumers**: Will hit same issue with `install-evaluators` command
- **Library team**: Can't provide seamless install experience

## Related

- v0.4.0 release (cross-provider support)
- Tag push fix (v0.2.2 was missing from remote)
