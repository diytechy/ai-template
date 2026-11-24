+++
id = "WI-1045"
title = "acceptance_record's landing rules move to a CMP-008 module; the file keeps the two-tree comparison"
workstream = "process"
sr_refs = []
needs = ["WI-1021", "WI-1023"]
specref = ""
buildtier = "strong"
safety_class = "ordinary"
priority = 3
planmode = "single"
+++

## Deliverable

Built on the maintenance branch `maint/wi-1045`, cut from `refactor_again`
at `9e8eb6e57`, with the commit hooks on, under the plan
[`docs/plans/WI-1045/plan.md`](../../../plans/WI-1045/plan.md) (revision 1),
which the coordinator approved on 2026-11-24 before any build, with D1 to
D12 confirmed. No id was minted, no status moved and no snapshot was taken.
No decisions record (D12): every call is the approved plan's.

- `ee1918c02`: the plan.
- `36a476992`: the build: the new module, the cut, the importers, the tests,
  the interface rows, the scaffold row, the documents, the RESYNC entry,
  `intake.py`'s size re-stamp, the regenerated views and the plan's approval
  line.
- `dec40ead9`: the close-out (this Deliverable, the move to `complete/`,
  the log fragment).
- `f21ab4907`: review round 1's fix, the RESYNC entry naming every moved
  definition.
- The commit after it: this review record.

**1. What moved and what stayed** (Done-when 1). The new
`project-trajectory/scripts/landing_rules.py` declares `Component: CMP-008`
and `Contracts: IF-308`. It holds the ruling-to-citer sync (LLR-298:
`ruling_sync_lines`, `staged_ruling_sync_lines`, `commit_ruling_sync_lines`,
their eight helpers and the six constants and git aliases), the parent-first
commit judgement (LLR-358: `parent_first_lines`, `parent_first_tiers`,
`staged_parent_first_lines`, `commit_parent_first_lines` and three helpers)
and the trunk mint's acceptance arms (LLR-364: `settled_amendments` and six
helpers; LLR-153: `unanchored_rows`, `text_as_bound`). The 33 definitions
are byte-identical to the base, compared source segment by source segment;
`acceptance_record` defines none of them and keeps no second name.
`acceptance_record.py` keeps its 73 other definitions, also byte-identical,
under its `Component: CMP-006` header with `Contracts: IF-091, IF-129`: the
two-tree comparison, the mirror rules, the merge-time acceptance-act refusal
(LLR-278, plan D2), the judged-text identity (D3, below) and the record
readers the new module calls (D4). Its docstring loses IF-308's body and the
ruling-sync section and names where they went. The plan's sections 1.2 and
1.3 list every function with its design row and side.

**2. The callers and the cover** (Done-when 2). `check.py` (CMP-007, its two
deferred imports), `integrate.py` (a module-level import, so the deferred-edge
count stays 46), `intake.py`, `text_then_act.py` and `adjudicate_act.py`
(CMP-008) read the moved names from `landing_rules`; no compatibility
re-export is left. The cover, under F-2's rule:
- `check -> landing_rules` (CMP-007 -> CMP-008): IF-308 re-owned to CMP-008,
  requestors CMP-007 and CMP-008 kept; its contract body moved word for word
  into `landing_rules`'s docstring.
- `landing_rules -> acceptance_record` (CMP-008 -> CMP-006): IF-091, its
  `data` rewritten to 156 characters (292 at the base, over the 160
  ceiling; the advisory is gone), `version` v1 -> v2, its body dropping the
  three calls that left and stating the readers the new module reads
  through it; and IF-129, unchanged, for `split_changed_cells` and
  `accepted_text_digest`.
- `landing_rules -> spine_carrier` (CMP-008 -> CMP-006): IF-102, unchanged.
- Removed: `check -> acceptance_record`; `acceptance_record ->
  kitlib/decisions` (CMP-006 -> CMP-008), so IF-256 drops its CMP-006
  requestor; `acceptance_record -> kitlib/registry` (the kernel).
- The other new edges are internal (`intake`, `integrate`, `text_then_act`,
  `adjudicate_act` into `landing_rules`; `landing_rules` into
  `kitlib/sitting` and `kitlib/decisions`) or into the shared kernel.

