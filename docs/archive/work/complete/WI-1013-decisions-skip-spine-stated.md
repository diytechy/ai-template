+++
id = "WI-1013"
title = "A delegated run records only the calls no spine row states and that are not about conducting the run itself"
workstream = "process"
sr_refs = ["SR-225"]
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 2
planmode = "single"
+++

## Deliverable

Review round 1 (Sol, low): two findings, both fixed in `81b24a125`. Sol
(low) reviewed alone; Argon timed out and was skipped. Review round 2
(Sol, low, narrow over `6969c7e16..17ee547c1`): APPROVE, no findings.

- MAJOR: `PROCESS.md` §6 and the `coordinator-cycle` skill still sent the
  run's conduct to a decisions record; both now follow the routing table
  (below, "Review round 1").
- MINOR: TC-293 (g) said the section routes no registry, spine or kit-file
  call to the record; it now says touching one no longer routes a call
  there by itself.

Built on the maintenance branch `maint/wi-1013`, cut from `refactor_again` at
`0d67302bd`, with the commit hooks on. The routing table in
`PROCESS_OPTIONS.md` "Delegated decisions record" stays the one home of what
a delegated run records, and its two copies follow it. Against each
Done-when item:

1. **A spine-stated choice is not recorded.** The table's new row "a choice
   a spine row states, whether the run wrote, amended or found the row" routes
   to "decide; the row is its record", and the template's header says the
   same.
2. **The run's conduct is not recorded.** A row for who reviewed and in which
   round, commit grouping or order, a re-stamp whose own ledger carries its
   reason and working around a tool or environment failure routes to "decide;
   the commit and the log fragment carry it". The sentence under the table
   routes a review finding's outcome by what it changes, so one that selects
   a design no spine row states is recorded. The header says both.
3. **What is left, the default and the bound.** "A reading of scope (how far
   the spec, a Done-when item or a requirement reaches), or a design choice
   no spine row states" routes to "decide, and record it". A call no row
   names is not recorded unless it is one of those two kinds or the ratchet
   promotes it. The table covers the calls a build or adjudication session
   makes under a recording dial through the kit's routes. The header opens
   with WHAT GOES HERE and NOT HERE.
4. **The note.** `kitlib.decisions.session_note` names `process-options.md
   "Delegated decisions record"` as the routing table's home and the two
   kinds of call left to record, and no longer says "touched a registry, the
   spine or a kit file". It keeps "or that you are unsure of", the ratchet's
   low-confidence arm. Its signature is unchanged (IF-256). Two new tests in
   `tests/test_decision_record.py` pin it: the note names the home and both
   kinds, each kind is found in that section and in the template's header,
   and neither "touched a registry" nor "kit file" is in the note.
5. **The ratchet is unchanged.** Its paragraph, the `escalate-first` sentence
   and the safety-boundary sentence are byte for byte as they were; the
   second test pins "The confidence ratchet is one-way".
6. **Existing records stay as written.** No file under `docs/decisions/` is
   edited, `run-000-example.toml` included (`docs/decisions/maint-wi-1013.toml`
   D-001). The one file added there is this branch's own record.
7. **RESYNC.** One entry at the end of `RESYNC_PACK.md` §4, "A delegated run
   records only scope readings and design choices no spine row states [since
   0d67302bd]": what the routing now leaves out, what it keeps, the note's new
   content, and that nothing migrates.
8. **The amendments, for the operator's re-accept.** LLR-283's detail (the
   `session_note` clause) and TC-293's method, clauses (g) and (i), text only;
   and, from review round 1, SR-233's acceptance criteria, LLR-311's detail
   and TC-332's method and expected, which drop `PROCESS.md` §6's
   dismissal-to-the-record clause. All text only; all stay `Accepted` and
   show as drift in `docs/ratify/CURRENT.md`, which files both chains
   (SR-225, SR-233) under "Waiting for automated adjudication": the dial
   releases those rungs. SR-225 and IF-256 are unchanged. No id was minted.

Commits: `211eaeea6` the plan; `f751678ab` the two tests, red; `9170e8593`
the routing table, the template's header, `session_note`, the RESYNC entry
and the byte-budget re-stamp, tests green; `1ea2f19af` LLR-283 and TC-293;
`6969c7e16` the close-out; `4dcd70439` review round 1's tests, red;
`81b24a125` its fixes; then this record of the review.

Tests, on the tree at `1ea2f19af`:

<!-- fig: cmd=".venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n auto tests/test_decision_record.py tests/test_decisions_to_review.py tests/test_decision_overrule.py tests/test_ruling_sync.py tests/test_policy_one_home.py tests/test_done_when_blessing.py" rev=1ea2f19af -->
- the record's modules and the direct importers of `kitlib.decisions`:
  `300 passed in 45.17s`;
