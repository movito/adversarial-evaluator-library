---
name: evaluator-versioning
description: Lifecycle policy for adversarial-evaluator-library — how to add, deprecate, and retire evaluators without breaking downstream consumers. Use whenever a model release, prompt rework, or output schema change tempts you to edit an existing evaluator in place.
type: reference
---

# Evaluator Versioning Policy

This library publishes evaluators as a stable contract. Compositions, agent
definitions, downstream projects, and CI pipelines call evaluators by name and
depend on their behavior staying put. Treat every published evaluator the same
way a mature API team treats a public endpoint.

## Core principle: evaluators are immutable contracts

Once an evaluator is registered in `evaluators/index.json`, its observable
behavior is frozen. Behavior changes ship as **new evaluators**, not as edits
to the old one. Old evaluators are deprecated with a pointer to the
replacement, then retired in a later release.

> "When in doubt, ship a new evaluator. Adding one is cheap. Silently breaking
> a consumer's pipeline is not."

## The contract — what consumers depend on

For each evaluator, the contract surface is:

1. **Name** — the stable handle (`gpt54-pro`, `arch-review`, ...)
2. **Model + provider** — drives cost, latency, and capability
3. **Prompt and protocol** — drives output structure
4. **Output schema** — sections, tables, fields
5. **Verdict vocabulary** — the literal strings downstream parsers match against
6. **`output_suffix`** — file naming consumers may glob on
7. **`timeout`** — operational expectation in pipelines

Anything in this list that changes counts as a breaking change.

## What requires a new evaluator vs. an in-place patch

### Requires a new evaluator (and deprecation of the old one)

- Different model (e.g. `gpt-5.4-pro` → `gpt-5.5-pro`)
- Prompt changes that alter output shape, sections, or recommendations
- Verdict vocabulary changes (e.g. `{SOUND, NEEDS_REVISION, UNRELIABLE}` → `{PASS, FAIL}`)
- New or removed output sections / tables
- `output_suffix` change
- Timeout change that materially shifts UX expectations

### In-place patch (bump evaluator patch version, no contract change)

- Typo fix in prompt with no semantic effect
- Comment / documentation polish in `evaluator.yml`
- README updates
- **Phantom model ID corrections** — if the previously shipped model ID never
  resolved against the provider's API, no real consumer ever got a successful
  call, so patching in place is safe. Document as `Fixed`, not `Changed`.
  Precedent: v0.6.1 fixed `gpt-5-turbo-2025-11-01`.

When unsure, treat the change as breaking and ship a new evaluator.

## Naming convention

The library has used two patterns historically. New work should converge on
**Pattern A**, but Pattern B is acceptable for flagship-model evaluators where
the model identity is the point.

### Pattern A — capability + version
`arch-review`, `code-reviewer`, `arch-review-fast`. When you need a breaking
change, ship `arch-review-v2`.

### Pattern B — model-keyed
`gpt54-pro`, `gpt55-pro`, `claude-arch`. Each model version gets its own
evaluator name. Name segment IS the version.

### Anti-pattern — silent in-place upgrades
Do **not** keep the name `gpt54-pro` and quietly point it at `gpt-5.5-pro`.
The historical case of `gpt52-reasoning` running on `gpt-5.4` is a legacy
artefact, not a precedent. Going forward, renames track model upgrades.

## Lifecycle states

Every evaluator entry in `index.json` and `evaluator.yml` carries a `status`:

| State        | Meaning                                                                |
|--------------|------------------------------------------------------------------------|
| `preview`    | Newly added, may still change. Max one minor release.                  |
| `active`     | Stable, recommended. Default for established evaluators.               |
| `deprecated` | Still functions, replacement available, scheduled for retirement.      |
| `retired`    | Removed from `index.json`. Folder may persist for git history.         |

## Required metadata

Each `index.json` entry must include:

```json
{
  "name": "gpt55-pro",
  "provider": "openai",
  "path": "openai/gpt55-pro/evaluator.yml",
  "model": "gpt-5.5-pro",
  "category": "deep-reasoning",
  "description": "...",
  "status": "active",
  "released": "2026-04-28",
  "version": "1.0.0",
  "deprecated_at": null,
  "replaced_by": null
}
```

The same fields belong in the evaluator's `evaluator.yml` so the file is
self-describing. `version` is the evaluator's own semver (independent of the
library's semver).

## Procedures

### A. Add a new evaluator (no replacement)

1. Create `evaluators/<provider>/<name>/` with `evaluator.yml`, `README.md`, `CHANGELOG.md`.
2. Register in `evaluators/index.json` with `status: active` (or `preview` if uncertain) and `released: <today>`.
3. Add an integration test covering happy path + verdict parsing.
4. Bump library MINOR version.
5. Add an `Added` entry to top-level `CHANGELOG.md`.

### B. Replace an existing evaluator (model upgrade, prompt rework)

