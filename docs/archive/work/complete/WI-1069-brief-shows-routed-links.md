+++
id = "WI-1069"
title = "A sitting is shown each routed link change: the acceptance model and amendment brief carry it, link-only rows too"
workstream = "process"
specref = ""
sr_refs = ["SR-146", "SR-178"]
needs = []
buildtier = "medium"
planmode = "single"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

Built on the maintenance branch `maint/wi-1069`, cut from `refactor_again`
at `d62f3c74b`, with the commit hooks on, under the plan
[`docs/plans/WI-1069/plan.md`](../../../plans/WI-1069/plan.md) (revision 1).
No status moved and no snapshot was taken on this repository. Two ids were
minted from the brief's ranges, LLR-484 and TC-571 (`trace.py --bump-ids`:
LLR 483 -> 484, TC 568 -> 571). No decisions record: every choice is stated
by a row or by the approved plan.

**The approval.** The coordinator approved plan revision 1 (`1fd247ee0`) on
2026-11-23 before any build, with D1 to D12 confirmed as proposed (D5 keeping
the RESYNC entry's "take held acts before upgrading, else re-sit" as the
adopter's guidance; D11 stamped to the measured size with the reason), the
RESYNC anchor kept at the branch base `[since d62f3c74b]`, and the two
`Drafted` interface rows' note edits listed apart as off-spine below.

- `1fd247ee0`: the plan.
- `144f9d8ef`: the build: code, tests, rows, template, regenerated evidence,
  views and prompt catalogue, the re-stamps, the RESYNC entry.
- `5f3907bb7`: the newline pin the smoke run found, and the views regenerated
  after the build commit (the off-spine census names the build among the
  commits that touched `interfaces.toml`).
- The commit after it: this close-out.

**1. Selection and the operator surfaces.** `record_rows.routed_cells(rel)`
is the one routed-cell lookup (`_settled` reads it).
`baseline_snapshot.routed_moved` returns the routed cells of a row claiming
acceptance that differ from its recorded copy, with `is_drifted`'s guards;
`trace.sr_chain_drifts` selects a chain on drift **or** a moved routed link,
so drift stays the accepted half (D1) and an unjudged trace cell
(`Hat-Refs`, `Phase`, `Evidence`) selects nothing. Model rows carry `routed`
and order their cells accepted, then routed, then the other trace cells
(`_ordered_cells`). One grouping, `trace.changed_cell_groups`, labels a
changed row's cells "accepted — re-acceptance owed", "adjudicated link —
goes to a sitting" and "other trace cell — owes no act", a lone accepted
group unlabelled and a `Drafted` row collapsed as before (D8); the acceptance
brief renders it and `gen_open_items._changed_cell_groups` now reads it
instead of its own copy. On this tree the model lists SR-017, SR-022 and
SR-024, which it missed at the base; the brief and the page show LLR-017's
`Constrains` (empty -> IF-032) under the sitting label.

**2. The amendment brief.** `_scoped_chain_rows` keeps a scoped row's moved
accepted cells and its moved routed links (`_judged_cells`); `_cell_block`
renders the links after the accepted cells, each marked `(link)`, so a
link-only row is shown; other trace cells are not. The template's `{rows}`
listing is labelled "AMENDED CELLS AND MOVED LINKS", its identity label
covers the links, and a LINKS paragraph asks of a link the question its
routing exists for, "does the row's text state what the link now points
at?", mapping yes to clarity and no to a meaning row not to bless. The
verdict's row grammar is unchanged (a link-only row's line parses as any
row's). Over WI-1068's 26 `amendment:` tokens the brief now shows 26 rows
(23 at the base), 21 of them with a `Constrains` link, and 26 identity lines.

**3. The identity.** `acceptance_record.accepted_text_digest` keeps its name
and shape (D4) and digests a row's nonempty routed cells with its accepted
cells. The brief states it and the three consumers compute it from the
committed row: the held act (`adjudicate_act._unbound_text`, its refusal now
naming "judged text (accepted cells and adjudicated links)"), the held-claim
exception (`held_status._excepted`) and the held-MEANING mint
(`acceptance_record.text_as_bound`), so a link moved after a verdict reads as
moved text in each. A binding written before this change binds a row with no
routed link as before and fails closed for a row carrying one (D5): in this
repository 0 of the 289 bound identity tokens sit on a held tier, so no live
consumer reads differently.

**4. Scope refusals.** A scope token naming neither home still refuses by
name; a scope none of whose rows has a moved accepted cell or adjudicated
link still refuses naming the scope (its reason now says so); every other
scoped row with nothing to judge is named on one closing line, `Scoped,
nothing to judge (not shown; rule no line for them): <ids>.`, which no row
count reads (D6). The combined brief composes its amendment section through
the same derivation, so it no longer drops a scoped row silently.

**5. Coverage bound.** The promises reach registries, recorded copies, act
ledgers and bindings in the shapes the kit's own routes write; a hand-edited
recorded copy, act ledger or binding is outside them (PROCESS.md §6, "Review
threat model"). LLR-359 and LLR-484 state it in their closing sentence.

**6. Tests, rows and the RESYNC entry.** Rows, as the plan's §4 wrote them,
with three corrections from mapping each clause to a test: LLR-359's refusal
names both digests only for an unequal identity (an absent one names the
committed digest); TC-398 drops the planned digest-width clause (TC-461's
test) and reads the link-only identity from the live file; LLR-484's label
clause speaks of the listed row's own accepted and other trace cells. SR-178's
acceptance-criteria absolute-term advisory ("never") is gone; SR-178 now has 9
direct design rows, over the advisory bound of 7. The RESYNC entry is
`[since d62f3c74b]`; `scripts/check_resync.py` reads it OK.

**Deviations from the plan, each with its reason.**
- The amendment-brief link tests live in a new in-process module,
  `tests/test_amendment_brief_links.py` (smoke tier), not the slow
  `tests/test_adjudicate_brief.py`, where only the removal test changed
  (renamed `..._is_named_not_shown_beside_a_removal`).
- The held-claim test lives in `tests/test_adjudicate_act.py`, whose small
  git fixture holds a requirement tier carrying a link; the fixture of
  `tests/test_held_status_git.py` holds only the needs tier, which has none.
- The held-MEANING mint's case is a new parameter (`link-moved-after`) of
  an existing test in `tests/test_intake_held_act.py`, covered by the
  module's TC-147 tag, so TC-147's evidence cell did not change (D12 expected
  it to).
- `held_status.HELD_REMEDY` names "accepted text and adjudicated links" (the
  plan named its docstring only).
- Forced by checks: `amendment_brief._scoped_chain_rows` split
  (`_judged_cells`) to stay under the cognitive limit; the complexity row of
  `trace._cell_diff_lines` deleted (it fell under 15: trunk debt WI-572
  recorded, now paid); `trace.py`'s SLOC baseline 3847 -> 3861 (+14, the plan
  guessed +10; D11); the smoke tier's `max-tests` 3890 -> 4060 (+29 in-process
  cases, about 4% headroom, as the stamp before it); the acceptance-brief
  golden regenerated (its opening sentence); the one non-literal LF site's
  pin in `tests/test_generated_newlines.py` 1672 -> 1656.
