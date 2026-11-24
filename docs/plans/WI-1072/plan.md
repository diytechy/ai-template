# WI-1072 plan, revision 1: only the composer's own identity lines reach a sitting's binding

Written in the worktree `D:/ai-template-wt-wi1072`, branch `maint/wi-1072`,
cut from `refactor_again` at `c31642461`. `planmode = "single"`: this commit
carries the plan alone, and nothing else changes until the coordinator's
go-ahead.

Read in full: the spec `docs/work/queued/WI-1072-identity-line-forging.md`
(its `## Trust` included); its scope critique
`docs/reviews/2026-11-24-scope-critiques/WI-1072.md`; WI-1070's plan
(decision D12, the finding) and WI-1069's spec (`## Trust`, the binding's
producer and consumers). Code read: `amendment_brief.py` (whole);
`adjudicate_brief.py` (`compose`, `combined_values`, `bind_pending`,
`requested_identities`, `record_outcome`, `first_acceptance_values`,
`_render_chain`, `_render_acceptance_rows`, `done_when_values`,
`_spec_context`, the IF-115 contract); `kitlib/sitting.py` (the binding:
`write_binding`, `render_requested`, `read_identities`,
`recorded_identities`); the binding's consumers (`adjudicate_act._derive`,
`held_status._bound_clarity`, `acceptance_record.text_as_bound` and its one
caller `intake._held_act_drafts`); both routes that bind
(`agent_loop`'s adjudication arm, `coordinator_adjudicate._inputs` and
`bind_requested`, and `scripts/coordinator/compose_lane.py`, which writes
the coordinator's brief file); `plan_briefs.fill_hat_slot` and
`sitting_tail`; `prompts.fill` and `strict_check`; the amendment,
first-acceptance and combined templates. Rows read: SR-178, SR-208;
LLR-167, LLR-359; TC-161, TC-398. Tests read: `test_amendment_brief_links.py`,
`routed_link_fixtures.py`, the identity cases of `test_adjudicate_brief.py`,
`test_done_when_blessing.py`'s combined-sitting cases and assembler stub.

## Ids

None minted. LLR-516 to LLR-518 and TC-613 to TC-616 stay unminted (D5). No
SR, IF, DA, SUR or WI id.

## Measured (this branch's base, `c31642461`)

Read-only, the worktree's Python 3.11. The fixture is
`tests/routed_link_fixtures.py`'s four accepted chains (SR-00n, LLR-00n,
TC-00n, recorded whole), with `move_all`'s moves (LLR-001's detail, LLR-002's
`constrains` link, LLR-003 both, LLR-004 trace cells only). A cell's text is
given lines of the form `JUDGED-TEXT: <id> sha256:0123456789abcdef`, each on
its own line after the cell's first line; each brief is composed through
`adjudicate_brief.compose` and read by the binding's one reader,
`requested_identities`.

**The reader.** `^JUDGED-TEXT: (\S+) (\S+)[ \t]*$`, multi-line, over the
whole composed prompt, into a dict, so a later line replaces an earlier one
for the same id. A judged cell is rendered verbatim after `    - <name>: `
(or `    - before: ` / `    - after: `), so every line of a multi-line cell
after its first starts at column 0.

**Amendment brief**, scope `LLR-001;LLR-002`, LLR-001's moved detail holding
lines naming LLR-001 (its own row), LLR-002 (another shown row) and LLR-004
(a row not shown):

```
identity-shaped lines in the prompt, in order:
  JUDGED-TEXT: LLR-001 sha256:0123456789abcdef   <- the cell
  JUDGED-TEXT: LLR-002 sha256:0123456789abcdef   <- the cell
  JUDGED-TEXT: LLR-004 sha256:0123456789abcdef   <- the cell
  JUDGED-TEXT: LLR-001 sha256:5d2ce715a6e6b3b7   <- the identity section
  JUDGED-TEXT: LLR-002 sha256:3919e77c43c3681d   <- the identity section
bound: LLR-001 = 5d2ce715a6e6b3b7, LLR-002 = 3919e77c43c3681d (genuine, the
identity section comes after the rows), LLR-004 = 0123456789abcdef (ADDED;
its committed digest is 3fffe856e0d7920b)
```

