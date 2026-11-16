+++
id = "WI-999"
title = "SR-165's derivation record is built: the record cells, the component check and a record for each live component"
workstream = "process"
sr_refs = ["SR-165"]
specref = ""
needs = []
buildtier = "medium"
safety_class = "ordinary"
planmode = "single"
priority = 5
+++

## Deliverable

Every live component row holds the partition's derivation record or cites the
row holding it, and `trajectory_arch.component_findings` reports a row whose
record is absent, incomplete, malformed or inconsistent, WARN plain and ERROR
under `--strict`. The rules are `derivation_record_findings` and its small
helpers, called on the rows the pass already loads, so the registry has no
second reader. `[checks] components_check = false` still turns the whole pass
off; no setting was added.

- **Schema** (85811e4bb): the eight cells on `kitlib.spine.OFFSPINE_KEYS`, the
  carrier's column map and `migrate_carrier.KEY`, and on the template's `-000`
  row.
- **Backfill** (864bcea5d): CMP-006 holds the record OI-130's ruling states;
  CMP-007, CMP-008 and CMP-009 carry `derivation = "CMP-006"`. The act
  `intake.py snapshot --approves components=docs/log.d/2026-11-16-operator-rules-oi130.md
  --reattests CMP-006,CMP-007,CMP-008,CMP-009` (act seq 182) copied only
  `components.toml`. It also absorbed CMP-006's `notes` amendment, pending
  since the 2026-08-30 copy.
- **Rules and tests** (1146c5b95): ten tests in `tests/test_trajectory_arch.py`
  cover TC-166 (a)-(e) and each malformed and inconsistent state, each tagged
  `Implements: TC-166`, and TC-166's evidence names them. `trajectory_arch.py`
  grew 1012 -> 1132 SLOC (pin re-stamped). `PROCESS_OPTIONS.md` "Component
  layer" states the record (+1,272 bytes, a watched file).
- **RESYNC entry**: "Live component rows carry a derivation record", a forced
  migration.

Built on the maintenance branch `maint/wi-999`, outside the lane workflow, at
the operator's direction: no claim, no lane review rounds, and commits made
with the hook bypassed. The tests-first commit under `[bars] red_mark` (steps
3 and 4 of the landing order below) was not used; the rules and their tests
landed in one commit, every commit strict-green. The review is the maintenance
branch's cross-family review, still to run.

## Context

Filed by hand in headless leg 33 (2026-11-04) as OI-127's placeholder. OI-127
was ruled (b), revised, on 2026-11-05, and this row became the routed work for
TC-166. No test and no code stand behind it, and LLR-172 states "NOT BUILT
YET". OI-129 was ruled (a) on 2026-11-08: an approved row is built unless
evidence shows substantial work.

**Where the partition was derived.** The 2026-08-16 plans derived the
requirement (`blind-derivation-a.md:101`, `-b.md:84`), not the partition. The
partition that produced CMP-006..009 was derived on 2026-08-13 by WI-441:

- **Candidates and per-metric scores:**
  `docs/archive/plans/2026-08-13-part-a-data-pack.md` §5, table at lines 484-490
  (P1-P5).
- **Ranking:** `docs/archive/plans/2026-08-13-part-a-shortlist-ruling.md:13-21`.
- **Objective:** OI-14 (A3), "ONE HOME PER BEHAVIOUR as a hard constraint and
  cut-count as the tie-breaker".

Three findings hold the backfill:

1. **Every candidate violates the hard constraint**
   (shortlist-ruling.md:42-50). The cut count alone ranks P3 first (30), not
   P5 (31).
2. **The recorded order follows no declared objective.** The shortlist ranked
   by straddle with judgement (P5, P3, P4, P1, P2). Straddle alone gives P5,
   P4, then P3 and P1 tied.
3. **Whether the human ruling adopted the partition is unclear.**
   - Approval of P5 was DEFERRED on 2026-08-13 (`docs/log.md:3814-3823`, decision
     10: approve again "on re-derived numbers").
   - On 2026-08-22 the owner approved the four rows ("looks good, approve",
     `docs/log.md:41498-41501`, commit `4fd20f898`).
   - On 2026-08-23 the log still called "the deferred P5 approval" the owner's
     to take (`docs/log.md:45536-45540`).

Writing the records needed answers this row could not invent (B3, B4). OI-130
was ruled on 2026-11-16: see "The operator's ruling".

