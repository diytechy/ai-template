+++
id = "WI-456"
title = "adjudicate: SR-007, SR-008, SR-009, SR-010, SR-011, SR-020, SR-022, SR-024, SR-032, SR-033, SR-034, SR-036, SR-043, SR-111, SR-113, SR-133 - ratified/routed cell(s) amended on merged trunk 1539f07..7674e4a (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-007", "SR-006", "SR-009", "SR-010", "SR-011", "SR-020", "SR-022", "SR-024"]
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
+++

## Deliverable

Closed DONE 2026-08-15. All 16 rows adjudicated against the LIVE registry and
against a cell-by-cell diff of the adjudicated range `1539f07..7674e4a`, not
against the recorded list: across that range **no row changed any cell beyond
`Boundary-Refs` and `area`** — title, shall, acceptance criteria, rationale,
priority, verification, status, `sn_refs` and phase byte-identical. Neither
amended cell is an obligation cell (`Boundary-Refs` is a new classification
field; `area` was retired by owner ruling `2026-08-14h`), so no attestation
went stale. **Tally: 14 scope-did-not-move (12 clean and still `Verified`, so
no flip was owed in either direction; 2 — `SR-007`, `SR-020` — with a LATER
separately-ruled movement already flipped to `Modified` by `WI-458`) · 2
deleted-by-ruled-demotion (`SR-008` → `LLR-008`, `SR-133` → `LLR-141`, both
obligations landed on `Modified`/`Draft` carriers, scope moved down a tier
rather than out) · 0 scope-change / re-scope / cancellation rows drafted.** No
Status cell flipped by this row. Per-row verdicts in this spec's
`## Disposition`; reasoning in `docs/log.md` entry `2026-08-15f`. Provisional
under the 2026-08-15 charge-through.

## Context

> **Two of the rows in this row's title no longer exist (2026-08-15).** `SR-008`
> and `SR-133` were DEMOTED to the design tier and deleted — SR-008's obligation
> into `LLR-008` under `SR-007` + `SR-006`, SR-133's into `LLR-141` under
> `SR-006` + `SR-156`. Both were `Verified`, and both demotions deliberately
> override that attestation under the owner's 2026-08-15 ruling. So their rows
> in the amendment table below are HISTORY, not an adjudication still owed: what
> this WI must judge for those two is whether the DEMOTION moved scope, on the
> receiving rows, not whether the boundary-ref edit did. The title is left
> unchanged on purpose — editing it renames the file and re-dates the clock.
> Forwarding and reasoning: `docs/log.md`, entry `2026-08-15b`.

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Ratified and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-007 `Boundary-Refs`: '' -> 'B-05'
- SR-007 `area`: 'Declared stack profile' -> ''
- SR-008 `Boundary-Refs`: '' -> 'B-05'
- SR-008 `area`: 'Declared stack profile' -> ''
- SR-009 `Boundary-Refs`: '' -> 'B-05'
- SR-009 `area`: 'Conditional scaffold profiles' -> ''
- SR-010 `Boundary-Refs`: '' -> 'B-05'
- SR-010 `area`: 'Scaffold generation' -> ''
- SR-011 `Boundary-Refs`: '' -> 'B-05'
- SR-011 `area`: 'Scaffold generation' -> ''
- SR-020 `Boundary-Refs`: '' -> 'B-01;B-04'
- SR-020 `area`: 'Git hooks' -> ''
- SR-022 `Boundary-Refs`: '' -> 'B-05'
- SR-022 `area`: 'Vendored-doc drift' -> ''
- SR-024 `Boundary-Refs`: '' -> 'B-05'
- SR-024 `area`: 'Permutation case gen' -> ''
- SR-032 `Boundary-Refs`: '' -> 'B-05'
- SR-032 `area`: 'Onboarding + dev-setup' -> ''
- SR-033 `Boundary-Refs`: '' -> 'B-05'
- SR-033 `area`: 'Release checklist' -> ''
- SR-034 `Boundary-Refs`: '' -> 'B-05'
- SR-034 `area`: 'Portability' -> ''
- SR-036 `Boundary-Refs`: '' -> 'B-05'
- SR-036 `area`: 'Scaffold generation' -> ''
- SR-043 `Boundary-Refs`: '' -> 'B-04'
- SR-043 `area`: 'Unattended coordinator' -> ''
- SR-111 `Boundary-Refs`: '' -> 'B-05'
- SR-111 `area`: 'Scaffold generation' -> ''
- SR-113 `Boundary-Refs`: '' -> 'B-05'
- SR-113 `area`: 'Onboarding + dev-setup' -> ''
- SR-133 `Boundary-Refs`: '' -> 'B-05'
- SR-133 `area`: 'Gate harness' -> ''

