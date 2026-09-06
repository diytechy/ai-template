# H1 execution — parsed SR-parent hat context

**Scope:** H1's explicit parent half. `_hat_slots` now delegates to
`plan_briefs.hat_surface_for_work_item`, which carries the existing work-item
tags into each independent SN parent reached through the row's parsed
`SR-Refs` → SR `SN-Refs` edges. It also resolves a
`SpecRef` only when its path explicitly names the canonical
`stakeholder-needs.toml`/`.md` carrier and its fragment is an exact SN ID. No
need schema field or prose/tag scanning was added.

**Base:** `83f2c7aa990a757729e7847816d40a8cdc2afcc7` (`git rev-parse HEAD`,
2026-09-06). The working tree already contained the parent agent's unrelated
changes; this slice touched only `project-trajectory/scripts/plan_briefs.py`,
`project-trajectory/scripts/plan_runner.py`, `tests/test_hats.py`, and this
record.

## Before

Before this slice, `_hat_slots` called only
`hat_context_for_work_item`, so a two-parent fixture with no WI tags emitted
only its always-on `SECURITY` hat. Its parent `scope` values and tags never
reached the brief. The exact pre-edit probe returned:

```
before-hats: ['SECURITY']
```

The same omission affected the H1 SN-026-shaped probe: its explicit need
context was never read.

## Change

`plan_briefs.hat_surface_for_work_item` uses the shared ref splitter,
`spine_carrier.load` for SR rows, `spine_carrier.load_needs` for the `id`-keyed
SN rows, and `hats.applicable`/`context_from_need` for each parent. Each parent
context unions that need's tags with the WI's typed Workstream/SafetyClass tags,
so a valid cross-field `and` predicate can fire; sibling needs are never merged,
so one parent cannot lend its tag or scalar to another. Selected names are
projected back through the loaded roster, preserving declaration order.
Declared unknown SR/SN IDs and absent required carriers raise `HatsError`.
`spine_carrier` parse/dual-home refusals remain `SystemExit` at the reader but
the round's existing intake boundary converts them to typed `PAGE`, preserving
the reason. The legacy template no-slot guard and absent-roster opt-out both
return before any parent read. A canonical needs-carrier `SpecRef` fragment adds
one explicit need context; a goal/spec document remains context-free, and a bad
canonical fragment or unknown exact SN ID refuses.

Before the live SN-026 tag amendment, the WI-059 probe (`SR-154;SR-155`)
resolved SN-026, SN-024, SN-006 and SN-002. Its parent tag union was
`unattended;loop;scripts;personal-data`; the repaired brief emits 14 hats,
including `FIRST-RUN-ADOPTER`, `CROSS-PLATFORM`, and `DATA-PROTECTION`, in the
roster's declared order. The subsequently authored SN-026 tags add `legal` and
`personal-data`; a real `hat_surface_for_work_item` call scoped directly by
`stakeholder-needs.toml#SN-026` now includes UNATTENDED-OPS, LEGAL and
DATA-PROTECTION. Only those two tags changed on the live need: its need,
acceptance, rationale and Status remain unchanged, and no approval snapshot
was written. The [amendment record](DECOMPOSITION-AMENDMENTS.md#h1--record-the-legal-and-data-protection-applicability-of-sn-026)
preserves the applicability decision and separates the unbuilt SR-175 work.

## Redaction and consent boundary

The approved two-file redaction boundary belongs to
`plan_briefs.build_surface`: the current governing design row is
`LLR-176` (`low-level-requirements.toml:1809-1819`), while `LLR-181` at
`:1869-1879` governs the shared `kitlib` package and is unrelated to this
surface. H1 leaves `build_surface` unchanged. The new helper is a separately
named hat-context read of the roster and explicit SR/SN parent carriers; it
does not add those rows to the model-provider surface or weaken any exclusion.
`SR-175` therefore remains an approved but unbuilt inclusion/consent contract,
including its planted-credential acceptance. H1's context resolution does not
discharge that gap or silently change provider consent; it only chooses which
declared perspective questions enter the decomposition brief.

## Verification

### Adversarial corrections

Three focused characterizations failed against the frozen first pass and then
passed after the correction:

1. `tags contains "scripts" and scope == "template"` did not fire because WI
   and parent contexts were evaluated separately. The corrected per-parent
   composition fires it, while `tags contains "need-only" and scope ==
   "repository"` remains false because those facts belong to different needs.
2. With no roster, an explicit but unresolved `SR-Refs` still caused a refusal.
   The absent/empty roster now returns the existing no-hats block before reading
   either spine carrier.
3. A malformed SR carrier raised `SystemExit` from `build_surface` before the
   roster handler and escaped `run_dual_plan_round`. Surface construction is now
   inside the existing context-intake boundary, which returns `PAGE` with the
   carrier's original refusal text.

The resolution is split into exact-parent discovery, per-parent WI+SN context
composition, and selection. No fallback, inferred prose scope, second registry,
or generic context framework was added. The H1 production delta is 97 net lines
in `plan_briefs.py`; the `plan_runner.py` correction removes two net lines. The complexity
ratchet remains at its prior baseline.

Focused commands, run with the repository `.venv`:

```
.venv/bin/ruff check project-trajectory/scripts/plan_briefs.py project-trajectory/scripts/plan_runner.py tests/test_hats.py
.venv/bin/pytest -q tests/test_complexity_ratchet.py tests/test_hats.py tests/test_dual_plan_round.py
git diff --check -- project-trajectory/scripts/plan_briefs.py project-trajectory/scripts/plan_runner.py tests/test_hats.py docs/ai-template-redesign-2026-09-05-codex/H1-EXECUTION.md
```

Results:

```
All checks passed!
79 passed in 4.10s
```

The tests cover per-parent WI-tag composition, cross-parent non-composition,
multi-parent scalar contexts, roster order, roster opt-out before scope reads,
unknown SR/SN references, absent required carriers, CSV-SR plus Markdown-SN
resolution, canonical TOML/Markdown SpecRef aliases, the SN-026-shaped explicit
fragment, unrelated goal SpecRefs, typed PAGE on malformed carrier refusal, and
the legacy no-slot override. The complexity ratchet and existing dual-plan
round suite pass. No provider was invoked, and no queue, registry, schema, or
process file was changed.

## OI-85 follow-up (2026-09-06)

The historical no-snapshot statement above describes the first H1 slice.
The owner has since re-attested SN-026's two tags through the
[OI-85 named-registry act](../log.d/2026-09-06-oi85-owner-ruling.md).
H1 and R-E now use the same canonical need-carrier spelling helper, following
native path semantics for `./`, lexical `..`, whitespace and platform
separators. A known-empty canonical need registry still rejects a nonexistent
ID; malformed need content refuses. Other TOML files do not become inferred
registries simply because they contain nested tables. The
[continuation log](../log.d/2026-09-06-oi85-plan-completion.md) carries the
failure-first regressions and final verification.