1. **Pick a new name.** Don't reuse. Pattern B → bump version segment (`gpt54-pro` → `gpt55-pro`). Pattern A → append `-v2`.
2. Run procedure A for the new evaluator.
3. Edit the OLD evaluator's `evaluator.yml`:
   - `status: deprecated`
   - `deprecated_at: <today>`
   - `replaced_by: <new-name>`
4. Mirror those fields in the OLD `index.json` entry.
5. Append a `Deprecated` entry to the OLD evaluator's `CHANGELOG.md` pointing to the replacement.
6. Add `Added` + `Deprecated` entries to top-level `CHANGELOG.md`.
7. Bump library MINOR.
8. **Do NOT delete the old evaluator yet.** Deprecation and retirement are different releases.
9. Update every composition that references the deprecated evaluator (see "Compositions" below).

### C. Retire a deprecated evaluator

1. Confirm at least one full minor library release has elapsed since deprecation.
2. Search `compositions/`, `tests/`, `docs/`, `.kit/`, and known downstream repos for the name. None should remain.
3. Remove the entry from `index.json` (or set `status: retired`).
4. Optionally move the folder to `evaluators/_retired/<provider>/<name>/`. Git history alone is also fine.
5. Add a `Removed` entry to top-level `CHANGELOG.md`.
6. Bump library MAJOR (or MINOR if the library is still pre-1.0 and no callers remain).

## Compositions (always update in lockstep with deprecation)

`compositions/*.yml` reference evaluators by name. When you deprecate
evaluator `X` in favor of `Y`, **update every composition that calls `X` in
the same PR**. Compositions should track only `active` (or `preview`)
evaluators. Leaving a composition pointed at a deprecated evaluator is
how silent rot starts.

## Pre-flight checklist (before any release that touches existing evaluators)

- [ ] Search the workspace for the evaluator name: compositions, tests, docs, `.kit/`, ROADMAP.
- [ ] Search downstream repos that depend on this library for the name.
- [ ] Verify any new model ID resolves: live `models.list` against the provider, sourced from `.env`.
- [ ] Run the new evaluator end-to-end against a sample document before publishing.
- [ ] Update `providers/registry.yml` if a new model family is involved; mark superseded models `legacy`.
- [ ] Update README / SELECTION-GUIDE / COGNITIVE-DIVERSITY docs if the evaluator menu materially changes.

## Worked example — gpt-5.5 release (2026-04-28)

OpenAI shipped `gpt-5.5` and `gpt-5.5-pro` on April 23–24, 2026. Upgrading the
flagship Pro evaluator:

1. **Verify** `gpt-5.5-pro` is callable: `set -a && source .env && set +a && curl ...models | jq '.data[] | select(.id == "gpt-5.5-pro")'`.
2. **Create** `evaluators/openai/gpt55-pro/` (yml, README, CHANGELOG). Copy gpt54-pro's prompt verbatim unless you intend a prompt change. Set:
   - `name: gpt55-pro`
   - `model: gpt-5.5-pro`
   - `output_suffix: -gpt55-pro.md`
   - `version: 1.0.0`
3. **Register** in `index.json` with `status: active`, `released: 2026-04-28`.
4. **Update** `providers/registry.yml`: add `gpt-5.5` and `gpt-5.5-pro` under `gpt.flagship`; mark `gpt-5.4-pro` as `legacy`.
5. **Deprecate** the old: `evaluators/openai/gpt54-pro/evaluator.yml` and `index.json` entry get `status: deprecated`, `deprecated_at: 2026-04-28`, `replaced_by: gpt55-pro`.
6. **Audit** `compositions/`, `tests/`, `docs/` for `gpt54-pro`. None today, but check.
7. **Add** an integration test for `gpt55-pro`.
8. **Bump** library MINOR → `0.8.0`. Update top-level `CHANGELOG.md` with `Added: gpt55-pro` and `Deprecated: gpt54-pro (replaced by gpt55-pro)`.
9. **Schedule retirement** of `gpt54-pro` for `0.9.0` once any downstream usage has migrated.

The same pattern applies if we later upgrade `gpt52-reasoning`,
`gpt5-diversity`, `gpt5-synthesis` to GPT-5.5 — each gets a new name (e.g.
`gpt55-adversarial`, `gpt55-diversity`, `gpt55-synthesis`) and the old ones
are deprecated with `replaced_by` set.

## What this skill does NOT cover

- Creating an evaluator from scratch (prompt design, category placement) — see `docs/adr/ADR-0002-evaluator-expansion-strategy.md`.
- Provider registry schema details — see `providers/registry.yml` header.
- Testing strategy — see `docs/EVALUATOR-TESTING-GUIDE.md`.

## When this skill applies

Invoke this policy whenever:
- A provider releases a new model and you're tempted to bump an existing evaluator's `model:` field.
- You want to change a prompt, verdict vocabulary, or output schema on a published evaluator.
- You're cleaning up legacy evaluators and considering deletion.
- A composition references an evaluator that has been (or should be) deprecated.
