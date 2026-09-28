+++
id = "WI-615"
title = "Doctrine sitting: the guard and fan-out rules, the reviewer and worker briefs, children coverage, OI-76's trailer text, the knowledge-pack edits, then the terminology pass"
workstream = "process"
specref = ""
buildtier = "medium"
priority = 3
safety_class = "ordinary"
needs = []
supersedes = "WI-609;WI-613;WI-614;WI-556;WI-668;WI-610;WI-536"
+++

## Deliverable

Built by one builder in ten commits with three Codex Sol rounds (wave-5
arbitration rulings 33 to 36), SOUND at bccfae71. Seven of the eight parts
are built. Part 7 (WI-610) is routed to the owner as OI-95.

- **WI-609:** the reviewer brief names each work item's own spec under
  `docs/work/` (and its `specref` target) as the spec of record. No prompt
  says `docs/specs` (grep, and a test).
- **WI-613:** PROCESS.md §3 "When a guard is owed", with the reviewer and
  worker briefs linking to it rather than restating it.
- **WI-614:** PROCESS.md §6's fan-out paragraph: down-tier and peer-tier
  kept, tiers never models, and no fan-out from review, critique,
  design-check or adjudication sessions. The rule has one home (a test).
- **WI-556:** the spine-authoring skill's children-coverage rule, citing
  OI-72 as the kit repository's ruling of record, in all three copies.
- **WI-668:** the worker brief's sent body cites no meta-repo record, its
  close bar points at `check.py`'s step table and `[tiers]`, and the
  session-protocol skill's full-suite order is settled.
- **WI-536:** the knowledge-pack edits. The partial-search bullet is in
  AGENTS.template.md. There is a new `subagent-brief` skill, the receipt
  doctrine is in spine-authoring §6, and the build-tier discriminator is in
  PROCESS_OPTIONS. `gen_skills_index --check` has a description floor under
  a labelled derived SR-224 (LLR-281, TC-291, IF-254 as its exit contract).
  `guardrails_core` selects a per-model payload under a derived SR-223
  (LLR-280, TC-290, IF-253). Whole-directory skill materialization and
  `delivery_inventory` share `bootstrap.skill_copies` (LLR-279, TC-289; B5
  fixed).
- **The terminology pass**, last: PROCESS.md §2's glossary lines (including
  that "expectation" inside a need is ordinary English). Kit prose, the
  dashboard card and trace.py's report table say *system specification* and
  *design expectation*. The OKF export's concept types stay: they are a data
  vocabulary pinned by approved TC-105. Also folded in: PROCESS.md §4's
  absolutes rule now spans needs, system specifications and design
  expectations (never test cases), with one waiver grammar.

Byte budgets: AGENTS.template.md 9,996 of 10,000 (re-stamped), CLAUDE.md
unchanged, byte-budget-guard 4,496 of 5,000, PROCESS.md 92,484 (+2,208,
watched), PROCESS_OPTIONS.md 193,432 (+619, watched).

Not built, routed: **part 7 (WI-610, OI-76's trailer text) is OI-95**, an
owner question with a typed brief; the recommendation is (a), amend the
ruling's wording to the code. Recorded, not edited: approved registry rows
that still say "system requirement" (SN-037, SN-038; SR-162, SR-163,
SR-193, SR-194, SR-196, SR-201, SR-205, SR-206, SR-212, SR-217, SR-219;
TC-105's method, which names the OKF types). `gen_skills_index.py --check`
without `--skills` silently checks nothing in this repository.

## Context

**Consolidated 2026-09-27** (the coordinator's queue consolidation, the owner's direction in `docs/handoff-2026-09-27-coordinator.md`): this row absorbs WI-609 (Point the reviewer brief at the work item's own spec, not the empty docs/specs folder (review pack C5)), WI-613 (State when a guard is owed in PROCESS.md, and link it from the reviewer and builder prompts (S15)), WI-614 (State the fan-out rules in PROCESS.md: peer-tier kept, tiers not models, never from review roles (S12)), WI-556 (Spine-authoring doctrine: the children-coverage rule stated as trust-based prose (OI-72 ride-along)), WI-668 (Make the shipped worker brief adopter-true: cite no meta-repo record in the sent body, point the close bar at its one home, and settle the skill's residual full-suite order), WI-610 (Reconcile OI-76's ruling text with where the code puts the Review-Verdict trailer (review pack C6)), WI-536 (Agent-brief and scope: the knowledge-pack review's six byte-paid edits and two kit findings). Every part edits byte-budgeted doctrine (PROCESS.md, AGENTS.template.md, the shipped prompts, the spine-authoring and session-protocol skills), so they share one byte-budget sitting and one dogfood-sync check instead of eight serial fights over the same caps. The absorbed specs are archived under `docs/archive/work/restructured/` with their scope text untouched: read each one's Context there before building its part. Their Done-when blocks are quoted below under their old ids and remain this row's spec; decompose, don't paraphrase.

Order (the 2026-09-26 handoff's, extended): WI-609, WI-613 and WI-614 first, then WI-556, WI-668, WI-536 and WI-610, and the terminology pass (this row's own scope) LAST, so it sweeps the prose the others add. WI-610 needs the owner's choice: surface it as an open item with both options and a recommendation unless the owner has ruled by then. Report the byte-budget-guard delta once per touched capped doc, at close.

Ruled by the owner: Q9 (prose name *system specification*, 2026-09-24) and
the sister plan's S2 (LLR -> *design expectation*, 2026-09-23; flag closed
2026-09-24). This is the assumption-tier plan's package T.

One prose pass over the kit's docs, prompts and dashboard labels, plus one
PROCESS.md glossary line each: `SR-###` rows are system specifications and
`LLR-###` rows are design expectations (the prefixes are historical), and
"expectation" inside a need row is ordinary English, not the tier. No old log
is edited. Id prefixes and rung names (`DevStg-LLReqs`) are unchanged here; the
prefix rename is a separate deferred item, taken last. `RESYNC_PACK.md` §4 is
the concept-rename table, and `check_vocab` may need the new words.

Folded 2026-09-28 (WI-616's landing, the fifth coordinator session): WI-616 extended the absolutes check from acceptance criteria to the whole matrix (needs, SRs and LLRs, never TCs; `project-trajectory/scripts/absolute_terms.py`, the spine-authoring skill's §2(d2) closed-domain question), but PROCESS.md §4 still states the absolutes rule for acceptance criteria only. WI-616 left it alone so as not to collide with this row's PROCESS.md sitting. Restate §4's rule to the matrix the check now covers, with its one waiver grammar (`recorded waiver:`), inside this sitting's byte budget.

## Done-when

- PROCESS.md §4 states the absolutes rule over the matrix `absolute_terms.py` checks (needs, SRs, LLRs; never TCs), not acceptance criteria alone.
- PROCESS.md carries the glossary lines, including the ordinary-"expectation"
  note.
- Kit docs, prompts and dashboard labels call SR rows system specifications and
  LLR rows design expectations; grep evidence names what still says otherwise,
  and why (ids, rung names, quotations).
- No file under `docs/log.md`, `docs/log.d/` or `docs/archive/` is edited.
- `RESYNC_PACK.md` carries the rename where adopters or `check_vocab` need it;
  byte budgets and the dogfood sync hold.
- The byte-budget-guard report for every capped or watched doc touched is quoted once, at close, and the dogfood sync test stays green.
- Every absorbed row's Done-when quoted below holds; their per-row commit-bar lines are this row's one bar.

### From WI-609 (Done-when, verbatim)

- The reviewer brief names the work item's own spec file (and its `specref`,
  where that points elsewhere) as the spec of record.