- `docs/registry-machinery-reference.md` §12.10 gains one sentence.

**Red first.** The new and changed tests before any code change:
`27 failed, 8 passed in 53.62s` (the 8: the guards and the unchanged
`test_only_ACCEPTED_cells_reach_the_judge`), each failing for its reason:
`SR-001's chain is not listed for (...)` for each of the six routed cells,
`assert ['SR-001', 'SR-003'] == ['SR-001', 'SR-002', 'SR-003']`,
`KeyError: 'routed'`, the link-only scope refused as "none of the 1 row(s) ...
still carries accepted text", `{'SN-Refs': 'SN-002'}` (the digest unmoved by a
link), the held act owed (`{'amendment': {'reaccepts': ['SR-001'], ...}}`)
under a moved link and under an accepted-cells-only binding, "a link moved
after the verdict was excepted", and the held-MEANING row minted to the
operator.
<!-- fig: cmd="python -m pytest -q -p no:cacheprovider --basetemp <scratch> <the 35 new and changed tests>" rev="1fd247ee0 plus the uncommitted tests, before any code change" -->

**Tests run** (the worktree's venv, `-p no:cacheprovider`, `--basetemp` under
`D:/review-tmp/2026-11-23-wi1069/`):
- The same 35 after the code: `35 passed in 56.10s`.
- The 86 modules importing a changed module (`trace`, `baseline_snapshot`,
  `record_rows`, `acceptance_record`, `amendment_brief`, `gen_open_items`,
  `adjudicate_act`, `held_status`, by grep and `trace.py --tests-for`), the
  modules of TC-147, TC-161, TC-398 and TC-571, and the four ratchets, `-n
  auto`: `3 failed, 3134 passed, 2 skipped, 18 warnings in 3165.81s
  (0:52:45)`. The three: the committed stage stale (the views regenerated),
  the smoke membership over 3890 (re-stamped) and the acceptance-brief golden
  (regenerated); rerun, `6 passed in 10.95s`.