Outcomes (§A5.2): flip rows back to Verified where no scope moved
(per the declared ratification level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-007 [project-trajectory/scripts/check.py :: load_profile] tests: (see TC-007) — Stack profile loader
- LLR-008 [project-trajectory/scripts/check.py :: load_profile] tests: (see TC-008) — Profile validation
- LLR-009 [project-trajectory/scripts/bootstrap.py :: select_skills/matches_scope] tests: (see TC-009) — Conditional profile seeding
- LLR-010 [project-trajectory/scripts/bootstrap.py :: MAPPING/main] tests: (see TC-010) — Scaffold writer
- LLR-011 [project-trajectory/scripts/bootstrap.py :: write/--force + write_kit_version] tests: (see TC-011) — Idempotent write + kit-version stamp
- LLR-020 [project-trajectory/hooks/pre-push :: pre-push] tests: (see TC-020) — Pre-push outgoing scan

### Knowledge packs the touched components declare (read before building)
- CMP-009 W4 Human & adopter surfaces: downstream-resync

### Interface seams via the touched modules
- IF-001 (Provides) scripts/trace <-> scripts/check: trace.py CLI: --strict-integrity exits 1 on a duplicate/malformed id or mis-columned row; --strict adds orpha…
- IF-002 (Provides) scripts/check_docs <-> scripts/check: check_docs.py CLI: --stale exits 1 on a broken intra-repo link, a missing PROJECT-VISION tag, or a generated …
- IF-003 (Provides) scripts/check_flows <-> scripts/check: check_flows.py CLI: --no-placeholders; exits 1 when an authored runtime-flow diagram violates its structural …
- IF-004 (Provides) scripts/check_perf <-> scripts/check: check_perf.py CLI: --tier T exits nonzero when a measured metric regresses beyond its declared PB budget tole…
- IF-005 (Provides) scripts/check_privacy <-> scripts/check: check_privacy.py CLI: --repo scans the tree and exits 1 on a secret (always-on floor) or, under docs/privacy-…
- IF-006 (Provides) scripts/check_stubs <-> scripts/check: check_stubs.py CLI: --strict exits 1 on a stub/NotImplemented/pass-only public symbol at the declared gate; c…

## Disposition

> **The heading is SINGULAR on purpose — do not "fix" it to `## Dispositions`.**
> `intake.parse_dispositions` partitions on the literal `\n## Dispositions` and
> **REFUSES the entire mint** ("a ## Dispositions section with no fenced TOML
> draft block - nothing minted") when the section carries no such block. This
> adjudication drafts nothing, deliberately, so the plural heading would arm a
> refusal on the next `intake.py sweep` that touches this row. That an
> adjudication concluding "no follow-up is owed" cannot say so under the heading
> the contract names is a real defect in `intake.py`; it is surfaced here and in
> log `2026-08-15f` rather than patched inline.

**Adjudicated 2026-08-15; closed DONE.** Reasoning and the tally:
[`docs/log.md`](../../log.md), entry `2026-08-15f`. **Provisional** under the
owner's 2026-08-15 charge-through and overturnable at the review sitting.
**NO Status cell is flipped by this row, in either direction** — none needs to
be, which is itself the finding.

### The measurement this adjudication rests on

The 16 rows' cells were re-read on the live registry AND diffed across the
adjudicated range `1539f07..7674e4a`, cell by cell, rather than taken from the
`## Context` list. **Result: across that range not one of the 16 rows changed
any cell other than `Boundary-Refs` and `area`.** Title, `requirement`,
`acceptance_criteria`, `rationale`, `priority`, `verification`, `status`,
`sn_refs` and `phase` are byte-identical before and after the merge for all 16.
The `## Context` list is complete; there is no unlisted normative edit hiding
behind it.

That is what decides the whole adjudication. **Neither amended cell is an
obligation cell.** `Boundary-Refs` was a NEW field the re-tier added — it
classifies which crossing a row's observable sits at; it does not change what
the row obliges, what evidence discharges it, or which test verifies it.
`area` was a free-text descriptor **retired by owner ruling `2026-08-14h`** for
the closed `Aspect` vocabulary, its derivable values dropped rather than
remapped. An attestation is an acceptance of an obligation and its evidence.
Nothing that was accepted is now false on any of these rows, so no attestation
went stale.

**The general disposition, therefore: SCOPE DID NOT MOVE. The amendment is the
ruled re-tier work itself, and the re-attestation rides that wave rather than
being owed row-by-row here.** Each row is still listed below because the
instruction was to check, not to rubber-stamp, and two groups genuinely differ.

### Group 1 — scope did not move; attestation stands; no flip owed (12 rows)

Each is still `Verified` on the live registry and was never flipped, so §A5.2's
"flip rows back to Verified" is vacuous for them — they never left. Live state
confirmed row by row.

| SR | Amended | Live status | Disposition |
|---|---|---|---|
| SR-009 | `Boundary-Refs` '' → `B-05`; `area` dropped | Verified | scope did not move — ruled re-tier work |
| SR-010 | `Boundary-Refs` '' → `B-05`; `area` dropped | Verified | scope did not move — ruled re-tier work |
| SR-011 | `Boundary-Refs` '' → `B-05`; `area` dropped | Verified | scope did not move — ruled re-tier work |
| SR-022 | `Boundary-Refs` '' → `B-05`; `area` dropped | Verified | scope did not move — ruled re-tier work |
| SR-024 | `Boundary-Refs` '' → `B-05`; `area` dropped | Verified | scope did not move — ruled re-tier work |
| SR-032 | `Boundary-Refs` '' → `B-05`; `area` dropped | Verified | scope did not move — ruled re-tier work |
| SR-033 | `Boundary-Refs` '' → `B-05`; `area` dropped | Verified | scope did not move — ruled re-tier work |
| SR-034 | `Boundary-Refs` '' → `B-05`; `area` dropped | Verified | scope did not move — the `area` value was RE-EXPRESSED, not lost: this row is one of the 21 that carry `aspect = "portability"` |
| SR-036 | `Boundary-Refs` '' → `B-05`; `area` dropped | Verified | scope did not move — ruled re-tier work |
| SR-043 | `Boundary-Refs` '' → `B-04`; `area` dropped | Verified | scope did not move — and the crossing pick is corroborated: `IF-020` (subagent_gate) is the one interface row tied to `B-04` and its `owner` cell reads `SR-043` |
| SR-111 | `Boundary-Refs` '' → `B-05`; `area` dropped | Verified | scope did not move — ruled re-tier work |
| SR-113 | `Boundary-Refs` '' → `B-05`; `area` dropped | Verified | scope did not move — ruled re-tier work |

### Group 2 — scope did not move HERE, but moved LATER by a separate ruled act, already recorded and already flipped (2 rows)

Both rows are `Modified` on the live registry, and **neither flip was caused by
the amendment this row adjudicates.** The diff proves it: across `1539f07..7674e4a`
both were untouched beyond `Boundary-Refs`/`area` and both were still `Verified`
at `7674e4a`. What moved them is WI-458's demotion pass (log `2026-08-15b`),
which is a *later, separately ruled* act with its own record. Nothing is owed
here for either; the re-attest sitting already sees them through their
`Modified` status.

- **SR-007** (`Boundary-Refs` '' → `B-05`; `area` 'Declared stack profile'
  dropped). Amendment: no scope movement. Subsequently: **scope EXPANDED** —
  the row absorbed `SR-008`'s obligation on 2026-08-15, gaining "refused when it
  is broken" in its title and "failing loudly on a malformed profile or a
  non-integer coverage threshold" in its shall. `Verified` → `Modified`, an
  attestation override made deliberately under the owner's 2026-08-15 ruling and
  named in the log rather than ridden in quietly.
- **SR-020** (`Boundary-Refs` '' → `B-01;B-04`; `area` 'Git hooks' dropped).
  Amendment: no scope movement, and the two-crossing attribution is
  independently corroborated by WI-459's sweep — `SR-020` is the `owner` cell of
  `IF-043`, the pre-push half of the hook floor. Subsequently: the row became
  the parent of retired `SR-021`'s interpreter probe (rationale amended,
  `Verified` → `Modified`, same ruled pass). The shall itself is unchanged.

### Group 3 — row deleted by ruled demotion; the demotion judged on the RECEIVING rows (2 rows)

Per this spec's own `## Context` note, what is owed for these two is not a
verdict on the boundary-ref edit but on the demotion. Both were `Verified` and
both demotions deliberately override that attestation under the owner's
2026-08-15 ruling. **The check that matters is whether an obligation was
dropped in transit. It was not** — each landed on a named carrier, and every
receiving row carries a status that surfaces it to the re-attest sitting:

- **SR-008** → `LLR-008` "Profile validation", `sr_refs = ["SR-007", "SR-006"]`,
  status `Modified`. Both parents are `Modified`. The split is deliberate and
  recorded: the malformed-profile clause went to SR-007, the missing-declared-binary
  clause was NOT folded because SR-006 already states it verbatim.
  **Disposition: row deleted by ruled demotion (see log `2026-08-15b`); scope
  moved DOWN a tier, not out; no obligation lost; nothing owed here.**
- **SR-133** → `LLR-141` "Work-branch lane signal + freshness skip",
  `sr_refs = ["SR-006", "SR-156"]`, status `Modified`. `SR-006` is `Modified`,
  `SR-156` is `Draft`. The demotion criterion was the row's own rationale, which
  read "Decomposed from SR-006".
  **Disposition: row deleted by ruled demotion (see log `2026-08-15b`); scope
  moved DOWN a tier, not out; no obligation lost; nothing owed here.**

### Tally

**16 rows: 14 scope-did-not-move (12 clean · 2 with a later, separately ruled
and already-flipped movement) · 2 deleted-by-demotion · 0 real scope-change,
re-scope or cancellation rows drafted.** No successor is minted, because none is
owed: no amendment in the adjudicated range changed an obligation, and every
change that DID change one is already carried by a `Modified`/`Draft` status
awaiting the ratification wave.
