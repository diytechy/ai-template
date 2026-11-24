+++
id = "WI-1070"
title = "The amendment brief shows a linked row's own text and the row each moved link names, so a sitting can judge the link"
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

Built on the maintenance branch `maint/wi-1070`, cut from `refactor_again`
at `ec188f984`, with the commit hooks on, under the plan
[`docs/plans/WI-1070/plan.md`](../../../plans/WI-1070/plan.md) (revision 1).
The coordinator approved it on 2026-11-24 before any build, D1 to D12
confirmed (D9 without the optional IF-131 requestor; D12 filed on trunk as
its own work item; TC-398's wording routed to WI-1071). No status moved, no
snapshot was taken, and no id was minted (D8). No decisions record: every
choice is stated by a row or by the approved plan.

- `19572aff6`: the plan.
- `dda7a821f`: the build: code, tests, rows, template, regenerated views,
  catalogue and evidence, the RESYNC entry, the deferred-import re-stamp and
  the plan's approval line.
- `674492855`: the need loader's example flag passed by name (the
  readability report's flag-axis warning; no behaviour change).
- The commit after it: this close-out.

**1. The linked row's own text.** A shown row with a moved adjudicated link
now lists, after its moved cells and links, its other nonempty accepted cells
as they now read, under `Unmoved accepted cells (with the cells above, the
row's whole accepted text):` (`amendment_brief._unmoved_cells`, rendered by
`_cell_block`; `(none)` when every accepted cell moved). A moved cell is not
repeated; a row whose moved cells are all accepted cells is shown as before.
The cells are classed by the identity's own classifier
(`acceptance_record.spine_cell_class`), the id and `Status` left out, and a
test pins that a shown row's cells and links, with its unmoved links (which
the block's head names as chains), digest to its judged-text line. On this
tree LLR-017 now reads its link, then its `Detail` and `Title`.

**2. The rows the moved links name.** A new required template slot,
`{linked}`, under `--- ROWS THE MOVED LINKS NAME (context for the LINKS
question: not under judgement, and in no JUDGED-TEXT identity) ---` between
the rows and the identity lines (D2), lists once each id a moved link names,
before or after, in tier then id order, naming the shown rows, cells and
sides that name it (`_linked_rows`). Per tier (`LINKED_TIERS`, D3): a need by
`Need`; a boundary crossing by `Direction`, `Entity` (with the entity's
`Name` when live) and `Carries`; a requirement by `Title` and `Requirement`;
a design row by `Title` and `Detail`; an interface by `Channel`, `Owner` and
the `Contract IF-###:` body one file states (`arch_interfaces.contract_homes`
then `gen_arch_map.file_contracts`, imported where read), its `Data` cell
standing in when none is (no surface, none or two stated, a refused header).
Each listed cell is on one line, whitespace collapsed, clipped at 2,400
characters at a space with `… [clipped at 2400 of N characters]` (D4); an id
naming no live row of those tiers is listed as `names no live row`; a named
row also shown for judgement as `shown above for judgement`; with no moved
link the section reads `(no moved link in this brief names a row)`. The
interfaces and external registries (off-spine) are read; their rows are
context, with no identity line and no verdict line. The template's LINKS
paragraph says so and asks for no verdict line on a listed row. The combined
brief composes its amendment section through the same template, so it
carries the listing.

**3. The identity.** Unchanged: `accepted_text_digest` and every reader of a
binding are untouched (D6, D10). The identity heading now reads `JUDGED
TEXT (the identity of each row shown for judgement: its accepted cells and
adjudicated links; the rows listed as context above are not in it)`. A
listed cell holding an identity-shaped line adds no identity to the binding
(tested). Over the 28 owed tokens the brief states 24 identity lines before
and after, 22 of them byte-identical; the two that changed are LLR-167's and
TC-161's, whose text this row amended. A binding written before the change
reads as before.

**4. The rows.** Amended in text, as the plan's §4 wrote them: LLR-167
(Detail, Rationale), TC-161 (Method, Expected), LLR-359 (Detail: "for each
row it shows for judgement", D7). TC-161's `Evidence` cell regenerated (a
silent trace cell). TC-398's "per shown row" is routed to WI-1071 (not
touched here).