`arch_seams.cross_component_findings` reports none uncovered: 621 internal
import edges, 122 crossing a component outside the kernel (121 at the base).
`trace.py --root . --strict` reports `component-findings=0
interface-findings=0`; its warnings equal the base's less IF-091's data
advisory. The derived view places LLR-358 (and SR-246 through it) in CMP-008
alone, IF-308 leaves CMP-006's boundary seams, and IF-256 leaves them too.
<!-- fig: cmd="arch_seams._classifiable_edges(root) and arch_seams.cross_component_findings(root) over the worktree" rev="the build commit's tree (36a476992), against 9e8eb6e57 for the base" -->

**3. Behaviour unchanged** (Done-when 3). No requirement, design or test-case
row changed. Eight test modules changed only their imports: the module a
moved name is read from (`test_adoption_record`, `test_decision_overrule`,
`test_intake_held_act`, `test_kitlib_spec_listing`, `test_parent_first`,
`test_parent_first_git`, `test_ruling_sync`, and `test_adjudicate_act`'s
three call sites); `test_parent_first`'s monkeypatch of the judgement's `_git`
follows it, and its docstring names the judgement's new module. Changed
beyond imports, each with its reason:
- `tests/test_acceptance_record.py` gains
  `test_landing_rules_own_IF_308_and_the_rules_that_moved` (the red-first
  test): the new module declares CMP-008 and IF-308 with its body and this
  module neither; every moved name is defined there and none here; the
  import runs one way; the judged-text identity is imported, not defined;
  and the rules call no `open` or `Path`.
- `tests/test_adjudicate_act.py`,
  `test_the_wait_is_read_from_the_parent_first_rules_one_predicate`: its
  source-text assertion names `landing_rules.parent_first_tiers(`, the
  module `adjudicate_act` now reads the tiers from.
- `tests/test_bootstrap.py`: `scripts/landing_rules.py` joins the scaffold's
  expected files (it ships through the manifest, below).
- `tests/test_module_size_ratchet.py`: `intake.py` 1946 -> 1947 (item 4).

**4. The sizes** (Done-when 4). `acceptance_record.py` 989 -> 689 SLOC: the
296 that moved and four import lines. It has no size-ratchet entry before or
after (under the 1,000-SLOC threshold at both ends), so the census needed no
edit for it (plan D7). `landing_rules.py` is 340 SLOC (the plan estimated
about 320; its sibling guard repeats the import block), under the threshold.
`intake.py` 1946 -> 1947, its one import line, a reviewed bump with that
reason. `integrate.py` 1788 and `check.py` 1339 are unchanged;
`adjudicate_act.py` 374 -> 375 and `text_then_act.py` 116, no entries. Import
layers: 46 deferred edges, inside 14..46, no cycle. No complexity row in
either sensor names a moved function. The smoke tier gains one test.
<!-- fig: cmd="check_complexity.module_sloc over each file" rev="9e8eb6e57, then the build commit's tree (36a476992)" -->

**The scaffold, the documents and the RESYNC entry.** A `MAPPING` row ships
`scripts/landing_rules.py`; `project-trajectory/README.md` gains its
kit-contents row. Docstrings the move made false now name `landing_rules`:
`kitlib/git.py`, `kitlib/decisions.py`, `text_then_act.py`, `intake.py`,
`integrate.py`, `check.py`'s two import comments, and
`docs/enforcement-audit.md`'s parent-first row. The generated views were
regenerated (`trunk_step.py --regen`: `components.derived.toml`,
`interface-reference.md`, `PROJECT_STATE.html`, `docs/stage`). The RESYNC
entry, "The landing rules move out of the acceptance record into their own
module", is anchored `[since 9e8eb6e57]`; `scripts/check_resync.py` reads it
`OK, 10 shipped path(s) changed`.