<!-- fig: cmd=".venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n auto tests/test_import_layers.py tests/test_module_size_ratchet.py tests/test_dogfood_sync.py" rev=1ea2f19af -->
- the whole-tree tests: `55 passed, 1 skipped in 4.64s`;
<!-- fig: cmd=".venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n auto tests/test_bootstrap.py tests/test_check_resync.py tests/test_resync_pack.py tests/test_old_kit_resync.py tests/test_spine_rules.py tests/test_derive_stage.py tests/test_generated_newlines.py tests/test_status_vocabulary_contract.py tests/test_skills_index.py tests/test_held_rung_doctrine.py tests/test_kit_path_invariant.py tests/test_gate_policy.py tests/test_architecture_decomposition_rubric.py tests/test_shell_portability.py tests/test_migrate_carrier.py" rev=1ea2f19af -->
- the modules that read `PROCESS_OPTIONS.md`, `RESYNC_PACK.md` or the
  template: `296 passed in 123.74s (0:02:03)`;
<!-- fig: cmd=".venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n auto tests/test_gen_open_items.py tests/test_decision_record_merge.py tests/test_migrate_vocabulary.py tests/test_open_item_queue.py tests/test_prompts.py" rev=1ea2f19af -->
- the open-items, merge-rung, vocabulary and prompt modules:
  `223 passed in 31.88s`.

Review round 1's tests, on the tree at `81b24a125`:

<!-- fig: cmd=".venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n auto tests/test_prompts.py tests/test_decision_record.py tests/test_decisions_to_review.py tests/test_skills_sync.py tests/test_skill_materialization.py tests/test_bootstrap.py tests/test_dogfood_sync.py tests/test_check_resync.py tests/test_resync_pack.py tests/test_held_rung_doctrine.py tests/test_skills_index.py tests/test_spine_rules.py tests/test_trace.py tests/test_trace_rules.py" rev=81b24a125 -->
- the prompt, skill-mirror, byte-budget, dogfood, RESYNC and trace modules:
  `500 passed, 2 skipped in 172.88s (0:02:52)`.

`trace.py --strict` and `check_trajectory.py --strict` exit 0 on both
trees, and `check_vocab.py` is clean. The specref
(`docs/reviews/2026-11-20-decisions-overlap/README.md`) is cleared at close,
as a terminal row's is.

Byte deltas: `project-trajectory/PROCESS_OPTIONS.md` 201,438 -> 202,180
(+742, watched: the routing table's two new rows and the sentence under it).
It had grown +1,897 unflagged since its last stamp (199,541); the
`byte-budget-guard` row is re-stamped at 202,180 in all three copies.
`project-trajectory/PROCESS.md` 100,990 -> 100,922 (-68, watched: §6's
clause), re-stamped likewise. `byte-budget-guard/SKILL.md` 4,613 -> 4,615
across both re-stamps, 385 under its 5,000 cap.

Review round 1 (`docs/decisions/maint-wi-1013.toml` D-002): at the
coordinator's ruling, the two texts first left for a follow-up now follow the
routing table. `PROCESS.md` §6 no longer sends a dismissal to the record. The
`coordinator-cycle` skill (SKILL.md and `references/recipes.md`, all three
copies byte-equal) records a call only when the routing table routes it
there (§5). Its other sites now send:

- dismissals, re-grades, dispute rulings and the convergence map to the
  response to the review, a commit message, which a convergence reviewer
  does not read (it does read the log fragment);
- reviewer stand-ins, the same-family relaxation, failed commit-check rounds
  and the other run-conduct notes to the commits and the log fragment;
- an operator-held step to the handoff and the log fragment.

A test outside every evidence class, a skipped test and a dispute ruling
still go in the record when §5 sends them there. No cited operator ruling
names the record as its carrier: ruling 7 (2026-10-07) and OI-108 say only
that the same-family relaxation is recorded.

## Context

Filed by hand on 2026-11-20 at the operator's direction. The decisions
records under `docs/decisions/` hold 1,193 entries from 132 runs between
2026-09-28 and 2026-11-20. The operator reads them only when they suspect a
run's choices carry risk (DA-020 as restated on 2026-11-20), and nobody can
read that volume, so a record is worth what an audit can find in it.

A judged sample of 106 entries, weighted back to the whole
(`docs/reviews/2026-11-20-decisions-overlap/`), puts them at:

- about 58% the conduct of the run: triage of review rounds, ceiling and
  budget re-stamps, commit grouping and order, working around a tool or
  environment failure;
- about 10% restating a spine row, usually an LLR the same run wrote or
  amended (LLR-306 holds wi-835's D-011, D-012 and D-015 almost word for
  word), and about 9% partly so;
- about 12% readings of scope, and about 11% design choices no spine row
  states.

The routing table in `PROCESS_OPTIONS.md` "Delegated decisions record"
sends every call that "touches a registry, the spine or a kit-owned file"
to the record, which is why the first two groups land there. Entries also
go stale once later work changes the spine: wi-841 D-002 places a hold in
`worker_endstate`, which LLR-309 now says asks no hold.

The operator's rule: "if the spine surfaces behavior that was selected,
there is no need to mention it as a decision."

### The delta

The routing table in `PROCESS_OPTIONS.md` "Delegated decisions record" is
the one home for what a run records. Two places copy it today and follow it:
`decisions.template.toml`'s header, and the instruction
`kitlib.decisions.session_note` returns, which `agent_loop.session_body`
appends to a build or adjudication session's body under `record` or
`escalate-first` (LLR-283, LLR-284). The instruction's text says "one
[decision.D-<n>] table per call that touched a registry, the spine or a kit
file, or that you are unsure of". It comes to name the table's home and the
two kinds of call left to record, and stops restating the routing.
`session_note` keeps its signature, so IF-256 is unchanged; the seam
`agent_loop` → `kitlib.decisions` already exists. No state, domain value or
boundary is added.

SR-225 states the record's mechanics (its required fields, the close
refusal, the overrule coupling) and not which calls go in it, so it is not
amended. LLR-283 states what `session_note` returns, so its detail is
amended to the new instruction. LLR-283 is `Accepted`: the amendment
changes its text only, stays `Accepted` and shows as drift for the
operator's re-accept, and lands in a commit before any act.