**5. Tests and the RESYNC entry.** 20 new tests and one changed one in
`tests/test_amendment_brief_links.py` (in process, smoke tier), over the
fixture `tests/routed_link_fixtures.py`, which gains the rows a link names
(two needs, an entity and a crossing, IF-001 with a data cell alone, IF-002
with a contract stated under the default scan root); the stubbed amendment
assembler in `tests/test_done_when_blessing.py` returns the new slot. The
RESYNC entry is anchored `[since ec188f984]`; `scripts/check_resync.py`
reads it OK (`3 shipped path(s) changed; entry anchored at ec188f984`).

**6. Coverage bound.** The promises reach registries, recorded copies and
bindings as the kit's own routes write them, and contract statements as the
contract grammar admits them; a hand-edited recorded copy, act ledger or
binding is outside them (PROCESS.md §6, "Review threat model"). LLR-167
states it in its closing sentence.

**7. The measure.** The brief's dry compose of WI-1068's combined sitting
(nothing written under `docs/`), at the base `ec188f984` and at the build
`dda7a821f`. The compose drops the tokens the eighth sitting settled without
refusing (the 15 blessed amendments are named not shown; the 11 accepted
first acceptances add nothing), so the figure of record is the 28 owed
tokens (the 24 amendments left owed and the four returned first
acceptances); all 54 are reported beside it (D11).

| Tokens | Base | Tip | Change |
|---|---|---|---|
| 28 owed (of record) | 188,615 | 218,919 | +30,304 (+16.1%) |
| all 54 | 188,802 | 221,416 | +32,614 |