**Deviations from the spec, and from the plan.**
- From the spec's Context (approved as plan D3): the held re-acceptance's
  judged-text identity, `accepted_text_digest`, which the Context lists among
  the rules to move, stays in `acceptance_record` behind IF-129. One of its
  three readers, the held-claim exception (`held_status`), is CMP-006, so
  moving it would add a crossing and a row; kept, all three readers call the
  one function and IF-129, IF-326, TC-398 and TC-461 stay true. The LLR-359
  rule itself already lives in CMP-008 (`adjudicate_act`) and CMP-006
  (`held_status`), neither of which moved, and the Context's
  `amendment_values` is no longer in this file.
- From the plan: none beyond the estimate in item 4.

**Red first.** The boundary test and the eight modules' import changes, before
the new module existed: `tests/test_acceptance_record.py` `1 failed, 14
passed in 0.97s` (the new test, `FileNotFoundError` on
`project-trajectory/scripts/landing_rules.py`); the switched modules `7 errors
in 3.78s`, each a collection error on the same missing file
(`test_adoption_record` loads it inside its test, so it does not error at
collection).
<!-- fig: cmd="python -m pytest -q -p no:cacheprovider tests/test_acceptance_record.py; then the eight switched modules" rev="ee1918c02 plus the uncommitted test changes, before any code change" -->

**Tests run** (the worktree's venv, `-p no:cacheprovider`, `--basetemp`
under `D:/review-tmp/2026-11-24-wi1045/`):
- The boundary test after the code: `tests/test_acceptance_record.py` with
  four of the switched modules (`test_parent_first`,
  `test_kitlib_spec_listing`, `test_ruling_sync`, `test_decision_overrule`),
  `105 passed in 18.15s`.
- The 137 modules importing a changed module (`acceptance_record`,
  `landing_rules`, `check`, `integrate`, `intake`, `text_then_act`,
  `adjudicate_act`, `bootstrap`, `kitlib/bootstrap_manifest`, `kitlib/git`,
  `kitlib/decisions`) or reading a changed document or registry (the README,
  the RESYNC pack, the enforcement audit, the interface registry and its
  derived views), the modules of the tests tagged TC-147, TC-278, TC-313,
  TC-331, TC-397, TC-398, TC-403 and TC-461 (`test_coordinator_act` added for
  TC-398), and `test_import_layers`, `test_module_size_ratchet`,
  `test_complexity_ratchet` and `test_dogfood_sync`, `-n auto`: `5212
  passed, 4 skipped in 5285.36s (1:28:05)`.
- `trace.py --root . --strict`: exit 0, `component-findings=0
  interface-findings=0`. `check_trajectory.py --root . --strict`: exit 0,
  `clean (1071 work item(s), 943 done (88%), 37 cancelled, graph acyclic)`.
- `run_menu.py smoke`, once, on the close-out tree: exit 0, `3957 passed,
  3 skipped, 18 warnings in 150.36s (0:02:30)` (the tier 3,960 tests, one
  more than the base), `check_resync: OK, 10 shipped path(s) changed`; CPU
  691.9 s over the 540 s budget, reported only, on a box shared with another
  builder. The unfiltered suite is the coordinator's, before the merge.
<!-- fig: cmd="python -m pytest -q -n auto -p no:cacheprovider --basetemp <scratch> <the 137 modules>; python project-trajectory/scripts/run_menu.py smoke" rev="36a476992's tree for the module run, then the close-out tree for the smoke run" -->

**Review record.** Round 1: Gemini Hydrogen `APPROVE`, findings=0; OpenAI
Sol one MINOR, adopted by the coordinator: the RESYNC entry named 10 of the
33 moved definitions and folded the rest into "with their helpers". Fixed in
`f21ab4907`: the entry lists all 33, grouped by rule (the ruling sync's 17,
its four constants and two git aliases among them; the parent-first
judgement's 7; the trunk mint's 9), the same set as the boundary test's
`LANDING_RULES`, and says that, with no compatibility shim, a project script
or test importing any of them from `acceptance_record` must import it from
`landing_rules`. `scripts/check_resync.py --root .`: `OK, 10 shipped path(s)
changed; entry anchored at 9e8eb6e5749735bc7431265cc9d40828e9eb7abe`.