## Done-when

- [x] The routing table and `decisions.template.toml`'s header say that a
      call whose selection a spine row states, whether the run wrote it,
      amended it or found it standing, is not recorded: the row is its
      record.
- [x] They say that a call about conducting the run is not recorded
      either: who reviewed and in which round, commit grouping or order, a
      re-stamp whose own ledger carries its reason, working around a tool or
      environment failure. The commit and the log fragment carry it. A
      review finding's outcome is judged by what it changes, so an outcome
      that selects a design no spine row states is still recorded.
- [x] What is left to record is stated plainly: a reading of scope, and a
      design choice no spine row states. Anything else is not recorded by
      default: a call none of the lines above names goes in the record only
      when it is one of those two kinds, or when the confidence ratchet
      promotes it. The routing covers the calls a build or adjudication
      session makes under a recording dial through the kit's routes.
- [x] The instruction each build and adjudication session is handed under a
      recording dial says the same, read from the one home rather than
      copied: `session_note` names the routing table's home and the two
      kinds left to record, and a test pins that it no longer carries the
      "touched a registry, the spine or a kit file" routing.
- [x] The confidence ratchet is unchanged: low confidence or a reviewer's
      dissent can still promote a call to the record or to an exit.
- [x] The existing records stay as written; nothing rewrites or prunes them.
- [x] A RESYNC entry tells adopters what the routing now leaves out, and
      that their records need no migration.
- [x] LLR-283's detail is amended to the instruction's new content, text
      only, for the operator's re-accept ("The delta"). SR-225 is unchanged.

## Critique dispositions

Round 1 (OpenAI Sol, low, 2026-11-21; Gemini Argon timed out, so Sol
reviewed alone; `docs/reviews/2026-11-21-scope-critiques/WI-1013.md`):
CHANGES-REQUESTED, two findings. Sol could not settle the last Done-when
item from the sources it read, so the coordinator settled it from SR-225 and
LLR-283's text.

- **S4 (MAJOR), `planmode` missing: adopted as `planmode = "single"`.** The
  row promises a routing over the space of a run's calls and changes both a
  shipped doc and the instruction code hands a session, so a short plan
  fixes the wording of the one home and what `session_note` says before the
  code (`docs/plans/WI-1013/plan.md`).
- **S3 (MINOR), no bound and no default for an unclassified call:
  adopted.** The third Done-when item now states the default (not recorded
  unless it is a scope reading or a design choice no spine row states, or
  the ratchet promotes it) and the bound (the calls a build or adjudication
  session makes under a recording dial through the kit's routes).
- **The amendment question (the last Done-when item as filed): settled.**
  "The delta" records that SR-225 does not state the routing and that
  LLR-283 states `session_note`'s content, so LLR-283 is amended and SR-225
  is not. The fourth Done-when item names the test that pins the change.