## The record form (S3: closed)

**Cells.** The record is eight flat cells on the component schema. A cell
cannot be a table: `spine_carrier` refuses one.

| Key | Value |
|---|---|
| `candidates` | the distinct candidate names, in the recorded ranking order, best first |
| `objective` | `"minimize <metric>"` or `"maximize <metric>"` |
| `constraints` | entries `"<constraint>: <violating candidates, space-separated, possibly none>"`, or the single entry `"none"` |
| `scores` | `"<candidate>=<number>"`, exactly one per candidate |
| `selected` | one candidate |
| `ruling` | non-empty text: who ruled, when, and where it is recorded |
| `override` | optional, `"<candidate>: <reason>"` |
| `derivation` | `"CMP-###"`: this row's record is held by that live row |

**One record per partition.** The record is held once per partition, on one
row. Every other row of the partition carries only `derivation`. This keeps
one fact in one home, at the cost of a single one-hop resolution.

**Ranking.**

- A feasible candidate (one that no constraint names) ranks above every
  infeasible one.
- Within each group, candidates rank by score in the objective's direction.
- Equal scores tie.
- The recorded order matches if no candidate is listed before one that the
  recompute ranks strictly above it. A tie may be listed in either order.
- The selection is ranked first if no candidate ranks strictly above it.

## Trust

This section answers PROCESS.md §3 "When a guard is owed". The bound is §6:
supported registry authoring.

**Producers.**

- A person or model edits `docs/requirements/components.toml`, in a partition
  round or this row's backfill.
- `bootstrap.py` copies the template. Its `-000` row is vacuous.
- `migrate_carrier.py` maps the new keys through its stated inverse. A
  converted row without a record is reported.

**Failed writes.**

- Absent cells, partial cells, or a value outside the form.
- A stale record after a re-score.
- An explicit empty string, a nested table, or an unparseable file. The
  carrier already refuses all three loudly, with SystemExit.

**Consumers.** The one semantic reader is `trajectory_arch.component_findings`,
which `check_trajectory.py` runs over IF-263. These readers do not interpret
the record:

- `trace.py` and `coherence.py` read part-of, supersession and tag joins.
- `gen_components.py` reads names.
- `traj_parse.py` reads dashboard rows.
- `baseline_snapshot.py`, `acceptance_record.py` and `held_status.py` handle
  approval copies and approved-cell amendments. The new cells take the
  fail-safe approved class.
- `bootstrap.py` and `kitlib/bootstrap_manifest.py` copy the template.
- `trace_text.py` gives prose advisories on Name and Notes only.
- `spine_rules`, `intake`, `review_brief`, `agent_policy` and `trunk_step`
  hold only path or status references.

No new reader is added.

**The shared ruling.** The rules apply to each live row that is not `-000`.
Every bad state is a finding that names the row and the element, reported
WARN plain and ERROR under `--strict`. None passes silently.

- **Absent.** The row has neither record cells nor `derivation`: "no
  derivation record".
- **Incomplete.** One finding per missing element.
- **Malformed.** The finding names the cell and the cause. Malformed values
  include:
  - an unknown verb;
  - a non-numeric score, a score missing, or an extra score;
  - a duplicate candidate;
  - a `selected` or violator that is not a candidate;
  - an override outside its form, or one that names anything but `selected`;
  - a `derivation` that is dangling, points at the row itself, chains to
    another citing row, or sits beside record cells.
- **Inconsistent.**
  - The recorded order does not match the recompute.
  - The selection is not ranked first and there is no override.
  - An override is present although the selection is ranked first.

The ranking rules run only when a record has no incomplete or malformed
finding. A record that fails those checks has already failed closed. Findings
against a held record are reported once, on the holding row, naming the rows
that cite it.

The override silences only the not-ranked-first finding, and only when it
names `selected`. `[checks] components_check = false` still turns off the
whole pass, as it does today.

The machine checks form and arithmetic. Whether `ruling` reports a real human
act is for review and the approval route to judge.

## The operator's ruling (OI-130, ruled 2026-11-16)

OI-130 held the backfill and is ruled. The record of the ruling is
`docs/log.d/2026-11-16-operator-rules-oi130.md`.

- **Q1 (b).** The operator accepts P5 as the depth-0 partition on
  2026-11-16, a fresh ruling. `ruling` cites it.
