+++
id = "WI-1072"
title = "A row's own text cannot add or override a judged-text identity the binding records"
workstream = "process"
specref = ""
sr_refs = ["SR-178"]
needs = ["WI-1070"]
buildtier = "medium"
safety_class = "ordinary"
priority = 3
planmode = "single"
+++

## Deliverable

Built on the maintenance branch `maint/wi-1072`, cut from `refactor_again`
at `c31642461`, with the commit hooks on, under the plan
[`docs/plans/WI-1072/plan.md`](../../../plans/WI-1072/plan.md) (revision 1).
The coordinator approved it on 2026-11-24 before any build, D1 to D10
confirmed: D1 with the refusal naming where the line sits; D6 on a condition
read from the code below. No status moved, no snapshot was taken, and no id
was minted (D5). No decisions record: every choice is stated by a row or by
the approved plan.

- `4d96403cb`: the plan.
- `98b7fe483`: the build: code, tests, rows, evidence, regenerated views,
  the RESYNC entry and the plan's approval line.
- The commit after it: this close-out.

**1. The mechanism (Done-when 1).** A refusal at compose (D1), in
`adjudicate_brief.compose`, for every routed brief (D2). After the fill, the
composed text is read with the binding reader's own pattern and compared, as
a multiset, with the lines the composer wrote: the amendment brief's
`{identity}` slot, none for every other brief, and for a combined sitting
its sections' text, each section checked as it was composed (D9, reported
under a values key that is never a slot), so the sitting's check covers its
own template and perspectives tail. Any identity-shaped line beyond those
refuses the brief (`_composed_identity_refusal`), and so does an identity
block that ends the text (below). The refusal names the line, the row id it
names and where it sits: its line number, the row whose shown text holds it
(the nearest rendered row head above it) and the heading above it, and, in a
combined sitting, the section (the coordinator's D1 condition). For example,
the measured replacement case now reads:

> the combined brief cannot be filled: the first-acceptance section: the
> first-acceptance brief's text carries a line shaped as a judged-text
> identity line that its composer did not write, which a sitting's binding
> would record as judged text: `JUDGED-TEXT: LLR-002 sha256:0123456789abcdef`
> at line 35, in the text shown for LLR-005, under `--- ROWS AWAITING A FIRST
> ACCEPTANCE, WITH THEIR CHAINS ---`. Reword it in its source (the row's
> cell, the spec or the template it came from) so no line opens as an
> identity line does, then compose again

The binding's format, its reader
(`requested_identities`) and its three consumers are unchanged, so a binding
written before this change reads as before (D3).

**D6, read from the code.** The coordinator's condition was that text
appended to a composed brief before `coordinator_adjudicate.py adjudicate
--brief-file` binds it is composed by kit code with no registry or spec
text. It is not: the coordinator-cycle recipe (`references/recipes.md`,
"Adjudication", step 1) appends a disposition row's `## Owner route` section
verbatim from that row's spec, and the arms map is drawn by a sub-agent from
the rows and tests ("the composer does not generate it"; "Draw the arms map
before composing the sitting"), then appended. So the check extends to
reservation, where the brief file is read: `bind_pending` raises
`ValueError` (`identity_refusal`) for a prompt whose identity-shaped lines
are not one contiguous block of distinct rows when it requests an amendment,
or that holds any when it requests none, naming each such line and where it
sits, and writes nothing; `coordinator_adjudicate.bind_requested` returns it
as a refusal before launch (exit 2; IF-284's list gains it). A composed
brief always passes (compose guarantees one block or none), so the loop's
route, which binds what it composed, never meets it. Because an appended
line directly after a block that ends the brief would join that block,
compose also refuses a brief whose identity block is its last text (only an
operator override placing the slot last can do that; the shipped templates
do not). LLR-359 states all three; its scope sentence is unchanged (the
plan's widening to "text appended to a composed brief" is dropped).

**2. The tests (Done-when 2).** `tests/test_judged_identity_lines.py` (new,
in process over `tests/routed_link_fixtures.py`, smoke tier), each tagged
TC-398:
- `test_an_amendment_cell_holding_an_identity_line_refuses_the_brief[own,
  shown, unshown]`: LLR-001's moved detail holds a line naming LLR-001,
  LLR-002 or LLR-004; refused naming the id, LLR-001's text and the rows'
  heading.
- `test_a_first_acceptance_cell_holding_an_identity_line_refuses_the_brief[own,
  shown, unshown]`: a Drafted LLR-005's detail names LLR-005, LLR-001 or
  LLR-004.
- `test_a_combined_sittings_later_section_holding_an_identity_line_refuses_it[own,
  shown, unshown]`: `amendment:LLR-002;first-acceptance:LLR-005`, LLR-005's
  detail naming LLR-005, LLR-002 (the replacement case) or LLR-004; refused
  naming the first-acceptance section.
- `test_a_combined_sittings_own_template_holding_an_identity_line_refuses_it`.
- `test_a_brief_whose_identity_lines_end_its_text_is_refused`.
- `test_every_routed_brief_refuses_an_identity_line_in_a_slot[8 briefs]`:
  each assembler stubbed to its template's slot set.
- `test_without_the_line_a_brief_binds_only_its_composers_block[amendment,
  first-acceptance, combined]`: the control; one consecutive block (none for
  the first acceptance), and the binding records exactly it.
- `test_reservation_refuses_an_identity_line_appended_after_composition`,
  `test_reservation_refuses_any_identity_line_in_a_brief_requesting_no_amendment`,
  `test_reservation_refuses_a_block_naming_one_row_twice`: D6's extension,
  through `coordinator_adjudicate.bind_requested` and `bind_pending`; no
  binding file is written.

`tests/test_done_when_blessing.py` gains
`test_a_combined_sittings_done_when_context_holding_an_identity_line_refuses_it`
(git, slow tier): the lane spec's Context holds a line naming the stubbed
amendment section's LLR-1.

**3. The rows (Done-when 3).** Amended in text only (D4), under the three
row rules: **LLR-359** `Detail` (the identity lines are one block; the
compose refusal naming the row and where the line sits; the end-of-text
refusal; reservation binds only one block of distinct rows, none for a brief
requesting no amendment, refusing otherwise) and `Rationale` (one sentence
added); **TC-398** `Method` and `Expected` (one sentence added to each);
TC-398's `Evidence` regenerated by `trace.py --regen-evidence` (a silent
trace cell). LLR-167 and TC-161 are unchanged. No code name in either row;
LLR-359 stays within SR-208 ("bound to the row's judged text") and SR-178;
TC-398 expects nothing LLR-359 does not state.

**4. The RESYNC entry (Done-when 4).** `project-trajectory/RESYNC_PACK.md`,
"A brief whose text carries a judged-text identity line its composer did not
write is refused [since c31642461]", naming `scripts/adjudicate_brief.py` and
`scripts/coordinator_adjudicate.py`. `scripts/check_resync.py`: `check_resync:
OK, 2 shipped path(s) changed; entry anchored at
c31642461a257e69c689745436985f8c61617703`.

**Contracts.** The IF-115 body in `adjudicate_brief.py` (one block; the
compose refusal; `bind_pending`'s ValueError) and the IF-284 exit-2 list in
`coordinator_adjudicate.py`; `docs/interface-reference.md` regenerated.

**Deviations from the plan, each with its reason.**
- D6's condition did not hold, so reservation checks the brief it binds
  (`identity_refusal`, `coordinator_adjudicate.py` touched, IF-284's
  sentence), and compose refuses an identity block ending the text, so an
  appended line cannot join it. Four tests beyond the plan's table: the
  three reservation tests and the end-of-text test. LLR-359's and TC-398's
  added sentences differ from the plan's §3 accordingly; LLR-359's scope
  sentence stays as it was.
- LLR-359's added rationale names "a section appended to it before
  reservation" rather than the plan's "such as an owner-route section or an
  arms map": `trace.py --strict` refuses `such as` as an open-ended clause.
- `adjudicate_brief.py` grew 782 -> 868 SLOC (the plan guessed about +20;
  the reservation check and the locator), under the 1,000 threshold.
- The control test is parametrized per kind and also binds each brief.
- The refusal names where the line sits (the coordinator's D1 condition).

**Red first.** The 26 new tests before any code change: `23 failed, 3
passed in 4.27s` (the 3: the clean controls). Each composition case failed
because the brief composed (`AssertionError` on `text is None`, the
returned brief's text shown), the two reservation cases because
`bind_requested` bound and returned `None`, and the twice-named block with
`Failed: DID NOT RAISE ValueError`.
<!-- fig: cmd="python -m pytest -q -n 8 -p no:randomly --tb=line tests/test_judged_identity_lines.py tests/test_done_when_blessing.py::test_a_combined_sittings_done_when_context_holding_an_identity_line_refuses_it --basetemp <scratch>" rev="4d96403cb plus the uncommitted tests, before any code change" -->

**Tests run** (the worktree's venv, `-p no:randomly`):
- After the code, the new tests and the Done-when case: `26 passed in
  4.22s`.
- The 40 modules: those importing `adjudicate_brief` or
  `coordinator_adjudicate` (grep, and `trace.py --tests-for` for both), those
  holding TC-398's tests, the new module, and `test_import_layers`,
  `test_module_size_ratchet`, `test_complexity_ratchet`, `test_dogfood_sync`,
  `-n auto`: `53 failed, 2171 passed, 17 skipped in 501.92s (0:08:21)`. All
  53 sit in five git-heavy modules (`test_held_status_git` 25,
  `test_intake_held_act` 24, `test_integrate_admission` 2,
  `test_done_when_blessing` 1, `test_adjudicate_act` 1), each failing as
  `... last_accepted/docs/requirements/<registry>.toml cannot be read at
  <commit>`: that run's `--basetemp` sat under a long scratch path, and the
  fixture repositories' recorded-copy paths passed Windows' path limit.
  Those five modules rerun with the same changes and a short `--basetemp`
  (`D:/review-tmp/2026-11-24-wi1072/pt`): `303 passed in 1308.20s
  (0:21:48)`.
- `trace.py --root . --strict`: exit 0, `Traceability: SN=31 SR=141 LLR=372
  TC=448 orphans=0 integrity=0 ...` with no finding (a first run flagged
  this row's own rationale `such as`, reworded above).
- `check_trajectory.py --root . --strict`: `clean (1071 work item(s), 943
  done (88%), 37 cancelled, graph acyclic).` before the close.
- `check_docs.py --root .` after the move: `check_docs: OK - 3720 doc(s),
  3842 intra-repo link(s), 0 broken.`
- `run_menu.py smoke` once, on the close-out tree: exit 0. Its steps:
  `trace.py --strict` as above; `check_trajectory: clean (1071 work
  item(s), 944 done (88%), 37 cancelled, graph acyclic).`; `check_docs: OK -
  3720 doc(s), 3842 intra-repo link(s), 0 broken.`; `check_resync: OK, 2
  shipped path(s) changed; entry anchored at c31642461...`; the smoke tier
  `3981 passed, 3 skipped, 18 warnings in 310.72s (0:05:10)`, its 3,984
  cases under `max-tests = 4060`, with CPU 905.1 s over the 540 s budget
  (`smoke budget: ... -> OVER`, reported only, on a box shared with another
  builder). The unfiltered suite is the coordinator's, before the merge.
<!-- fig: cmd="python -m pytest -q -n auto -p no:randomly --basetemp <scratch> <the 40 modules>; the five failing modules again with --basetemp D:/review-tmp/2026-11-24-wi1072/pt; trace.py --root . --strict; check_trajectory.py --root . --strict; check_docs.py --root .; run_menu.py smoke" rev="98b7fe483's tree (module runs, uncommitted then) and the close-out tree, 2026-11-24" -->

**Acts owed to automated adjudication.**
- Amendments to `Accepted` rows (text only): LLR-359 (Detail, Rationale);
  TC-398 (Method, Expected).
- Routed traced changes to `Accepted` rows: none (TC-398's `Evidence` is a
  silent trace cell; no `verifies` moved).
- New `Drafted` rows owed a first acceptance: none.

**Left.**
- Nothing of this row's. The locator is a reading aid: it names the line,
  the nearest rendered row head and heading above it, so a line in an
  operator's template override or an appended section is named by its line
  and that section's heading. The unfiltered suite is the coordinator's,
  before the merge.

## Context

Filed on trunk on 2026-11-24 by the queue drill's coordinator, from
WI-1070's plan (its decision D12, found by its builder and left out of its
scope).

A sitting's binding records one judged-text identity per row its brief
shows for judgement: the brief's `JUDGED-TEXT: <row id> <digest>` lines,
read by one reader over the whole composed prompt (`adjudicate_brief`,
`requested_identities`: a multi-line match anywhere in the text, later
lines replacing earlier ones for the same id). The held act, the held-claim
exception and the record's kept-row reading each take a row only while the
committed row's identity equals the bound one (LLR-359; WI-1069's
`## Trust`).

The brief prints each judged cell verbatim, and a registry cell may span
lines. So a row whose own text holds a line shaped as an identity line
adds an identity the composer never wrote; where that line comes after the
genuine one (a combined prompt's first-acceptance section follows its
amendment section's identity lines), it replaces the genuine digest of the
row it names. A binding could then record a digest no shown text has, and
a held act could take a row whose text the verdict never judged. Registry
text is written by supported workflows (authoring and the kit's routes),
so this is inside the coverage bound PROCESS.md §6 ("Review threat model")
draws. WI-1070's new context listing collapses each listed cell to one
line and is tested against such a line; the rows' own cells are not.

**Order.** After WI-1070, which changes the same brief and template.

Critiqued 2026-11-24 (Sol and Hydrogen;
`docs/reviews/2026-11-24-scope-critiques/WI-1072.md`): `planmode` is
`single`, and the row carries a `## Trust` section.

## Trust

PROCESS.md §3, "When a guard is owed". The binding beside a verdict decides
whether an act may take a row on a held rung, so what enters it is
authority; this row narrows what enters it, and changes nothing else.

- **Producer.** Unchanged from WI-1069's `## Trust`
  (`docs/archive/work/complete/WI-1069-brief-shows-routed-links.md`): the
  binding is written when a sitting's request is bound, and records one
  judged-text identity per row the composed brief shows for judgement. This
  row adds that only the identity lines the composer itself writes for
  those rows enter it; text a judged cell carries never does.
- **A failed or missing write.** Unchanged: a binding absent, unreadable,
  carrying no identity, not naming the row, or naming another digest than
  the committed row's, fails closed in each consumer. A brief the plan's
  mechanism cannot compose safely is refused at compose, never bound with
  a guess.
- **Consumers.** Unchanged: the held act, the held-claim exception and the
  record's kept-row reading each take a row only while the committed row's
  identity equals the bound one, through the one identity function.

## Done-when

- [x] The binding records only the identity lines the composer wrote for
      the rows it shows for judgement: a judged cell, in an amendment, a
      first-acceptance or a combined brief, holding a line shaped as an
      identity line neither adds an identity nor replaces one. The plan
      settles the mechanism (where the reader looks, or how a judged cell
      is rendered, or a refusal at compose), from the code.
- [x] A test per brief kind drives a cell holding such a line naming its
      own row, another shown row and a row not shown, red first.
- [x] LLR-359 states the rule in contract terms, no code names, if its
      text does not already cover it; any amended row is owed to a sitting.
- [x] A RESYNC entry if a shipped file changes.