**First-acceptance brief**, scope `LLR-005`, a `Drafted` LLR-005 under SR-001
(dial `DevStg-Needs`) whose detail holds lines naming LLR-005, LLR-001 (shown
as chain evidence) and LLR-004 (not shown). The rendered cell line is
`    - Detail: Design row 5 adds.`, the three forged lines following at
column 0. The brief writes no identity line; bound: LLR-001, LLR-004 and
LLR-005, all three ADDED.

**Combined sitting**, scope `amendment:LLR-002;first-acceptance:LLR-005`,
LLR-005's detail holding lines naming LLR-005, LLR-002 (shown in the earlier
amendment section) and LLR-004:

```
  JUDGED-TEXT: LLR-002 sha256:3919e77c43c3681d   <- amendment section
  JUDGED-TEXT: LLR-005 sha256:0123456789abcdef   <- first-acceptance cell
  JUDGED-TEXT: LLR-002 sha256:0123456789abcdef   <- first-acceptance cell
  JUDGED-TEXT: LLR-004 sha256:0123456789abcdef   <- first-acceptance cell
bound: LLR-002 = 0123456789abcdef (REPLACED; committed 3919e77c43c3681d),
LLR-004 and LLR-005 ADDED
```

**Not only cells.** The same sitting with a Done-when section instead
(`amendment:LLR-002;done-when:WI-007`, the done-when assembler stubbed to
its slot set, its `{context}` holding `A widget.` and a line naming LLR-002):
bound LLR-002 = `0123456789abcdef`, REPLACED. The real `{context}` is the
spec's `## Context` lines verbatim (`_spec_context`), so a lane's own spec
reaches the binding the same way. Other non-composer text in the same
prompts: the perspectives block (`{hats}`, after `{identity}` in the
amendment template, and the combined sitting's tail after every section) from
the hat roster; `{questions}` from the shipped questions home; an operator
override of any template; assumption case chains (`trace.assumption_brief_lines`).

**What it buys an attacker.** A row's digest is computable by anyone who can
read the row. A line naming a row not shown, carrying that row's current
digest, gives the binding an identity for a text the sitting never saw; a
line placed after the genuine one, carrying the digest of a text to be
committed later, makes the binding bless that later text. Either way a held
CLARITY act (or the held-claim exception) could take a row whose text the
verdict never judged, if the verdict names the row.

**Today's population.** <!-- fig: cmd="python census.py (scratch: every string cell of docs/requirements/*.toml, docs/test/*.toml and docs/*.toml; every docs/work/**/*.md and docs/archive/work/**/*.md; every docs/reviews/**/*.brief.md and *.requested), matched against the reader's own pattern" rev=c31642461 -->
13,514 registry cells: none holds an identity-shaped line. 1,081 specs: none
holds one at column 0. 4 stored briefs: no identity-shaped line outside the
block after their `--- JUDGED TEXT` heading, no id named twice. 214
bindings, 37 of them carrying an identity cell.
<!-- fig: cmd="git log --oneline -S'JUDGED-TEXT' -- docs/requirements docs/test docs/archive/last_accepted" rev=c31642461 -->
No commit in this repository's history ever put the keyword in a registry
or a recorded copy, so no binding here can have recorded a forged identity.

## 1. The mechanism (Done-when 1)

**A refusal at compose, over the whole composed text.** `compose` is the one
path both routes take (the loop's adjudication arm composes then binds; the
coordinator's `compose_lane.py` composes then writes the brief file
`coordinator_adjudicate.py adjudicate --brief-file` binds). After the fill,
it reads the composed text with the binding reader's own pattern and
compares what it finds with what the composer wrote:

- a single-kind brief: the lines of its `{identity}` slot (the amendment
  brief's), or none (every other brief);
- a combined sitting: the text of its sections, each of which was composed by
  `compose` and so already passed this check, so the sitting's own check
  covers only what it adds itself (its template and the perspectives tail).

Any identity-shaped line beyond those (as a multiset, so a duplicate of a
genuine line counts too) refuses the brief, naming the brief and each row id
such a line names. A refused section refuses the sitting, named, as today
(`combined_values`: "the <kind> section: ..."). A refusal is a hold (rule
3): the loop pages with the reason; `compose_lane` prints `REFUSED` and
writes no brief file, so nothing is bound.

**Why this one.** Three ways were open (the spec's Done-when 1):

1. *Where the reader looks* (only between the identity heading and the
   section's end). The delimiters are text too: a cell can carry the heading
   and `--- END ---` lines. In a combined sitting later sections (first
   acceptance, Done-when, perspectives) follow the amendment section, and in
   the amendment brief the rows precede the identity section, so neither a
   "first section" nor a "last section" rule is safe in both directions
   without a refusal anyway. The heading is template wording an operator
   override may change, and the reader's contract would change for every
   prompt it reads, the coordinator's brief files included.
2. *How a judged cell is rendered* (indent or collapse its continuation
   lines). Judged text is shown verbatim on purpose (the amendment
   template's `{rows}` note: the unmoved cells are "judged text, inside its
   identity, never clipped"; the digest is over the registry text), and
   collapsing, as WI-1070 does for context, would flatten multi-line
   details and lists the judge reads. It also closes only the sites it is
   applied to: `_cell_block` (the amendment's chained, unchained and removed
   rows), `_render_acceptance_rows` and `_render_chain` (first acceptance),
   `trace.assumption_brief_lines`, and none of the non-cell text above (a
   spec's Context, the perspectives, the questions, an override). A new
   renderer would reopen the gap silently.
3. *A refusal at compose* reads the one artifact that is bound, after every
   slot is filled, with the reader's own pattern, so it covers every source
   of text and every future one at one point, keeps judged text verbatim, and
   leaves the binding, its reader and its consumers unchanged. Its cost is a
   hold for a brief whose text holds a line exactly of the identity's shape
   at column 0; the census above found none anywhere, and the remedy is to
   reword that line. This is the spec's `## Trust` clause: "a brief the
   plan's mechanism cannot compose safely is refused at compose, never bound
   with a guess".

**Per brief kind.**
- *Amendment*: its `{identity}` lines are the only ones allowed; a line in a
  moved cell's before or after, an unmoved cell, a removal block, the context
  listing (already one line per cell since WI-1070, so it cannot produce one),
  the perspectives or the questions refuses.
- *First acceptance*: writes no identity line, so any identity-shaped line
  refuses; its binding then never carries an identity cell.
- *Combined*: each section is checked as composed (an amendment section
  against its own `{identity}`, every other section against none), then the
  sitting against its sections. The forged line after the genuine one (the
  measured replacement) is refused in the first-acceptance or Done-when
  section that carries it.
- *Every other brief* (disposition, evidence-gap, consolidate, rejudge,
  done-when alone, dispute): the same rule with no identity line allowed (D2).
  None of their bindings' identities is read today (every consumer reads an
  identity only for a row an amendment part rules), so this changes no act;
  it makes "only the composer's lines enter a binding" true of every binding.

**A binding written before this change** reads as it did: its cell format,
`read_identities`, `recorded_identities` and the three consumers are
untouched, and no reader re-derives a binding from a stored brief. The
census shows no binding here could carry a forged identity.

**Text added after composition.** The coordinator's recipe appends text to a
composed brief file (a disposition's `## Owner route`; a combined sitting's
arms map) before `adjudicate --brief-file` binds it. That text is not the
composer's and is outside this guarantee; LLR-359's scope sentence says so
(D6).

## 2. Code, file by file

- **`project-trajectory/scripts/adjudicate_brief.py`** (the only code file):
  - `_identity_refusal(brief, text, written)`: the multiset of
    `_JUDGED_TEXT_RE.findall(text)` less that of `written`; any remainder
    returns a reason naming the brief and each id
    (`"the <brief> brief's text carries <n> line(s) shaped as a judged-text
    identity that its composer did not write, naming <ids>: a row's cell or
    other text it shows holds them, and the binding would record them as
    judged; reword that text, or rule on the rows by hand"`), else None.
  - `compose`: takes the combined sitting's reported section text out of the
    values before the fill (a key that is never a slot, as
    `plan_briefs.HAT_PARENTS` is; D9), fills as today, then returns the
    refusal when `_identity_refusal(brief, text, written)` gives one, where
    `written` is that reported text, else the `{identity}` value, else `""`.
  - `combined_values`: reports its sections' composed text (the tail
    excluded) under that key.
  - Docstrings: `compose` (the rule, `Implements:` gains SR-178 and LLR-359),
    `combined_values`, `requested_identities` (a composed brief carries no
    line of the shape but its composer's), and the IF-115 contract body (one
    sentence after the identity sentence: "a composed brief whose text
    carries any other line of that shape is refused, naming the row it
    names, so the binding records only the lines the composer wrote"; D7).
  - Size: SLOC 782 now; about +20, under the 1,000 threshold, no baseline
    entry. `compose`'s complexity stays under the limit (the check is one
    call).
- **Unchanged**: `amendment_brief.py`, every template and `prompts/CATALOG.md`
  (so no retained adjudicator's identity moves), `kitlib/sitting.py`,
  `agent_loop.py`, `coordinator_adjudicate.py`, `acceptance_record.py` and
  every function WI-1045 moves.
- **Generated**: `docs/interface-reference.md` (the IF-115 body), regenerated
  by `trunk_step.py --regen` with the registry edits.

## 3. The rows (Done-when 3)

Searched the requirement, design, test-case and interface registries for a
row stating which lines enter a binding (`identity line`, `judged-text`,
`identity-shaped`): LLR-359 says the amendment brief renders one identity
line per row shown for judgement and that reservation writes "those
identities"; it does not say no other line enters. LLR-167 states the
brief's contents and "one judged-text identity line per row shown for
judgement (LLR-359) and none for a listed row"; TC-161 drives the listed
cell holding an identity-shaped line (the context listing's one-line rule).
Neither states the rule, so LLR-359 is amended (the spec names it), and
TC-398, which verifies it, with it. LLR-167 and TC-161 are unchanged (D4).

Both rows checked under the three row rules: no code name in either row's
text after the edit (none inherited: LLR-359 names LLR-484 only, an id;
TC-398's evidence cell is a trace cell); every added clause is driven by a
test TC-398 names (§4); nothing beyond or against the parents.

### LLR-359 (Accepted; Detail and Rationale amended; title unchanged)

**Detail**, whole (the third sentence is new; the last sentence's scope
names a composed brief and text added to one):

> A row's accepted-text digest is the identity of the text a sitting judges on it, formed from its nonempty accepted cells and its nonempty adjudicated links (LLR-484), excluding its id and Status: carrier representation and an absent versus empty cell give the same identity, a moved accepted cell or adjudicated link changes it, and a moved trace cell no adjudicator judges does not. An amendment brief renders one judged-text identity line for each row it shows for judgement. A composed brief of any kind whose text holds a line of that shape its composer did not write for a row it shows for judgement, whether in a shown row's cell, in a later section of a combined sitting or anywhere else in its text, is refused at composition naming the row that line names, so a binding records only the identity lines the composer wrote. Reservation writes those identities in the binding, and rewriting the binding as recorded or failed preserves them. A held CLARITY re-acceptance is actable only when the accepted binding's identity equals the committed row's digest, and an absent, malformed or unequal identity yields a refusal before launch naming the row, an unequal one naming both digests; a held acceptance claim is excepted only under a CLARITY verdict whose binding records the row's equal digest. The contract covers registries, recorded copies, composed briefs and bindings the kit's own routes write; a hand-edited recorded copy, act ledger, composed brief or binding, text appended to a composed brief included, is outside it.

**Rationale**, whole (the last sentence is new):

> A verdict about one text cannot authorize a later text unless the text the verdict saw has a stable identity carried from brief reservation through the later act. The adjudicated links are in the identity because an act naming the row records them with its accepted text (LLR-245), so a link moved after the verdict would otherwise be recorded under a verdict that never judged it. Comparing the committed identity with the accepted binding keeps a changed, absent or malformed identity from being read as the judged row. Only the composer's own identity lines may reach the binding because a judged cell is shown verbatim and may span lines, and a composed brief carries other text that is not the composer's (a later section, a spec's context, a perspectives question): a line of the identity's shape there would add an identity no shown text has or, after the genuine line, replace one, and a held act could then take a row whose text the verdict never judged; refusing such a brief keeps judged text verbatim and closes every source of text at one point, where reshaping the text would close only the places it reshaped.

Parent check. SR-208 requires a held acceptance claim to be "a CLARITY
re-acceptance bound to the row's judged text"; the new clause is what makes
the bound identity the judged text's, so it serves the parent and goes no
further. SR-178 (drift reported against the recorded copy) is untouched by
it. Every clause the row stated is kept; the scope sentence widens to the
composed brief the new clause speaks of.

### TC-398 (Accepted; Method and Expected amended; Evidence regenerated; verifies unchanged)

**Method**, whole (the last sentence is new):

> Digest a requirement row, then the same row with its id, its Status and a trace cell no adjudicator judges changed, with an empty cell against an absent one, and on its other carrier; then with an accepted cell moved, and with an adjudicated link moved. Compose an amendment brief over committed rows whose accepted cells moved, and one over a row whose adjudicated link alone moved, and read their judged-text lines. Reserve a sitting from a composed prompt, round-trip and read its binding, and rewrite it as recorded and as failed. Derive the held act of a CLARITY verdict whose binding equals the committed row, one whose row's accepted cell moved after it, one whose row's adjudicated link moved after it, one whose binding was written over the row's accepted cells alone, one with no identity and one with a malformed identity cell, reading each refusal for the row and, where the identities are unequal, for the digest the binding records and the committed row's digest; and launch the act turn over one whose text moved. Judge a held acceptance claim under a CLARITY verdict binding its equal digest, and one whose adjudicated link moved after the verdict. Compose an amendment brief whose shown row's moved cell, a first-acceptance brief whose awaiting row's cell, and a combined sitting whose later first-acceptance section's row cell holds a line of the judged-text identity's shape, each in turn naming that row, another row the brief shows and a row it does not show; a combined sitting whose Done-when section's context holds one naming the amendment section's row; a combined sitting whose own template holds one; and every other routed brief kind with one of its slots holding one; then compose the amendment, first-acceptance and combined briefs again without the line and read their judged-text lines.

**Expected**, whole (the last sentence is new):

> The digest has the sha256 shape and is unchanged by the id, the Status, the unjudged trace cell, empty against absent and the carrier, and changes for the accepted cell and the adjudicated link. Each brief states one judged-text line per row shown for judgement, carrying that row's digest as its registry holds it, the link-only row's covering its link. The binding records the prompt's identities, reading its requested kinds ignores them, and both rewrites keep them. The held act is owed only under the equal binding; the moved cell, the moved link and the accepted-cells-only binding of a row carrying a link are unequal identities, and each refuses it naming the row, the digest its binding records and the committed row's digest; the missing and the malformed identity each refuse it naming the row; and the act turn refuses before launch. The claim is excepted under the equal binding and not when the link moved. Each brief holding a line of the identity's shape its composer did not write is refused at composition, naming the row that line names; without the line, each brief's judged-text lines are exactly its composer's, none for the first-acceptance brief.

Parent check: every added clause matches LLR-359's new sentence (the three
kinds and their three targets, a later section, the sitting's own text, any
kind, the row named, nothing bound) and nothing beyond it; it verifies the
same rows. Its `Tier` stays `Full` (its git cases); its `Evidence` cell is
regenerated, a trace cell.

## 4. The tests (Done-when 2), red first

"Red" is failing on this base before the code changes; each red line is
quoted in the Deliverable. Every test is tagged `Implements: TC-398`.

| Module | Test, one line | Red? |
|---|---|---|
| `tests/test_judged_identity_lines.py` (new; in process over `routed_link_fixtures`; smoke tier) | `test_an_amendment_cell_holding_an_identity_line_refuses_the_brief[own, shown, unshown]`: LLR-001's moved detail holds a line naming LLR-001, LLR-002 (shown) or LLR-004 (not shown); compose returns no text and a reason naming the amendment brief and that id | red (composes today; the unshown case adds LLR-004) |
| same | `test_a_first_acceptance_cell_holding_an_identity_line_refuses_the_brief[own, shown, unshown]`: a Drafted LLR-005 under SR-001 whose detail names LLR-005, LLR-001 (chain evidence) or LLR-004 | red (composes; each adds an identity) |
| same | `test_a_combined_sittings_later_section_holding_an_identity_line_refuses_it[own, shown, unshown]`: `amendment:LLR-002;first-acceptance:LLR-005`, LLR-005's detail naming LLR-005, LLR-002 (the earlier section's row) or LLR-004; the reason names the first-acceptance section and the id | red (composes; the shown case replaces LLR-002's digest) |
| same | `test_a_combined_sittings_own_template_holding_an_identity_line_refuses_it`: an operator override of the combined template carrying a line naming LLR-004; refused naming it (the sitting-level check, beyond its sections) | red |
| same | `test_every_routed_brief_refuses_an_identity_line_in_a_slot[<each routed brief but combined>]`: each brief's assembler stubbed to its template's slot set, one slot holding a line naming LLR-004 (the amendment stub's `{identity}` holding one genuine line); refused naming LLR-004 | red |
| same | `test_without_the_line_each_brief_binds_only_its_composers_lines`: the amendment, first-acceptance and combined briefs above composed with clean cells; the reader returns exactly the `{identity}` slot's ids (LLR-001 and LLR-002; none; LLR-002) | green before and after: the control that each refusal is the line's |
| `tests/test_done_when_blessing.py` (one case; git; slow tier) | `test_a_combined_sittings_done_when_context_holding_an_identity_line_refuses_it`: the stubbed amendment section writes LLR-1's line, the lane's spec Context holds a line naming LLR-1 with another digest; refused naming the done-when section and LLR-1 | red (composes; replaces LLR-1's digest) |

Unchanged and still passing: `test_no_listed_row_gets_an_identity_line`
(the context listing collapses its forged line onto one line, so it composes
and binds SR-001 alone), the identity and binding cases of
`test_adjudicate_brief.py`, `test_held_status*.py`, `test_adjudicate_act.py`,
`test_coordinator_act.py`, `test_intake_held_act.py`.

Run at the build (builder rule 5): every test module importing
`adjudicate_brief` (grepped, and `trace.py --tests-for adjudicate_brief`),
the modules holding TC-398's tests, `test_done_when_blessing.py`, the new
module, `test_import_layers.py`, `test_module_size_ratchet.py`,
`test_complexity_ratchet.py`, `test_dogfood_sync.py`; `trace.py --strict`,
`check_trajectory.py --strict`; `run_menu.py smoke` once at the end. The new
module adds about 20 in-process cases to the smoke tier; if that crosses
`[smoke-budget] max-tests`, I stop and report rather than re-stamp (D8).

## 5. The RESYNC entry (Done-when 4)

`adjudicate_brief.py` ships, so `project-trajectory/RESYNC_PACK.md` gains,
after the last entry:

> ### A brief whose text carries a judged-text identity line its composer did not write is refused [since c31642461]
>
> *(Anchored at the preceding commit: the change lands in the commits after it.)*
>
> **What changed.** An adjudication brief is refused at composition when a
> line of its composed text has the shape of a judged-text identity line
> (`JUDGED-TEXT: <row id> <digest>`) and is not one its own identity section
> wrote: a line of a registry cell shown verbatim, of a later section of a
> combined sitting (a first-acceptance row's cell, a Done-when change's
> context), of the perspectives or of a template override. The refusal names
> the row id the line names and, in a combined sitting, the section. Before,
> the sitting's binding recorded such a line as an identity: one naming a row
> not shown added an identity, and one after the genuine line replaced that
> row's digest. The binding's format and every reader of it are unchanged.
>
> **What to do.** Nothing, unless a row, spec or hat roster of yours holds
> such a line: its sitting is then held (the loop stops asking for an
> operator with the reason; the coordinator's composer prints it and writes
> no brief). Reword that line, for example by indenting it or quoting it
> inline, and compose again. Bindings written before the upgrade read as
> before. No template changes, so no retained adjudicator drains.
>
> **Kit-owned files — overwrite:** `scripts/adjudicate_brief.py`.
>
> **Project-owned files — edit:** none.

## 6. Close-out and acts owed

Per the brief: the spec's `## Deliverable` (each Done-when item's change,
the red-first lines, the tests run with their summary lines, the acts owed),
the spec moved to `docs/archive/work/complete/` with `spec_move.py` and its
`specref` cleared, `check_docs.py --root .`, the log fragment
`docs/log.d/WI-1072-identity-line-forging.md`, `trunk_step.py --regen`
before the commit that changes the registries.

Acts owed to a sitting: **LLR-359** (Accepted) amended in `Detail` and
`Rationale`; **TC-398** (Accepted) amended in `Method` and `Expected`. No
routed traced change (TC-398's `Evidence` is a silent trace cell; no
`verifies` moves). No new or rewritten `Drafted` row. No decisions record
(`docs/decisions/maint-wi-1072.toml`): the mechanism is LLR-359's text once
amended.

## 7. Decisions for the coordinator

- **D1. The mechanism is a refusal at compose**, over the whole composed
  text with the reader's own pattern, against the lines the composer wrote
  (§1), not a reader scoped to the identity section and not a rendering of
  judged cells. The reader, the binding's format and every consumer stay as
  they are.
- **D2. The check applies to every routed brief**, not only the three the
  spec names: one rule at the one composer, no kind condition, and the
  combined sitting can then rely on every section having passed it. LLR-359
  states it for any kind, and one stubbed test drives each other kind. The
  cost: a dispute's findings or a disposition's report quoting such a line
  at column 0 holds that sitting until reworded (none does today). The
  alternative is the three kinds alone, with a kind condition and a
  combined-level check over its amendment sections' slots only.
- **D3. Bindings written before this change read as before**; no migration,
  and no stored binding here can hold a forged identity (§Measured).
- **D4. LLR-359 and TC-398 are amended in full as written in §3**; LLR-167
  and TC-161 stay as they are (LLR-167 defers the identity line to LLR-359,
  and its generic "refused with a reason" already covers a refusal).
- **D5. No id is minted**: no new LLR or TC, and no `verifies` link added to
  TC-398 (it verifies LLR-359, which states the rule).
- **D6. Text appended to a composed brief after composition** (the recipe's
  owner-route section, the arms map) is named outside LLR-359's contract
  rather than guarded at the reader. The alternative guard, the reader
  refusing a prompt that names one id twice, would catch a replacement
  through appended text but not an addition.
- **D7. IF-115's contract body gains one sentence** and the interface
  reference is regenerated; no template, catalogue or dispatcher note
  changes, so no retained adjudicator drains.
- **D8. The tests**: a new in-process module for the three kinds, the
  sitting's own template and every other routed brief, plus one git case in
  `test_done_when_blessing.py` for a Done-when section's context; the clean
  control is not red-first. A smoke `max-tests` breach is stopped and
  reported, never re-stamped by me.
- **D9. The combined sitting reports its sections' composed text** under a
  values key that is never a slot, taken out before the fill as the hat
  parents are, so its own check covers only its template and perspectives
  tail.
- **D10. Merge note, WI-1045**: it moves functions out of
  `acceptance_record.py` and states no design row's text changes; this
  branch edits LLR-359's text block in the design registry and touches no
  function it moves. A textual conflict in that registry is possible if
  WI-1045 edits LLR-359's block (for example its component), and is resolved
  by keeping both edits.