- **Q2, as the re-score states it.** The numbers are the re-score's, taken on
  today's tree (`docs/plans/2026-11-11-oi130-rescore/README.md`, "Scores"),
  not August's. The record on CMP-006 carries:
  - `candidates = ["P5", "P3", "P4"]`;
  - `objective = "minimize cut"`;
  - `constraints = ["one-home-per-behaviour: P3 P4 P5"]`;
  - `scores = ["P5=140", "P3=152", "P4=235"]`;
  - `selected = "P5"`, with no `override`: P5 ranks first.
  P1 and P2 are not candidates of this record. The re-score did not score
  them, and says why.
- **The record's shape is SR-165 as written.** The operator: without it,
  traceability is incomplete.
- **Optionality.** The check is on by default and `[checks] components_check
  = false` turns it off, as "Trust" already says. No new setting is added.

## Done-when

- [x] The CMP schema carries the eight cells:
      - `kitlib/spine.py` `OFFSPINE_KEYS`;
      - the `spine_carrier` column map and the `migrate_carrier` inverse;
      - the template's `-000` row, which declares every key.
- [x] `component_findings` reports every state in "Trust". No second reader
      of the registry is added.
- [x] In-process cases in `tests/test_trajectory_arch.py` cover TC-166 (a)-(e)
      and each malformed and inconsistent state named above.
- [x] CMP-006 holds the record as OI-130's ruling of 2026-11-16 states it
      ("The operator's ruling", above). CMP-007, CMP-008 and CMP-009 cite
      it. The strict trace is clean.
- [x] TC-166's `evidence` names the test.
- [x] RESYNC entry: a forced migration. An adopter's live CMP rows need a
      record while `components_check` is on.
- [ ] Review bar: A+B (REVIEW-A plus an independent REVIEW-B). Open: on
      this maintenance branch the review is the branch's cross-family
      review, which runs after the build.

**One WI, landing order (S1).**

1. The schema commit adds no reader.
2. The backfill commit carries `intake.py snapshot --approves`, citing the
   OI-130 ruling, because the rows are Approved.
3. The tests-first commit puts the cases under `[bars] red_mark`.
4. The rules commit removes the marks.

Every commit stays strict-green.

## Architectural delta

- **New value domain:** the derivation record on CMP rows, owned by CMP-006.
- **New dependency:** `component_findings`' output, and with it the exit code
  of `check_trajectory --strict`, now also depends on those cells.
- **IF-263** already carries "spine/config files" in and "finding strings"
  out, so its contract is unchanged.
- **IF-039** still copies the template verbatim.
- **Unchanged:** no mode class is added (the existing dial and the vacuity
  rules stand), and no boundary, flow or component. A static check inside an
  existing pass is not a runtime flow.
- **Out of scope:** no refactor outside the row. `trace.py`'s separate
  component reader stays as it is.

## Critique dispositions

Round 1 (fresh Codex session, 2026-11-08): CHANGES-REQUESTED, four MAJORs and
one MINOR.

- **S1, the one-WI choice and the landing order: adopted.** "One WI, landing
  order (S1)" orders the commits so that "Every commit stays strict-green".
  The records precede the rules.
- **S2, Trust: adopted.** "Trust" names the producers, the failed writes and
  the consumers by path. It states one ruling: "Every bad state is a finding
  that names the row and the element ... None passes silently." It also states
  "The override silences only the not-ranked-first finding, and only when it
  names `selected`."
- **S3, a closed record form: adopted.** "The record form (S3: closed)" gives
  the eight cells, the per-partition home and the ranking rule, including the
  rule for constraints ("A feasible candidate ... ranks above every infeasible
  one") and for ties.
- **S4, the planning ruling: adopted as `planmode = "single"`.** The rules
  cover a closed but non-trivial input space.
- **S5, the architectural delta: adopted.** "Architectural delta" names the
  new domain, the new dependency and the existing contracts that suffice.
- **The critic's B4 condition is met.** The critic's question 3 asked for a
  stated hold if planning found a live component without an existing ruling.
  The evidence in Context shows that the ruling and the objective are
  ambiguous. "The owner-held step (B4)" holds the row through `needs`. Only
  the backfill needs the owner's answer.

Round 2 (fresh Codex session, confirming, 2026-11-08): APPROVE, no findings;
every adopted disposition confirmed.