- The ratchets after the re-stamps: `56 passed, 1 skipped in 7.95s`; after
  the `_judged_cells` split, the brief's importers (`test_adjudicate_brief`,
  `test_amendment_brief_links`, `test_coordinator_adjudicate`,
  `test_intake_held_act`): `224 passed in 161.14s (0:02:41)`.
- `trace.py --root . --strict`: exit 0. `check_trajectory.py --root .
  --strict`: exit 0, `clean (1066 work item(s), 935 done (88%), 37 cancelled,
  graph acyclic)`.
- `run_menu.py smoke`: the first run `1 failed, 3901 passed, 3 skipped, 18
  warnings in 187.61s` (the LF pin); after the fix, exit 0, `3902 passed, 3
  skipped, 18 warnings in 232.54s (0:03:52)`, CPU 842.0 s over the 540 s
  budget (reported only, on a box shared with another builder). The
  unfiltered suite is the coordinator's, before the merge.
<!-- fig: cmd="python -m pytest -q -n auto -p no:cacheprovider --basetemp <scratch> <the 86 modules>; python project-trajectory/scripts/run_menu.py smoke" rev="144f9d8ef's tree (the module run on it uncommitted), then 5f3907bb7's for the smoke run" -->

**Acts owed to automated adjudication.**
- Amendments to `Accepted` rows (text only): SR-178 (AcceptanceCriteria,
  Rationale); LLR-167 (Detail, Rationale); LLR-359 (Detail, Rationale);
  TC-161 (Method, Expected); TC-398 (Method, Expected). TC-161's and
  TC-398's Evidence cells were regenerated (silent trace cells, no act).
- Routed traced changes to `Accepted` rows: none.
- New `Drafted` rows owed a first acceptance: LLR-484, TC-571.
- Off-spine, shown by no sitting: IF-075 (`data`) and IF-129 (`notes`), both
  `Drafted`, their first acceptance already owed.

WI-1068 waits on this row; with it landed, its scope shows 26 rows, and the
seven rows above are owed beside it.

## Context

Filed on trunk on 2026-11-23 by the queue drill's coordinator, while
preparing WI-1024's sitting A (WI-1068). A routed traced cell (a
requirement's needs and boundary crossings, a design row's requirements, a
test case's verified rows and, since WI-1024, a requirement's or design
row's `constrains` link) is classed traced because it carries no prose, and
routed because whether the move changed what the row claims is a sitting's
judgement (`acceptance_record.SPINE_TRACED_CELLS`' comments; WI-1024's
plan, the specref: "Silent, the whole population would land unjudged").
The record keeps such a row at its recorded copy until an act names it
(WI-1060). But no sitting is shown the change:

- **The amendment brief renders accepted cells only**
  (`amendment_brief._scoped_chain_rows` keeps `c[0] in accepted`). Its
  docstring says traced cells are excluded because the classification
  "already answers" them, which predates routing: it is true of a silent
  traced cell, not a routed one. So sitting A would judge LLR-010's
  amended `detail` without being shown that the row now constrains IF-014,
  and blessing it would copy the link into the record unjudged.
- **A row whose only change is a routed link is in no surface.** The
  acceptance model (`trace.reaccept_model`) does not select LLR-017,
  LLR-022 or LLR-024, whose only change is a `constrains` link: they are
  absent from `docs/ratify/CURRENT.md`, `open-items.html` and the brief,
  while the snapshot prints them LEFT OWED and the act ledger lists them
  `kept`. A combined brief naming them as `amendment:` tokens drops them
  silently. Two answers to "what is owed" disagree.

