<!--
Contracts: IF-163 — the interface seam this file declares (process.md §8; row of
record in requirements/interfaces.toml).

Contract IF-163: the forward-only blackboard's HAND-AUTHORED bytes — everything
    outside the GENERATED STATUS marker pair — read as data by the kit's checks
    and by a resuming session; the block between the markers is its writer's
    own row. Markdown with `##` sections: `## Current State` is the section a
    stopping coordinator excerpts into its exit banner (the generated block
    rides inside that excerpt as the writer's bytes). Only what must happen
    NEXT belongs here — what already happened lives in log.md — so a work-item
    id recorded closed must not appear in the hand-authored prose, and a claim
    naming one there is refused; inside the generated block that rule stands
    down, because the generated frontier legitimately names queued ids.
-->

# Meta-Repo Status — Blackboard

The **working surface** for developing the kit itself — the same `status.md`
pattern the kit scaffolds downstream, self-applied. This file is
**forward-only**: only what must happen **next** lives here. Backward-looking
homes: [log.md](log.md) (sessions, verdicts, **Decisions**),
[open-items.html](open-items.html) (the generated **Open items** owner surface),
[docs/work/](work/) (the WI registry's active workspace — status = directory;
terminal rows live on under [archive/work/](archive/work/), one directory
deeper (OI-55 ruled (a), 2026-08-22) — same registry, same reader, dashboard
[`PROJECT_STATE.html`](../PROJECT_STATE.html)), and
[archive/](archive/README.md) (design history, with per-file dispositions), and
the folder map [docs/README.md](README.md) (what each `docs/` directory holds and
the seams it owns).

- **THE SPINE IS SIGNED AND THE BASELINE IS SEEDED** (sitting 3, 2026-08-20 —
  the owner's written approval; the record: [log.md](log.md) Decisions
  `2026-08-20a` + the Sittings row of the same date). `docs/archive/last_approved/`
  exists and drift detection is live: a post-sign amendment is a live edit the
  snapshot comparison reports, adjudicated per the declared approval level —
  never a silent ride. The D-9 step 7/8 follow-on (retire `Modified`, arm
  UNANCHORED as an ERROR, compute `Founded`) lands as the same-sequence
  mechanical act. Known-open, unrelated: the `trajectory` gating red (owned,
  first in the grind).
- **The frontier is OPEN and the grind runs in series** (owner directive
  2026-08-20): the generated block below carries the order. The second batch's
  closing review (internal Opus + cross-family Sol) is **taken and iterated** —
  all 22 worklist items dispositioned, the two CRITICALs proven against the
  reviewers' own executed attacks, record in
  [reviews/2026-08-21-program-grind-close/RESUME.md](reviews/2026-08-21-program-grind-close/RESUME.md).
  Five of the six queued briefs RULED (2026-08-21; record:
  [log.d/2026-08-21-owner-rulings-oi48-52.md](log.md#2026-08-21--four-of-the-six-queued-briefs-rule-in-one-owner-message-the-floor-question-is-answered-but-deliberately-not-yet-ruled);
  execution rows in the generated frontier below) — the largest being the
  **stage unification program**, whose six ruled slices are all BUILT per
  [plans/2026-08-21-stage-unification-plan.md](plans/2026-08-21-stage-unification-plan.md)
  (v1 FINAL, the owner's four answers in its §6): `docs/gate` and the whole bar
  axis are deleted, `docs/stage` is the one derived value, and the approval
  dial takes a rung. All six slices are now LANDED and green, and **the
  program close's adversarial round is TAKEN AND ITERATED** (2026-08-22,
  internal Opus + cross-family Sol): all 17 worklist items dispositioned, the
  three trust-bearing fixes proven against the reviewers' own executed attacks
  — including both Release-producer mutants, which the shipped pins PASSED and
  the rebuilt ones fail. Resume state:
  [reviews/2026-08-22-wi498-program-close/RESUME.md](reviews/2026-08-22-wi498-program-close/RESUME.md).
  The program row is **CLOSED COMPLETE** (2026-08-22): every close-owed item
  is dispositioned, the signed figures were independently reproduced
  (2831/14 exact at the approval commit), and the remainders all carry rows
  in the frontier below (the cell repairs + cross check, the approval-brief
  split, and the four open lanes). The spine's surfaced set is
  APPROVED and the baseline is CURRENT (2026-08-23, the owner's in-session
  act — the dated brief he signed from is
  [ratify/2026-08-23-spine-approval.md](ratify/2026-08-23-spine-approval.md)):
  the drift is at **zero rows** and the open-items surface at **zero pending
  decisions**. The component registry is APPROVED too (2026-08-22, the
  owner's ruling after reading the four rows in full), and the ladder reads
  `DevStg-LLReqs`: what holds it there is the orphan debt — **one**
  undecomposed SR remaining
  (`SR-181`; no TC-less LLR remains), assigned (owner-directed
  2026-08-22) and riding fold-in notes on the queued rows that own their
  subjects, so the grind pays the debt as a side effect and the ladder climbs
  as the mints approve — each mint lands `Drafted`, so the ladder itself has
  not moved. (The CI pair — the hosted bar
  per trigger and the hosted verdict — was the first fold-in paid, minting
  three LLR/TC pairs beside the test-evidence carrier.)
  **THE NINETEEN ARE APPROVED AND THE BASELINE IS RE-SEEDED** (2026-08-24,
  the owner's in-session act, from the corrected brief the three preceding
  fixes produced — the dated copy he signed from is
  [ratify/2026-08-24-spine-approval.md](ratify/2026-08-24-spine-approval.md);
  record: [log.d/2026-08-24-oi62-rule-and-spine-approval.md](log.md#2026-08-24--oi-62-ruled-e-and-the-nineteen-are-approved-from-the-corrected-brief)):
  `docs/stage`'s draft count was taken to **zero**, the re-attest window closed
  (`trace.py --approve modified --check` exit 0), and **phase 4 climbed back
  to `DevStg-Impl`** — the reopened-phase warning its minted drafts held open
  is cleared. The ladder's live rung stays `DevStg-LLReqs` on phase 5. Still
  owner-owed from the wording round that lightened the brief: the two banked
  findings about `Approved` text nobody may edit
  ([reviews/2026-08-24-draft-wording-round/RESUME.md](reviews/2026-08-24-draft-wording-round/RESUME.md)).
  Environment, RE-MEASURED 2026-08-25: **41 GB free on C:** — the disk pressure
  that forced the batched/cleaned-basetemp form is gone. Measured in the other
  direction on the same box, and worth knowing before reaching for the
  workaround: pointing `--basetemp` at D: roughly **doubles** the smoke tier's
  wall time (26 s on the declared command, 60 s with the redirect), so redirect
  it only when C: is genuinely short.
- **`OI-68` AND `OI-69` ARE RULED (2026-08-30)** — record
  [log.d/2026-08-30-owner-rulings-oi68-oi69.md](log.md#2026-08-30--the-owner-rules-oi-68-1c-a-sloc-based-line-ratchet--2a--3a--4a-and-oi-69-a1--b1--c2--d1--e1-once-the-dial-is-on-five-rows-filed-with-their-edges).
  `OI-68` (the complexity sensor): (1c) BOTH sensors stay armed and the
  module-size line ratchet is RE-BASED to SLOC — non-blank, non-comment,
  non-docstring lines, one definition shared with the sensor — (2a) the sensor
  censuses `tests/` too, (3a) armed here, (4a) the prototype's conventions at
  15; plan of record
  [plans/2026-08-29-complexity-sensor-plan.md](plans/2026-08-29-complexity-sensor-plan.md)
  (its phase 2 is now arm + re-base, nothing deleted; its byte arithmetic is a
  day stale — measure, don't trust). `OI-69` (adjudicator session retention):
  (a1) a retained transcript is not an actor, (b1) `reset_on_same_artifact =
  false` with the fork hardening banked, (c2) keep-warm pings THROUGH the
  blackout (≈ $1.20 a window against a ≈ $3 rewrite), (d1)
  `process.toml [adjudicator]`, (e1) dedicated CLI homes once the dial is on;
  plan of record
  [plans/2026-08-29-adjudicator-session-retention-plan.md](plans/2026-08-29-adjudicator-session-retention-plan.md).
  **RESUME HERE:** the generated frontier below names the queued rows and
  their order — the sensor report-only (strong, spine) → arm-and-re-base
  (soft-edged to the debt owner) → ship; the adjudicator telemetry-first row
  → the retention layer → its on-box verification; and the knowledge-pack
  review's byte-paid edits, unblocked by anything. Enabling the dial is the
  owner's edit of one number afterwards. **Before the grind starts: the
  bar** — the full suite's floor is one 304 s test and nine 60–90 s dispatch
  lanes (measured 2026-08-30,
  [log.d/2026-08-30-oi67-docs-pass-and-bar-timing.md](log.md#2026-08-30--docs-the-oi-67-programs-shipped-and-reference-docs-brought-level-with-the-tree-and-the-bars-wall-time-measured-piece-by-piece));
  a row for it when the work is ready to start, ideally driven by the sensor's
  first census.
- **THE INTERFACE ROW IS BEING RESHAPED — `OI-67` RULED (a), 2026-08-29.**
  One row is one owner, its consumers and a typed statement of the
  information; `provider`, `req_refs` and the prose `contract` leave the row
  and the module header is the definition's only home. The plan of record
  is [plans/2026-08-29-if-row-shape-plan.md](plans/2026-08-29-if-row-shape-plan.md)
  (six slices, sequenced by `needs`; the rows are in `docs/work/queued/` and
  the generated frontier below names them — **slice 1 is LANDED**, record
  [log.d/2026-08-29-wi528-if-row-shape.md](log.md#2026-08-29--wi-528-the-interface-row-shape-in-code-oi-67-slice-1):
  the row reads `owner` + `requestors`|`consumers` + `channel` + `data`, the
  kit's registry is converted, and the far side names the direction — the
  owner's in-session addition; **slice 5 is LANDED too**, out of plan order so
  the shipped `PROCESS.md` §8 and templates stopped describing cells the code
  no longer reads — record
  [log.d/2026-08-29-wi532-if-row-shape-shipped.md](log.md#2026-08-29--wi-532-the-interface-row-shape-ships-to-adopters-oi-67-slice-5),
  converter `migrate_carrier.py --if-shape`; **slice 2 is LANDED** — a
  registry, config or hook file declares through its comment header, the two
  git hooks declare, and the reverse check is owner-exact, record
  [log.d/2026-08-29-wi529-header-non-python.md](log.md#2026-08-29--wi-529-the-contract-header-reaches-every-owner-oi-67-slice-2);
  the 67 owner-exact warnings it surfaces were slice 3's worklist; **slice 3 is
  LANDED** — 132 of 136 definitions stated beside their owners by a four-worker
  round, record
  [log.d/2026-08-29-wi530-cell-pass.md](log.md#2026-08-29--wi-530-the-cell-pass-on-the-new-shape-oi-67-slice-3),
  the round itself at
  [reviews/2026-08-29-oi67-slice3/](reviews/2026-08-29-oi67-slice3/README.md)).
  **slice 4 is LANDED** — one row, one direction, one kind: twenty rows
  minted (`IF-145`–`IF-164`), two duplicate pairs collapsed, 136 → 154 rows,
  the reference at 73 sources / 150 seams / 150 stated, by a three-worker
  round recorded at
  [reviews/2026-08-29-oi67-slice4/](reviews/2026-08-29-oi67-slice4/README.md),
  record [log.d/2026-08-29-wi531-if-row-split.md](log.md#2026-08-29--wi-531-the-split--one-row-one-direction-one-kind-oi-67-slice-4).
  **slice 6 is LANDED — THE PROGRAM'S SIX SLICES ARE ALL BUILT:** the gate is
  armed (a declared seam with no body, an external-owned row no far-side
  module states, a stray declaration, and any retired cell are `--strict`
  findings), every one of the 154 rows is stated (reference 74 / 154 / 154),
  the CSV loaders read through one comment-skipping reader so `IF-031`'s
  owner declares in its own header, and the three `external:`-owned rows are
  stated by their far side — record
  [log.d/2026-08-29-wi533-arm-the-gate.md](log.md#2026-08-29--wi-533-the-gate-is-armed-oi-67-slice-6).
  **Slice 6's cross-family round RAN** (gpt-5.6-sol, eleven findings, nine
  folded at the root — the gate's grammar arm, the no-in-tree-endpoint rule,
  presence-based retired cells, four raw CSV readers, the blank preamble line
  — record [log.d/2026-08-29-oi67-slice6-round.md](log.md#2026-08-29--review-the-oi-67-slice-6-cross-family-round--eleven-findings-nine-folded-at-the-root),
  dispositions [reviews/2026-08-29-oi67-slice6/](reviews/2026-08-29-oi67-slice6/README.md)),
  and **the arms the split surfaced are DONE** — nine rows (`IF-165`–`IF-173`),
  154 → 163, the reference at 74 / 163 / 163, `gen_arch_map` running every
  target it is named — record
  [log.d/2026-08-29-wi534-if-arms.md](log.md#2026-08-29--wi-534-the-arms-the-split-surfaced--nine-rows-minted-and-stated-oi-67-follow-on).
  **The owner accepted decisions 4.1, 6.2, 6.7 and 6.8** — record
  [log.d/2026-08-29-owner-rulings-oi67-decisions.md](log.md#2026-08-29--the-owner-accepts-decisions-41-62-67-and-68-of-the-oi-67-slices--recorded-nothing-changes-in-code);
  the first session's decisions file (below) is still unread. **RESUME
  HERE:** (1) the smoke budget read **40.7 s → within** on 2026-08-30 once
  the other sessions went quiet, after two days of OVER readings (88–180 s)
  on a box they held at 50–90 %; the budget is untouched and the quiet number
  is on record in
  [log.d/2026-08-30-owner-rulings-oi68-oi69.md](log.md#2026-08-30--the-owner-rules-oi-68-1c-a-sloc-based-line-ratchet--2a--3a--4a-and-oi-69-a1--b1--c2--d1--e1-once-the-dial-is-on-five-rows-filed-with-their-edges);
  (2) left standing,
  each recorded in the two fragments:
  the three tracked fragments opening with `#`/`###` (the trunk lane's),
  `TC-161`'s approved prose naming `IF-127` (the owner's), the seven
  `_`-prefixed names crossing `IF-173` (a rename to file), the ten seam-TC
  allowlist entries the arms added past the seed (the burn-down), and a
  repo-wide `ruff check tests/` red on two pre-existing F401s. The ruling
  record is
  [log.d/2026-08-29-oi67-ruled-a.md](log.md#2026-08-29--the-owner-rules-oi-67-a-one-row-one-direction-one-kind--the-cells-go). The
  contract header from `OI-66` stays and becomes load-bearing: a module states each contract beside the code as a
  `Contract IF-###:` block, and `docs/interface-reference.md` harvests them
  under a freshness gate that sits on the pre-commit floor. Records:
  [log.d/2026-08-29-wi527-contract-header.md](log.md#2026-08-29--wi-527-the-component-side-contract-header-built-and-adversarially-reviewed),
  and the decisions this session took unconsulted are filed for review at
  [decisions-for-review-2026-08-29.md](decisions-for-review-2026-08-29.md);
  slices 4 and 6's are at
  [decisions-for-review-2026-08-29-slices-4-6.md](decisions-for-review-2026-08-29-slices-4-6.md).
  - **THE 71-ROW CELL PASS IS SUPERSEDED by the plan's slice 3**, which
    spends the same authoring on the new shape. **Two rows are done as proof
    the pipeline works end to end** (`IF-013`, `IF-144`); the reference reads
    **137 declarations over 134 seams, 2 stated**. Measured for the ruling: 14
    rows are two-way, 35 bundle several kinds, 31 are owned by something the
    `*.py` scanner cannot see — slice 2 widens the scanner before slice 3
    authors into it.
  - **The marker grammar tightened, and that is the adopter-visible half.** It
    must OPEN its line and parse as an id list — line-start alone still leaked
    (`Contracts: not IF-080; an example` declared IF-080). Both lossy forms are
    reported by name so no repo loses a seam in silence; 0 findings here, and
    the detector was proved to fire by planting one.
  - **A false green closed for the whole kit:** a `[generated]` row naming an
    absent FILE now fails `staged-divergence`. Every freshness step is vacuous
    on an absent target, so deleting a declared artifact disarmed its own gate.
    Prefix rows stay exempt — `docs/okf/` is absent by dial.
  - **Left broken on purpose, both recorded:** `IF-134`/`IF-135` have no
    declaring module because the git hooks are extensionless and a `*.py` scan
    cannot see them; and the reverse check is id-global, so an id declared on
    the WRONG module still passes.
  `OI-61`'s (c) stays deferred and was NOT re-raised.
- **The interface tier's end-state schema is LANDED.**
  A seam row now reads `provider -> consumers`: no direction
  column, no endpoint cell restating what the row's owner already derives, and
  the derivations held by test rather than by claim
  ([test_seam_resolution.py](../tests/test_seam_resolution.py)). Two follow-ons
  are OPEN and neither is owed by the lane that shipped this: **the twelve
  requirement-owned provider-side rows** wait on an owner-informed re-point, one
  seam at a time, fed by
  [plans/2026-08-23-sr-owned-provides-report.md](plans/2026-08-23-sr-owned-provides-report.md)
  — `trace.py`'s Provider derivability advisory asks for each cell back as its
  owner moves to the design tier; and **the 21 published-medium rows state no
  provider**, because none was ever recorded, so recording the medium each row's
  `contract` names is authoring per row rather than a rename. Adopters take the
  migration through [RESYNC_PACK.md](../project-trajectory/RESYNC_PACK.md)'s
  entry, which classifies the four `Consumes` shapes before any cell is touched.
- **The snapshot block is CLEARED and STAYS clear** (2026-08-23, re-seeded
  again 2026-08-24): `intake.py snapshot` does not refuse, so a session can
  record an approval by refreshing it. The standing rule survives the closes
  around it: a `Drafted` row is approved on its own merits, from the rendered
  brief — never bulk-flipped to tidy a surface.
- **The `wi484-concern-refs-component-view` lane is OPEN with slice 5 landed**
  (2026-08-23): phases 0, 1, **2**, 3 and 5 are done — the component view is
  GENERATED (`components.derived.toml`, freshness-gated by the `component-view`
  step), `detail_doc` is retired, the amend-without-flip guard carries a
  `Hat-Refs` arm (warn-first, `--staged`), and phase 2's writer is now the
  `spine-authoring` skill's own rule at SR §2(c2) + LLR §3 (the fork was ruled
  for the minting tier; the Plan-WI brief mints no spine row, so it was declined
  as a home). The row's spec Context lists what is still owed. **What remains
  needs the owner or a mechanism, not a next slice:** phase 2's duplication (17
  rows state the attribution twice, in an approved `Rationale` cell) is
  owner-adjacent and deliberately unTAKEN.
  **Phase 4's mechanism blocker is RESOLVED (2026-08-23):** `hats.py`
  now declares an `OPTIONAL_KEYS` concept (`knowledge`, validated when
  present, absent everywhere and fine), so the roster key can be added
  without becoming mandatory on all 16 rows. What phase 4 still awaits is the
  owner's own act, not a next slice: filling `knowledge` values into
  `hats.toml`, which is declared owner text and was deliberately left empty.
- **The `wi508-architectural-remap` lane is OPEN with slices 1–4 landed**
  (2026-08-25). The framing act is done: the row was re-validated against
  the amended `SR-163` — the sole amendment is the `MAINTAINER` lens, and
  every normative cell is byte-identical to the text the row was minted
  against — and against the four open items that reached its SpecRef file
  since, none of which retask it. `SR-163` is now DECOMPOSED:
  `LLR-203`/`TC-199` (the shipped-file inventory, its declared exclusions,
  and the purpose reference it does not carry) and `LLR-204`/`TC-200` (the
  `Implements:` grammar and the declared warn-to-gate dial, running the
  OTHER direction). The orphan debt is therefore down to `SR-181` alone,
  and **four `Drafted` rows are back on the approval surface** — the
  ordinary consequence of a mint, moving no rung; the re-attestation brief
  carries one section for them and blessing it is the owner's act.
  **The blind derivation has RUN** (slice 2), on two axes, from a five-file
  input set with the design tier, the component/interface registries and the
  source tree held out — brief recorded before the answers at
  [plans/2026-08-25-blind-minimal-map-brief.md](plans/2026-08-25-blind-minimal-map-brief.md),
  both returns and the measured agreement at
  [plans/2026-08-25-blind-minimal-map-derivation.md](plans/2026-08-25-blind-minimal-map-derivation.md).
  24 modules against 23, **97.2%** pair agreement, 84% placed identically —
  and the result neither axis could reach alone: **both invented the same
  module owning ZERO requirements** (the finding/severity/exit contract), so
  the corpus is missing a row that eleven-to-thirteen others each restate.
  **That is a missing requirement, not module work.** Blindness was NOT total
  and both teams disclosed it: the harness injects this repo's own instruction
  file into a subagent's context, so a future run of this instrument must strip
  the harness context and not only the input set.
  **The alignment pass has RUN** (slices 3–4; record:
  [plans/2026-08-25-remap-alignment.md](plans/2026-08-25-remap-alignment.md)),
  and it spent most of its effort REFUTING the derived maps rather than executing
  them. The live map is ~3.5x finer (83 named modules against 24 and 23), so the
  test applied to every divergence is *calls, not lines*: does each home
  re-implement the behaviour, or do they all call one home? Twelve dispositions —
  **ten keep-with-recorded-reason, two keep-with-the-reason-absent, zero
  consolidations** — because the twelve are exactly where the two blind maps
  disagreed. Three consolidation families were dissolved by measurement (38
  modules already import one declaration stage; merging the measurement
  comparators would put `D-7` one refactor from being undone; each freshness
  `--check` is three lines over its own renderer). **One survived and the
  rationale made it smaller, and the row it was filed as has since closed** —
  the allow-file parse-honesty arm reached the three declared-exception
  readers that dropped a malformed line silently, each keeping its own
  grammar, no parser merged. Closed: see
  `docs/log.d/2026-08-25-wi519-allow-file-parse-honesty.md`.
  Banked, not built: the duplication
  census reads 0/0/0 because it hashes function BODIES, so structural repetition
  is invisible to it by construction.
  **THE SURVEY IS COMPLETE** (slice 5): all **18** dispersion families carry a
  disposition — one consolidate, twelve keep, one partly upheld — and each keep
  declares whether it rests on a mechanical shared-stage test or a read
  rationale. Three derived-map merges were REFUSED with cause (the launcher
  split is argued in `SR-160`'s own text and the shared piece would need a shell
  library the kit deliberately does not ship; both converters are one-shot tools
  whose migrations have already run; the manifest's shared signal already has one
  home). **One consolidation row was filed and has since closed** (`priority 1`,
  `high-risk`): the hook scanner and the transcript redactor had compiled two
  credential-class lists independently, and **four of five driven samples
  disagreed, both ways** — a PEM private-key block was refused at the commit
  hook and passed UNREDACTED into a committed transcript, so the durable
  artifact was less protected than the ephemeral one. Closed: see `docs/log.d/
  2026-08-25-wi520-secret-class-vocabulary.md`.
  **THE INHERITED DEBT NOW HAS AN OWNER THAT OUTLIVES THE PROGRAM: `WI-521`.**
  The module-size ratchet's pointer MOVED off the remap row onto it — a
  close-time re-point is a promise where a filed row is a fact, and the remap is
  a consolidation program while that ratchet measures size, which is
  decomposition. M-06's four test monoliths land there too, explicitly unbound
  from a ride-along rule that failed to deliver across two programs; the
  test-tree sensor gap rides with them, carried but not executed (its axis is
  under an unruled owner question). **The remap row's close now has nothing to
  re-point.**
  **`OI-64` IS RULED (b) AND EXECUTED — the remap row's owner-owed ruling is
  discharged**; what remains on it is the blessing of the four `Drafted` rows.
  The reporting protocol is now stated once as **`IF-144`**: a
  finding names its location, carries a severity from a closed four-value set,
  never lets an advisory reach the exit code, promotes to failure only under a
  declared strict flag, and exits zero naming the absence when an optional input
  is missing. No existing row was edited — (b) is state-and-sweep-nothing.
  - **The shape resolved on the evidence, not by a second ruling.** It read at
    first as a blocker (one `provider` or one `component` per row, against
    fourteen providers splitting five and five across `CMP-006`/`CMP-007`), but
    that was the wrong axis: the protocol is what the harness presents at its
    **package boundary**, and all ten restating rows cite **`B-05` unanimously**.
    28 rows already use that shape.
  - **Two clauses deliberately absent, recorded on the row.** *Every degrade is
    named* is not stated, because `SR-181`'s acceptance permits a silent degrade
    while `SN-008` forbids one — it would red an `Approved` row on day one. And
    the closed set is four *dispositions*, not the twelve tokens the checkers
    spell them with.
  - **The row honours the rules it states.** First draft tripped four of the
    registry's own advisories (732 characters against a 500 ceiling, an argument
    in `contract`, a date stamp in `notes`); thinned to **466** with the argument
    moved to `rationale`.
  Three corrections from the 2026-08-28 review stand on the row (record:
  [reviews/2026-08-28-oi64-oi65-sol-round/](reviews/2026-08-28-oi64-oi65-sol-round/)):
  the restating rows number **ten, not thirteen**; at most **six** clauses are
  removable; and `SR-158` does **not** declare itself unsatisfied. Option (a)'s
  sweep stays unruled and is still not executable — an SR row has **no field for
  citing an interface**.
- **The `wi521-decomposition-debt-owner` lane is OPEN with slice 1 landed**
  (2026-08-25; record:
  [log.d/2026-08-25-wi521-slice1-acceptance-record.md](log.md#2026-08-25--wi-521-slice-1-the-acceptance-record-leaves-the-checker)).
  The acceptance record left the checker: 677 lines moved VERBATIM into
  `project-trajectory/scripts/acceptance_record.py`, `check_trajectory.py`
  re-stamped **4,963 → 4,327**, every name re-exported so no caller moved, the
  CLI byte-identical across nine driven paths and 56 API probes, and `intake.py`
  no longer importing a ~5,000-line validator at all. **Before trusting the
  fusion table this row inherited, read the re-derivation that corrects it:** 13
  of the 71 SRs have a TIED live module and `agent_loop`'s head position rests
  on one of them, so the table says WHICH modules fuse obligations, not in what
  order. **The row does not close** — it is the standing debt owner and the
  ratchet still points at it. **Slice 2 took M-06's largest monolith
  standalone** (record:
  [log.d/2026-08-25-wi521-slice2-integrate-test-split.md](log.md#2026-08-25--wi-521-slice-2-m-06s-largest-monolith-split-standalone)):
  `tests/test_integrate.py` 3,520 lines → four modules along its OWN seven
  banner sections plus `tests/integrate_fixtures.py`, proven by node-id SET
  equality against the monolith (133 ids, diff empty) rather than by a green,
  and with smoke membership unmoved at 1,369 because all three new modules were
  re-tiered into `conftest.SLOW_MODULES`. Next, in that order: the rest of
  `check_trajectory`, then `agent_common` / `bootstrap` / `agent_loop`, then
  M-06's remaining three (`test_trace` 2,099, `test_trajectory_arch` 1,993,
  `test_agent_loop` 1,640). The test-tree sensor gap stays CARRIED, its axis
  still under an unruled owner question.
- **Standing owner acts the loop will not make:** merge-to-main + push for
  `dualplan-routing-fix`, `guardrails-fable-method`, `ConcurrencyTrainRewrite`
  and this branch (`push = "human"`). Known residue, kept deliberately: the
  `wi416-parked-handback-contract` branch holds a 271-line pre-ruling draft
  that exists nowhere else (its rows are disposed; the handback ruling
  superseded it) — delete only after deciding the draft is not wanted.
- **STARTING COLD? Read in this order:** this block → the `2026-08-22`
  fragments in [log.d/](log.d/) (the rulings, the program close, the
  per-WI sessions) → the generated frontier below, then grind it IN SERIES
  (one worker per row, routed by BuildTier; full-suite runs FOREGROUND with
  an explicit timeout — a backgrounded run dies when the session's turn
  ends, the lesson every interrupted worker of this arc re-learned; use a
  `--basetemp` on D: while C: stays low). The standing constraint under all
  of it: **the depth-0 frame is LOCKED and APPROVED** — **4 entities ·
  4 crossings · 3 relationships**, cut-row ids spent and watermark-held;
  the repository is the system, the template is the deliverable. The
  2026-08-15 interface-rework provisional state is ruled (`OI-49` (b),
  2026-08-21): live cells approve in bulk, the named exception reads have a
  recommendation each in
  [`docs/plans/2026-08-22-interface-exception-dossier.md`](plans/2026-08-22-interface-exception-dossier.md)
  awaiting the owner's approving Status-change commit, `IF-097`/`IF-080`
  closed by the record.
- **Unfiled follow-ups** (no ids yet, so listed as topics): the stage-ladder
  program's deferred codex review round; the SN-036 per-decomposition coverage
  record (re-derive it — the basis line now reads `uncovered=0`); the two
  findings in the archived
  [2026-08-01 handoff §6](archive/history/handoff-2026-08-01.md); and the three
  unruled residues + §8 dead-symbol table in
  [spine-restructure-2026-08-08.md](spine-restructure-2026-08-08.md) (its §7
  items 2/4/5 need a destination before that file can archive); and
  PROCESS.md §4 still describing the approval dial as "an ordinal `0`–`4`" —
  staleness predating the vocabulary campaign (the rung-string rekey
  superseded it), surfaced 2026-08-23 and left for its own row.
- **Conventions:** spec-of-record [specs/README.md](specs/README.md) · rubrics
  [rubrics/README.md](rubrics/README.md) · partial-close reports
  [handbacks/](handbacks/README.md).

## Current State

<!-- BEGIN GENERATED STATUS -->
_GENERATED by `python project-trajectory/scripts/gen_trajectory.py --status` — do not hand-edit; cite the spine registries + `docs/stage`, not this rendering (the forward-only intent below is hand-authored)._

- **In stage:** **DevStg-LLReqs** (stage 5 of 8, LLR definition in work) (per-phase `1=DevStg-Impl;3=DevStg-Impl;4=DevStg-Impl;5=DevStg-LLReqs`, derived current **phase=5**) — the rung this repo is IN, derived over its settled spine. [`derive_stage.py`](../project-trajectory/scripts/derive_stage.py) derives it, recorded in [`docs/stage`](stage).
- **Spine:** **SN=27 SR=75 LLR=187 TC=184** (6 drafts) · 163 seams · 4 components.
- **Ready frontier** _(dependency-ready WIs in build order — generated from the scheduler; a closed WI drops out automatically, so this list is never stale and never names a `done` id):_
  - **WI-537** `P2` — check_complexity.py: a stdlib cognitive-complexity and SLOC census with a TSV baseline, r…
  - **WI-484** `P2` — Concern/hat references on SR and LLR rows and the generated component view: effective set…
  - **WI-508** `P2` — The architectural remapping program: blind minimal-map re-derivation, divergences filed a…
  - **WI-535** `P2` — Adjudicator telemetry first, dial off: session id and occupancy / window / percent per fa…
  - **WI-521** `P2` — The decomposition debt owner: four wide modules, M-06's four test monoliths, and no senso…
  - **WI-536** `P2` — Agent-brief and scope: the knowledge-pack review's six byte-paid edits and two kit findin…
<!-- END GENERATED STATUS -->

- **Bar (per commit)** and the **standing rules** (claim refusal on prose ids,
  never sanction a check to green a step, signed-claim/one-machine humility,
  line-ending hygiene, claiming through the integrator): the `session-protocol`
  skill §2–§3, which is their home — relocated out of this forward-only surface
  at the 2026-08-20 docs sweep. Additionally: run `check_trajectory.py --strict` directly and
  unfiltered before claiming anything done, since the DEFAULTED pre-commit floor
  stays warn-first by design and is never the strict bar. Probe providers before
  planning a critique dispatch, and route by PROVIDER, not gateway.
- **External follow-up** *(not this repo's work)*: guardrails content
  enrichment lives in `TheColliny/FableClaudeMDForOpus` (vendored downstream).
- **Process (kit source):** [PROCESS.md](../project-trajectory/PROCESS.md) ·
  [PROCESS_OPTIONS.md](../project-trajectory/PROCESS_OPTIONS.md) · working rules
  [CLAUDE.md](../CLAUDE.md) + the `session-protocol` skill · still-owed lock
  items [repo-lock.md](repo-lock.md) (§1 now defers to the generated surfaces).

## Scope

- **Goal:** keep the kit **maintainable and trustworthy** — the
  `PROJECT-VISION:` tag opening [README.md](../README.md) is canonical.
- **Supported platforms:** Windows + POSIX; kit scripts stdlib-only on
  Python 3.11+.
- **Non-goals (self-application boundary):** no product **launch** — the
  kit's "product" is `project-trajectory/` + `tests/`, a meta-repo has no
  product to launch, and an actions-menu launcher is in scope; no scaffolded
  `docs/process.md` (the masters live in `project-trajectory/`).