Over the 28: the amendment section 83,286 -> 113,576; the listing 21,802
characters, 26 interfaces listed (the 21 rows' `Constrains` targets), none
clipped, none naming no row; 21 unmoved lists, 4,311 characters; LLR-167's
and TC-161's own blocks +1,922 and +1,658 (their amendments); the template
text about +600; the first-acceptance section +14 (LLR-359's new words in a
chain). Over the 54, LLR-359's block (2,274) is shown as well, now amended.
<!-- fig: cmd=".venv/Scripts/python.exe scripts/coordinator/compose_lane.py WI-1068 combined <the 28 owed tokens | all 54 of WI-1068's spec> <WI-1068's 32 sr_refs> docs/reviews/wi-1068-dry/001-ADJUDICATE-dry.md <scratch>; a section and line count over the output" rev="ec188f984 (base) and dda7a821f (tip)" -->

**Deviations from the plan, each with its reason.**
- The digest-equality pin adds the row's unmoved links to the cells it
  reads off the block: the identity covers every routed cell, and unmoved
  links are not shown (the plan said "the shown cells and links digest");
  TC-161's method says "with its unmoved links".
- One test beyond the plan's table: a linked row whose every accepted cell
  moved lists `(none)` (the plan's §1 stated the case). It was written after
  the code, so it has no red line; it passed on its first run.
- `amendment_brief.py` grew 258 -> 405 SLOC (the plan guessed about +110),
  far under the 1,000 watch line; its size ratchet needed nothing.
- Forced by a check: `tests/test_import_layers.py`'s deferred-import window
  re-stamped 44 -> 46, with its reason in the test. The approved D9 reads
  the contract harvest through two function-body imports
  (`amendment_brief -> arch_interfaces`, `-> gen_arch_map`, inside
  `_stated_contracts`), so a brief naming no interface pays nothing; the
  base read 44, at the top of the window. Neither module reaches the brief,
  so no cycle or layer edge grew; `cross_component_findings` reads 0 and
  `check_trajectory.py --strict` is clean.
- The readability report (advisory) named a positional `False` this row
  added; `674492855` passes it by name. It still reports, against the
  stamped flag-axis baseline, positional literals that predate this row in
  the three touched files (`amendment_brief.py` 1, from WI-791's
  `adjudication_action(True, v)`; `adjudicate_brief.py` 1;
  `tests/test_done_when_blessing.py` 10); none is gating and none is this
  row's.
- The IF-115 contract sentence in `adjudicate_brief.py` and the regenerated
  `docs/interface-reference.md`, as the plan's §7 named.

**Red first.** The new and changed tests before any code change, on the
fixture alone: `19 failed, 9 passed in 4.33s` (the 9: the eight unchanged
WI-1069 tests and the accepted-only guard), each failing for its reason:
the link-only block without its unmoved cells (`assert '- LLR LLR-00...after:
IF-001' == '- LLR LLR-00...tle: Design 2'`), `ValueError: substring not
found` for the unmoved label, the digest of the shown cells unequal to the
identity (`('LLR-002', {'Constrains': 'IF-001', 'SR-Refs': 'SR-002'})`),
`KeyError: 'linked'` for each listing test, and the template's missing
heading and `{linked}` slot.
<!-- fig: cmd="python -m pytest -q -p no:cacheprovider --basetemp <scratch> tests/test_amendment_brief_links.py --tb=line" rev="19572aff6 plus the uncommitted tests and fixture, before any code change" -->

**Tests run** (the worktree's venv, `-p no:cacheprovider`, `--basetemp`
under `D:/review-tmp/2026-11-24-wi1070/`):
- After the code: the link module, `tests/test_done_when_blessing.py` and
  `tests/test_prompts.py`: `238 passed in 890.57s (0:14:50)`.
- The 42 modules: those importing `amendment_brief` or `adjudicate_brief`
  (grep and `trace.py --tests-for`), those holding TC-161's and TC-398's
  tests, `tests/test_routed_link_owed.py` (the shared fixture), and
  `test_import_layers`, `test_module_size_ratchet`, `test_complexity_ratchet`,
  `test_dogfood_sync`, `-n auto`: `1 failed, 2394 passed, 17 skipped in
  2377.34s (0:39:37)`. The one: the deferred-import window (above),
  re-stamped; rerun with the link module, `36 passed in 9.57s`.
- After `674492855`, the link module: `29 passed in 4.89s`.
- `check_trajectory.py --root . --strict`: exit 0, `clean (1068 work
  item(s), 940 done (88%), 37 cancelled, graph acyclic)`.
- `trace.py --root . --strict`: exit 1 on one finding, LLR-484's `such as`
  (see Left), the same at the base.
- `run_menu.py smoke`: exit 1 at its first step, that same `trace.py
  --strict`, so its chain stopped before the tier. Its remaining steps run
  by hand on `674492855`: `check_docs: OK - 3707 doc(s), 3835 intra-repo
  link(s), 0 broken.`; `check_resync: OK, 3 shipped path(s) changed; entry
  anchored at ec188f984`; `check_smoke_budget.py --mode warn`: `3947 passed,
  3 skipped, 18 warnings in 192.10s (0:03:12)`, exit 0, CPU 790.0 s over the
  540 s budget (reported only, on a box shared with another builder). The
  tier's 3,950 cases sit under `max-tests = 4060`. The unfiltered suite is
  the coordinator's, before the merge.
<!-- fig: cmd="python -m pytest -q -n auto -p no:cacheprovider --basetemp <scratch> <the 42 modules>; python project-trajectory/scripts/run_menu.py smoke; then check_docs.py --root . --stale, scripts/check_resync.py, scripts/check_smoke_budget.py --mode warn" rev="dda7a821f's tree (module run, uncommitted then) and 674492855 (smoke steps), 2026-11-24" -->

**Acts owed to automated adjudication.**
- Amendments to `Accepted` rows (text only): LLR-167 (Detail, Rationale);
  TC-161 (Method, Expected); LLR-359 (Detail).
- Routed traced changes to `Accepted` rows: none.
- New `Drafted` rows owed a first acceptance: none.

The 21 link rows, LLR-167 and TC-161 stay owed from the eighth sitting; the
sitting that re-judges them is filed when this row and WI-1071 land.

**Left.**
- The finding D12 named: a judged cell is rendered verbatim, so a registry
  cell holding a line that opens `JUDGED-TEXT: <id> <digest>` would be read
  by the binding as an identity line. Filed by the coordinator on trunk as
  its own work item; not fixed here (the listing's one-line rule is).
- TC-398's "one judged-text line per shown row" -> "per row shown for
  judgement", routed to WI-1071.
- `trace.py --root . --strict` exits 1 at this base and at the tip on one
  finding outside this row: `FINDING (requirement form): LLR LLR-484 Detail
  uses 'such as'` (LLR-484 was accepted at the eighth sitting's act). Shown
  on an export of `ec188f984` with no change of this branch.

## Context

Filed on trunk on 2026-11-24 by the queue drill's coordinator, to answer
the eighth automated adjudication sitting's verdict (WI-1068, sitting A,
Gemini Neon; the specref), its first `## amendment` disposition.

WI-1069 made the amendment brief show each moved routed link (before and
after, marked `(link)`) and a row whose only change is a link, and its
template asks of a link the question its routing exists for: "does the
row's text state what the link now points at?". The sitting could not
answer it. For each of the 21 rows gaining a `constrains` link it ruled
MEANING, not blessed, saying the brief supplies neither the interface the
link names nor, for a link-only row (LLR-017, LLR-022, LLR-024), the row's
own text. The coordinator confirmed it from the composed brief: the
amendment section lists moved cells only, so LLR-017 reads in full
"Constrains (link): before (empty), after IF-032". The same gap is why the
sitting did not bless LLR-167 (the brief's contract asks a question it does
not equip the judge to answer) and TC-161 (it verifies that contract).

All 21 rows, LLR-167 and TC-161 stay `Accepted` at their recorded text,
owed (the act `WI: WI-1068` left them owed). F-4's slices 2 to 4 add many
more `constrains` links; every one meets the same gap at its sitting
unless this row lands first.

Critiqued 2026-11-24 (Sol and Hydrogen;
`docs/reviews/2026-11-24-scope-critiques/WI-1070.md`): `planmode` is `single`, and the
coverage bound is a Done-when item.

## Done-when

- [x] For each row in an amendment brief's scope with a moved routed link,
      the brief shows the row's current accepted text (every accepted cell,
      not only the moved ones), so a link-only row is judged against its own
      text.
- [x] For each id a moved routed link names, before or after, the brief
      shows that row's identifying text (its title and the cell that states
      what it is: an interface's contract, a requirement's requirement, a
      design row's detail, a need's statement, a crossing's description), as
      context, not as text under judgement; an id that names no live row is
      shown as such. The plan settles, from the code, which cell each tier
      shows and the bound on its size.
- [x] The binding's judged-text identity is unchanged in what it covers (a
      row's accepted cells and its routed links), or the plan argues a
      change under the `## Trust` section WI-1069 wrote; the brief says
      which shown text is context and not under the identity.
- [x] LLR-167 and TC-161 state and verify the new contract (text only, no
      code names); any other row the plan finds saying the brief shows moved
      cells only is amended in text. Every amended row is owed to a sitting.
- [x] Tests, red first, over a link-only row and a row with both, through
      the amendment brief and the combined brief; a RESYNC entry if a
      shipped file or template changes.
- [x] Coverage bound: the promises reach registries, records and bindings
      as supported workflows and the kit's own routes write them;
      hand-edited kit-written state (a record copy, a ledger, a binding) is
      outside them (PROCESS.md §6, "Review threat model").
- [x] The Deliverable measures the brief over WI-1068's 54 tokens before
      and after (characters), so the next sitting's split is known.

## Scope answers

- **Not in scope:** re-sitting the 21 rows (a sitting row filed when this
  lands, with WI-1071's rows); the first-acceptance brief, which already
  shows each row whole with its chain.
- **Order.** Lands before the sitting that re-judges WI-1068's link rows,
  and before any sitting judging F-4's later slices' links.