- No shipped prompt still points at `docs/specs` as where open work lives
  (grep evidence quoted).
- The prompt and byte-budget tests stay green.

### From WI-613 (Done-when, verbatim)

- PROCESS.md states the rule once, beside the 0->A->B rule, with its two
  consequences.
- The reviewer and builder prompts link to it and restate nothing; the
  vendored `antidote` copies are unchanged.
- Byte budgets on PROCESS.md and the prompts hold (the byte-budget-guard
  report quoted), and the dogfood sync test stays green.

### From WI-614 (Done-when, verbatim)

- PROCESS.md states both delegation kinds as kept, names tiers rather than
  models, and forbids fan-out from review, critique, design-check and
  adjudication sessions, saying that this is prose until the observability
  design exists.
- No prompt or skill restates it; any that names a model for delegation names a
  tier instead.
- Byte budgets hold.

### From WI-556 (Done-when, verbatim)

The spine-authoring skill (the kit master and this repo's copy, kept in sync
where `tests/test_dogfood_sync.py` covers it) states the rule: an LLR may be
satisfied by its parent's coverage; an SR may be satisfied by its children
only when the children span the SR's full dimensional space and are not
interdependent; otherwise the honest states are a recorded orphan or a direct
TC. Cites `OI-72` as the ruling of record. One commit; byte budgets respected
if the touched doc is capped.

### From WI-668 (Done-when, verbatim)

- `prompts.load("WORKER")`'s sent body cites no id of this repository's own
  records; the evidence moved to the template's comment header.
- The close-bar bullet points at the step table and `docs/stack.ini` `[tiers]`
  instead of restating the bar, and every scaffold declares what it names.
- The session-protocol skill's full-suite order agrees with the brief, in all
  three copies; `prompts/CATALOG.md` is regenerated; the commit bar passes.

### From WI-610 (Done-when, verbatim)

- The owner's choice is recorded: surfaced as an open item with both options
  unless the owner has already ruled.
- The chosen side is changed, so one statement of where the trailer rides
  remains, and the other side cites it.

### From WI-536 (Done-when, verbatim)

- `AGENTS.template.md` carries the partial-search rule as one bullet and is
  still within its byte cap; each capped or watched doc touched has its byte
  delta reported and its row re-stamped.
- The `subagent-brief` skill ships with `scope: kit`, `INDEX.csv` is
  regenerated, and `gen_skills_index.py --check` passes.
- The `spine-authoring` skill states the receipt doctrine and the restatement
  test, PROCESS.md §3 carries the one-sentence mechanism, and the build-tier
  discriminator and inline-versus-dispatch conditions are in the two sections
  rank 7 names.
- `gen_skills_index.py --check` refuses a description under the floor, and a
  guardrail payload is selected by model substring; a test pins each.
- A two-file skill has been bootstrapped into a scaffold and the finding closed
  either way (fixed with a test, or the limit stated in `skills/README.md`), the
  `anthropics/skills` row is corrected, and the commit bar passes.