Measured on trunk at `3f887ec5d`: 21 routed `constrains` changes owed by
WI-1024's slice 1, three of them on link-only rows; the model carries
LLR-010's `Constrains` triple but marks only `Detail` accepted.

Critiqued 2026-11-23 (Sol and Hydrogen;
`docs/reviews/2026-11-23-scope-critiques/WI-1069.md`): a `## Trust` section,
the deliverables kept together with the reason, and a coverage bound.

## Done-when

- [x] The acceptance model selects a row whose routed traced cell differs
      from its recorded copy, even when no accepted cell moved, and the
      operator surfaces built on it (the acceptance brief, `open-items.html`)
      list it as owed, naming the link that moved. A silent traced cell
      still selects nothing.
- [x] The amendment brief shows, for each row in its scope, every routed
      link that moved (before and after, by the cell's contract name)
      beside its accepted cells, and a row whose only change is a routed
      link is shown, not dropped; the question it asks of a link is the
      one the routing exists for (does the row's text state what it now
      points at?). The verdict's row grammar is unchanged.
- [x] The binding's judged-text identity covers what the brief showed, so
      a link changed after the verdict is not taken under it (`## Trust`
      below); the plan says how, from the code.
- [x] A brief scope naming a row with nothing to judge, accepted or routed,
      still refuses by name; a combined brief no longer drops a scoped
      row silently.
- [x] Coverage bound: the promises reach registries, records and bindings
      as supported workflows and the kit's own routes write them;
      hand-edited kit-written state (a record copy, a ledger, a binding) is
      outside them (PROCESS.md §6, "Review threat model").
- [x] Tests, red first, over a fixture with an accepted-text-only row, a
      routed-link-only row and a row with both, through the model, the
      operator surfaces and the amendment brief; the rows the change
      re-cuts (SR-146's and SR-178's design rows that say accepted cells
      only, LLR-167 and any the plan finds) are amended in text and owed
      to a sitting; a RESYNC entry.

## Trust

PROCESS.md §3, "When a guard is owed". Done-when 3 widens what a verdict's
binding identifies, and the binding decides whether an act may take a row
on a held rung, so the file's authority is stated here.

- **Producer.** The binding beside a verdict (`<verdict>.requested`),
  written when a sitting's request is bound (`adjudicate_brief.bind_pending`,
  `coordinator_adjudicate.bind_requested`), records one judged-text
  identity per row the composed brief shows (the brief's `JUDGED-TEXT:`
  lines, read back by `kitlib.sitting.recorded_identities`). Today an
  identity digests a row's accepted cells; this row extends it to the
  routed links the brief shows.
- **A failed or missing write.** A binding absent, unreadable, carrying no
  identity, not naming the row, or naming another digest than the
  committed row's: each consumer fails closed, as today. The held act's
  derivation refuses naming the row and both digests; the held-status
  exception reads the claim as not excepted; the record's kept-row reading
  does not count the row as settled.
- **Consumers, by path, and their shared ruling.** `adjudicate_act.py`
  (`_unbound_text`, the held re-accept), `held_status.py` (`_excepted`, a
  held CLARITY re-acceptance claim) and `acceptance_record.py` (the ruled
  rows a held verdict keeps). Each takes a row under a verdict only while
  the committed row's identity equals the bound one; one identity function
  serves all three, so a link changed after the verdict reads as changed
  text in every one. Released rungs and taken acts read no identity, as
  today.

## Scope answers

- **Kept together.** The model and surface change and the brief and
  binding change are one row on purpose: the brief reads the model, the
  binding digests what the brief shows, and one fixture (accepted-only,
  link-only, both) drives all three; landed apart, the first would list
  link-only rows that no brief could show.
- **Not in scope:** what a verdict on a routed link authorizes (the act
  already records a named row whole from live); the first-acceptance brief
  (a `Drafted` row shows every cell already).
- **Order.** WI-1068 (sitting A) waits on this row: its 21 routed links are
  the case that found it.