**Acts owed to automated adjudication.**
- Amendments to `Accepted` rows: none.
- Routed traced changes to `Accepted` rows: none.
- New or rewritten `Drafted` rows owed a first acceptance: no new row.
  Three off-spine `Drafted` interface rows were rewritten, each still owing
  the first acceptance it owed before: IF-091 (`data`, `version`, its body),
  IF-308 (`owner`) and IF-256 (`requestors`).

**Left for the coordinator to file** (plan D10).
- `acceptance_record.verdict_rulings`, an alias of
  `kitlib.verdict.verdict_rulings` no script or test calls. It keeps
  `acceptance_record`'s import of `kitlib/verdict`, a CMP-006 -> CMP-008
  edge, so CMP-006's accepted `notes` sentence about `kitlib/station.py` and
  `kitlib/verdict.py`, "Their other edges come from files declaring CMP-008
  and are internal", is not true.
- `landing_rules.ARCHIVE_WORK_DIR`, a constant nothing reads, moved verbatim
  with the ruling sync's constants.

Round 2 (narrow, over `dec40ead9..c3d455001`, round 1's finding and the coordinator's ruling prepended): OpenAI Sol APPROVE findings=0; Gemini Hydrogen APPROVE findings=0.

## Context

Filed on trunk on 2026-11-21 from WI-1021's one-component table, on the
operator's ruling (queue-drill HANDOFF §3.5 R2). Under one component per
file (§3.3 N3), a file doing two components' work is evidence about the
partition (OI-14): it keeps its one header and gets its own row, never a
split inside the row that found it.

`project-trajectory/scripts/acceptance_record.py` (2,392 lines) declares
CMP-006 under WI-1021. Its declared job is the spine's: comparing two git
trees cell by cell to say whether accepted text moved (LLR-158, LLR-178,
LLR-202, LLR-220, LLR-222, LLR-225, LLR-302). Beside it sit rules the
coordinator's landing runs on top of that comparison, which their design
rows tag CMP-008:

- the ruling-to-citer sync (LLR-298: `ruling_sync_lines` and its staged and
  commit forms);
- the parent-first commit judgement (LLR-358: `parent_first_lines` and its
  forms);
- the intake mint's acceptance arms (LLR-153) and its settled-amendment
  filtering (LLR-364);
- the held re-acceptance's text identity (LLR-359: `accepted_text_digest`,
  `amendment_values`).

The merge-time re-acceptance refusal (LLR-278) is tagged CMP-006 and reads
as the spine's; the plan says which side it falls on. Each of these design
rows also names functions in other files (`check.py`, `integrate.py`,
`text_then_act.py`, `intake.py`), so the exact set that moves is the plan's,
read from the code.

`check_doc_refs.py`, the table's other file doing two components' work, gets
no row until WI-1023 lands: its symbol-binding oracle's spine role retires
there (§3.5 R2).

**Order (settled by the scope critique, 2026-11-21).** After WI-1023 (F-3),
which itself follows WI-1022 (F-2). F-2 makes interface owners and endpoints
component ids and narrows the cross-component cover, so the move's seams are
written once, in that form. F-3 removes the design rows' `module` and
`code_symbol` cells, so the move re-points none of them.

## Done-when

- [x] The CMP-008 rules above live in one or more modules whose `Component:`
      header declares CMP-008; `acceptance_record.py` keeps the two-tree
      comparison and its CMP-006 header. The plan lists every function that
      moves and every one that stays, with the design row behind each.
- [x] Every cross-component import the move introduces or redirects is
      covered under F-2's rule: a `call` row owned by the imported file's
      component that names the importer's component among its requestors.
      That includes the edges between CMP-006 and CMP-008 and the callers
      in other components whose import now lands in the new module, such
      as `check.py` (CMP-007) on the parent-first rules through IF-308. The
      cover is a new `Drafted` row, a requestor added to an existing
      `Drafted` one, or an existing seam re-owned, each with its contract
      body; the cross-component rule reports nothing uncovered.
- [x] Behaviour is unchanged: no design row's requirement text changes, and
      every test module importing `acceptance_record` or a module this row
      creates runs green with only its imports changed; a test that must
      change otherwise is named in the Deliverable with its reason.
- [x] `acceptance_record.py`'s size baseline is re-stamped down by what left;
      `trace.py --strict` and `check_trajectory --strict` are clean.
