# WI-1069 plan, revision 1: a sitting is shown each moved routed link

Written in the worktree `D:/ai-template-wt-wi1069`, branch `maint/wi-1069`,
cut from `refactor_again` at `d62f3c74b`. `planmode = "single"`: this commit
carries the plan alone, and nothing else changes until the coordinator's
go-ahead.

Read in full: the spec `docs/work/queued/WI-1069-brief-shows-routed-links.md`
(its `## Trust` and `## Scope answers` included); its scope critique
`docs/reviews/2026-11-23-scope-critiques/WI-1069.md`; WI-1024's plan §1 (the
class of `constrains`); WI-1068's spec (the sitting that waits on this row);
WI-1067's spec (the sibling, to stay off SR-207 and TC-560). Code read:
`trace.py` (`spine_chain`, `sr_chain_drifts`, `_owes_first`,
`reaccept_model`, `_cell_diff_lines`, `_entry_lines`, `dial_releases_chain`,
`reaccept_lines`, `acceptance_check`); `baseline_snapshot.py` (`is_drifted`,
`drifted_cells`, `owing_rows`, `tier_owing`, the IF-125 contract);
`record_rows.py` (`ROUTED_TRACED_CELLS`, `_settled`, `row_rule`);
`acceptance_record.py` (the cell tables, `split_changed_cells`,
`accepted_text_digest`, `_row_settled`, `settled_amendments`,
`unanchored_rows`, `text_as_bound`); `amendment_brief.py` (whole);
`adjudicate_brief.py` (`first_acceptance_values`, `_render_chain`,
`combined_values`, `bind_pending`, `requested_identities`);
`adjudicate_act.py` (`_state`, `_unbound_text`, `_derive`); `held_status.py`
(`_bound_clarity`, `_excepted`); `kitlib/sitting.py` (`read_identities`,
`recorded_identities`); `intake.py` (`_routed_amendments`,
`_held_act_drafts`); `gen_open_items.py` (`_changed_cell_groups`,
`_changed_cell_lines`, `_acceptance_cards`, the page header); `pending.py`
(the SR drift projection); `prompts/adjudicate-amendment.template.md`;
`kitlib/verdict.py` (`row_rulings`). Rows read: SR-139, SR-144, SR-146,
SR-148, SR-178, SR-207, SR-208, SR-232; LLR-118, LLR-153, LLR-158, LLR-167,
LLR-173, LLR-245, LLR-246, LLR-259, LLR-271, LLR-272, LLR-273, LLR-278,
LLR-359, LLR-364, LLR-420; TC-123, TC-147, TC-153, TC-161, TC-331, TC-398,
TC-448, TC-461, TC-530; IF-075, IF-124, IF-125, IF-129, IF-287, IF-296.
Tests read: the amendment-brief, identity, held-claim, act, drift and
open-items modules named in §5, and the size, complexity, import and smoke
ratchets.

## Ids

Two minted, from the brief's ranges: **LLR-484** (the selection and surface
obligation, §4) and **TC-571** (its case). LLR-485 to LLR-489 and TC-572 to
TC-580 stay unminted. No SR, IF, DA, SUR or WI id.

## Measured (trunk at `d62f3c74b`, this branch's base)

Measured read-only with the worktree's Python 3.11 over the live registries
and the recorded copy (`docs/archive/last_accepted/`).

- **Rows that claim acceptance and differ from their recorded copy: 27.**
  18 carry an accepted change and a routed change (all `Constrains`: LLR-010,
  012, 013, 025, 026, 033, 039, 047, 118, 124, 130, 171, 198, 199, 258, 279,
  281, 320); 3 carry a routed change alone (LLR-017, LLR-022, LLR-024, each
  `Constrains`); 6 carry an accepted change alone (SR-207, SR-211, SR-249,
  LLR-403, TC-195, TC-480); 0 carry a silent trace change alone. So the slice
  owes 21 routed `constrains` changes (18 + 3). WI-1068's Context says "20 of
  them also gaining" a link; the measured figure is 18.
- **The acceptance model selects 22 requirement chains.** SR-017, SR-022 and
  SR-024 are not among them: LLR-017, LLR-022 and LLR-024 appear in no
  entry's rows. With the change, 25.
- **The amendment brief over WI-1068's 26 `amendment:` tokens shows 23 rows
  and 0 `Constrains` cells, and drops LLR-017, LLR-022 and LLR-024 unnamed.**
  It states 23 identity lines. The acceptance brief (`docs/ratify/CURRENT.md`)
  already shows LLR-010's `Constrains` under "traced — routes to adjudication",
  because LLR-010's chain is selected by its moved `Detail`.
- **Bindings.** 212 `.requested` files under `docs/reviews/`; 35 carry an
  identity cell, 289 identity tokens (LLR 133, TC 112, SR 38, SN 6). 276 of
  them name a row whose live text carries a nonempty routed cell. The dial
  (`operator_accepts_through = "DevStg-Boundary"`) releases the SR, LLR and TC
  tiers and holds SN, DA and SUR; no routed cell exists on a held tier, so 0
  tokens on a held tier change value under §3.

## 1. Selection

### Where drift is computed today

`trace.reaccept_model` keeps a requirement when `owes(sr)` holds: the SR owes
a first acceptance (`_owes_first`), a row of its chain does, or
`sr_chain_drifts(sid, chain, snapshot)` is true. The chain is
`trace.spine_chain`: the SR, every design row below it in the requirement
tree, every test case verifying either. `sr_chain_drifts` asks
`baseline_snapshot.is_drifted(rel, id_col, row, snapshot_rows)` of each chain
row: true when the row claims acceptance, is present in the recorded copy,
and `split_changed_cells` (the id column and `Status` excluded, the rest
classed by `spine_cell_class` over `SPINE_TRACED_CELLS`, the residual
accepted) reports a nonempty **accepted** half. The traced half, routed or
silent, never selects. Once an SR is selected, each chain row is diffed
against the recorded chain and kept as `changed` with every moved cell,
accepted first then traced, so a routed change on a row under an
otherwise-selected SR is already shown; a row whose own SR nothing else
selects is not.

### What changes

- `record_rows.routed_cells(rel)`: the routed set for a registry, keyed by
  stem (the lookup `_settled` builds inline today; it reads it from here).
- `baseline_snapshot.routed_moved(rel, id_col, live_row, snapshot_rows)`:
  `{cell: (before, after)}` for the routed cells of a row that claims
  acceptance and is present in the copy, `{}` otherwise, with `is_drifted`'s
  guards and the same `split_changed_cells`.
- `sr_chain_drifts` selects a chain when any row `is_drifted` **or** has a
  nonempty `routed_moved`. `is_drifted`, `drifted_cells` and `owing_rows` are
  unchanged: "drift" stays the accepted half, the record's LLR-173 and
  TC-153 stay true, and a moved routed link is a second reason a row owes
  (decision D1).
- Each model row gains `routed`, the frozenset of its moved routed cells, and
  `cells` is ordered accepted, then routed, then the other trace cells.
- **A silent trace cell still selects nothing**: `routed_moved` reads only the
  routing table, so a row whose only moved cells are, say, `Hat-Refs`,
  `Phase` or `Evidence` makes neither arm true and its SR stays out of the
  model (a test pins it, and a test pins the table the arm reads).

### Every reader of the model, and what it shows for a link-only row

| Reader | What it shows for a link-only row after the change |
|---|---|
| The acceptance brief, `docs/ratify/CURRENT.md` (`trace.reaccept_lines`, `trace.py --accept modified`) | The row's SR chain gets a section; the row renders as changed, its link by cell name with before and after under the routed label (below). The dial puts the chain in the operator's section or the collapsed "Waiting for automated adjudication" block as today (`dial_releases_chain` counts a changed row as owing); here LLR is released, so SR-017, SR-022 and SR-024 land in the block. |
| The brief's freshness gate (`trace.acceptance_check`, step `acceptance-fresh`) | The window stays open while such a row owes; the brief reads stale until regenerated (trunk-owned). |
| The operator page, `open-items.html` (`gen_open_items`) | A card for the SR chain, "re-accept owed"; the row's link as a word diff under the routed label; the header counts the chain. |
| The amendment brief (`amendment_brief.amendment_values`, alone and as a combined sitting's amendment section) | The row is shown, its link marked (§2). |
| The first-acceptance brief (`adjudicate_brief.first_acceptance_values`) | Unchanged: it reads only `accept`-kind entries, and a link-only chain with nothing `Drafted` is `reaccept`. A chain that is `accept` for another row already renders the link-only row whole, labelled not this session's. |

Not readers of the model, read for completeness: `pending.py`'s status
projection asks `is_drifted` of SRs alone and says "accepted text differs",
so it does not list a link-only SR; left unchanged (D9). The snapshot command
(LEFT OWED), the act ledger (`kept`) and the trunk mint already treat a
link-only row as owed.

## 2. The brief

- **Selection inside the scope.** `_scoped_chain_rows` keeps, per scoped row,
  the accepted cells (`accepted`) and the routed cells (`routed`) of the model
  row, and keeps the row when either is nonempty. Other trace cells are not
  shown.
- **Rendering.** One block per row as today, accepted cells first, each link
  after them by its registry column name (`Constrains`, `SR-Refs`,
  `Verifies`, `SN-Refs`, `Boundary-Refs`, the names accepted cells already
  use; D7), marked as a link:

  ```
  - LLR LLR-010 (chain of SR-010)
    - Detail
      - before: ...
      - after: ...
    - Constrains (link)
      - before: (empty)
      - after: IF-014
  ```

  A link-only row is the same block with its links alone.
- **The question.** The template gains one paragraph (its body, not the
  questions home: it is this brief's method, D7): a cell marked `(link)` is an
  adjudicated link, carrying no prose, and the one question asked of it is
  the one its routing exists for, *does the row's text state what the link
  now points at?* If it does, the link moved no obligation (CLARITY for that
  cell); if it does not, the row now claims what its text does not say
  (MEANING), and such a row is not one to bless. The listing's label becomes
  "AMENDED CELLS AND MOVED LINKS", the identity label "the identity of each
  row's accepted text and links shown above", and the dispatcher notes for
  `{rows}` and `{identity}` say the same.
- **The verdict's row grammar is unchanged.** A link is ruled with a row line
  naming its cell (`- [CLARITY] LLR-017 Constrains -> ...`); `row_rulings`
  keys on the row id, `rows=N` counts rows shown, and no reader of a verdict
  changes. A test pins a link-only row's line parsing as today.
- **A scoped row is never dropped unnamed (Done-when 4).** The three scoped
  populations (chain rows, unchained need and assumption rows, removed rows)
  are collected as today; a scope token naming neither home still refuses
  naming the token; a scope none of whose rows has anything to judge,
  accepted or routed, still refuses naming the scope, its reason reworded
  ("still carries accepted text or an adjudicated link that differs from its
  copy", the silent-trace case named). New: when some rows are shown, every
  other scoped id is named in one line after the blocks, `Scoped, nothing to
  judge (not shown; rule no line for them): <ids>.`, which does not start
  with `- ` so no row count reads it (D6). The combined brief composes its
  amendment section through the same derivation, so it gains both halves:
  the link-only rows are shown and the rest named, and an empty section still
  refuses the whole sitting naming the section.

## 3. The identity (Done-when 3, `## Trust`)

- **One function.** `acceptance_record.accepted_text_digest(rel, id_col,
  row)` keeps its name and shape (`sha256:` and 16 hex over sorted JSON) and
  digests the row's nonempty **accepted cells and routed cells**
  (`record_rows.routed_cells(rel)`), the id and `Status` excluded. It is
  already the only identity function: the brief states it (`_identity`), and
  the three consumers compute it from the committed row: the held act
  (`adjudicate_act._unbound_text`), the held-claim exception
  (`held_status._excepted` through `_bound_clarity`) and the held-MEANING
  mint's at-the-bound-text test (`acceptance_record.text_as_bound`). No
  consumer changes its comparison; each now reads a moved link as moved text.
  The act's refusal wording names "its judged text (accepted cells and
  adjudicated links)" instead of "its accepted text".
- **All routed cells, not only the moved ones.** The digest covers every
  routed cell of the row, shown or unchanged. An unshown link is unshown
  because it equals the recorded copy, which the verdict judged the row
  against; a move to it after the verdict is a move away from what was
  judged. It is also the only identity a consumer can recompute without
  knowing which cells a brief showed. It is the record's own comparison:
  `record_rows._settled` and `acceptance_record._row_settled` already compare
  accepted plus routed cells.
- **The name stays** (D4). "Accepted-text digest" is the row vocabulary of
  SR-208's acceptance criteria and LLR-246; renaming it would amend both
  (LLR-246 is 3.4k characters of code names) and IF-129's data cell and
  stale WI-1045's prose. LLR-359 defines the term as the identity of the
  text a sitting judges: accepted cells and adjudicated links.
- **A binding written before this change.** It carries digests over accepted
  cells alone. Read after the change: for a row whose routed cells are all
  empty, the two digests are equal (empty cells are dropped), so it still
  binds, and that is safe because there is no link the verdict did not see.
  For a row carrying a nonempty routed cell, the digests differ, so it fails
  closed in each consumer: the held act refuses before launch naming the row
  and both digests; the held claim is not excepted, so the commit or merge
  refuses it; the held-MEANING row is not counted as at its bound text, so
  no operator row is minted and it stays on the amendment row and the
  acceptance brief as owed. The remedy is a re-sit. Nothing is versioned or
  migrated (D5): an accepted-only verdict never judged the link, so it must
  not authorize recording it. No false acceptance is possible: a nonempty
  routed cell changes the hashed text, so an old digest cannot equal a new
  one. In this repository the identity is read only for held rows and no
  held tier carries a routed cell, so 0 of 289 bound tokens read differently.
  Released rungs and taken acts read no identity, as today.
- **Coverage bound (Done-when 5).** The promises cover registries, recorded
  copies, act ledgers and bindings in the shapes the kit's own routes write
  (the authoring lanes, the snapshot command, the binding writer). A
  hand-edited recorded copy, act ledger or binding, and a list cell spelled
  in a form the carrier does not write, are outside them (PROCESS.md §6,
  "Review threat model"). LLR-359 and LLR-484 say so in a closing sentence,
  as LLR-364 does.

## 4. The rows

Each amended row is rewritten whole under the three row rules: no code name
(inherited ones scrubbed), one obligation with every clause driven by a test
its case names, nothing beyond its parent. Amendments change text only; the
two new rows are `Drafted`. A clause the build finds no test for gets a test
or is cut, and the Deliverable says which.

Checked and left unchanged, with why: LLR-118 and TC-123 (the page reads the
model; neither says a row with a moved link is absent, and TC-123's
"undrifted" row is an unchanged fixture row); LLR-158 (the basis is
unchanged); LLR-173 and TC-153 (drift stays the accepted half, D1); LLR-246
and SR-208 (the identity keeps its name, D4); LLR-259 ("changed" already
covers the row); LLR-271, LLR-272, LLR-273, LLR-364, LLR-420 (no claim about
what the model selects or the brief shows); TC-147 (gains one test tag, its
evidence cell regenerated; text unchanged, D12).

### SR-178 (Accepted; AcceptanceCriteria and Rationale amended; D2)

Its criteria say "a merely traced cell moving is not" reported, which LLR-484
would contradict. Requirement and title unchanged.

- **AcceptanceCriteria:** "An artifact whose normative text has moved since
  the copy that recorded its acceptance is reported whether or not its Status
  moved; an accepted cell or an adjudicated link moving under a row still
  claiming acceptance is reported, while a trace cell no adjudicator judges
  moving is not, and a row below acceptance has no claim to fall from and is
  not reported; the status marker itself is not read as the movement, so a
  flip is neither an amendment nor a mask for one; and stakeholder needs,
  assumptions and surrogates are held to the same rule."
- **Rationale:** the current text, then one paragraph: "AN ADJUDICATED LINK
  IS REPORTED, THOUGH IT IS TRACED. A requirement's needs, boundary crossings
  and constrained interfaces, a design row's requirements and constrained
  interfaces and a test case's verified rows carry no prose, so they are not
  accepted text; but whether a move changed what the row claims is a
  sitting's judgement, and an acceptance act leaves such a row at its
  recorded text until an act names it. A move no surface reported would wait
  for an act nobody was shown. A trace cell no adjudicator judges follows
  live whenever an act writes its file, and is not reported."
- Clauses and their cases: moved text reported whatever the Status, the
  accepted cell, the row below acceptance, the marker: TC-153. The
  adjudicated link and the unjudged trace cell: TC-571. Needs: TC-269.
  Assumptions and surrogates: TC-448.

### LLR-484 (new, `Drafted`, parent SR-178, phase 6, test_refs TC-571)

- **Title:** "A row whose adjudicated link moved is owed on the acceptance
  surfaces, naming the link"
- **Detail:** "An adjudicated link is a trace cell whose change goes to an
  adjudicator: a requirement's needs, boundary crossings and constrained
  interfaces, a design row's requirements and constrained interfaces, and a
  test case's verified rows. The acceptance model lists the chain of every
  row that claims acceptance and whose adjudicated link differs from its
  recorded copy, as it lists a row whose accepted text moved, even when none
  of its accepted cells moved. It gives each listed row its moved accepted
  cells, its moved adjudicated links and its other moved trace cells as three
  groups, each cell with its before and after. A row whose only moved cells
  are trace cells no adjudicator judges, such as its perspectives, phase or
  evidence, lists no chain. The acceptance brief and the operator's decision
  page show each listed row in its chain with each moved link by its cell
  name, before and after, under a label saying it goes to a sitting, apart
  from the accepted cells, labelled as owing a re-acceptance, and the other
  trace cells, labelled as owing no act. The contract covers registries and
  recorded copies the kit's own routes write; a hand-edited recorded copy is
  outside it."
- **Rationale:** "An acceptance act leaves a row whose adjudicated link moved
  at its recorded text until an act names it (LLR-245), so the snapshot
  command reports it left owed and the act ledger lists it kept; a model
  selecting on accepted text alone put it on no surface, and two answers to
  what is owed disagreed. The link carries no prose, so it arms no
  re-acceptance of its own; whether its move changed what the row claims is a
  sitting's judgement, so the row is listed for one rather than re-anchored
  without one."
- Parent check: within SR-178's amended criteria (the link reported, the
  unjudged trace cell not).

### LLR-167 (Accepted; Detail and Rationale rewritten; title unchanged; D3)

- **Detail:**

  "The session route reads an adjudication row's `Brief` and `Adjudicates`
  cells through the same reading the merge slot uses, so a spelling or scope
  one accepts cannot move the other's bound. The row's declared `Brief` cell
  selects the brief's template: the trunk mint writes it at every
  adjudication it mints with a brief to declare, and its report-less
  cancellation and clean-close spot-check rows declare none, and a row
  declaring an unknown brief, the retired conflict brief included, refuses.
  The brief is filled under the prompt loader's strict check, which refuses
  an unknown slot and an unfilled declared one, and both of the loop's
  routing arms reach it by one path, so a claimed adjudication row gets the
  same brief whether or not a routing registry is configured. Every shipped
  brief, the Done-when and combined briefs included, is composed whole by its
  own evidence derivation or refused with a reason, never in part. A refusal
  is a hold, never a fallback: the loop prints the reason on its stop banner
  and exits asking for an operator, running no session, so a judge is never
  briefed as a builder; only a row declaring no brief builds from the worker
  assignment. A session handed a judging brief completes only when it
  commits, under the row's result trailer, the typed verdict line the brief
  demands at the path the brief names; no verdict, a missing machine line, a
  label outside the brief's closed set or a missing counter leaves it
  incomplete.

  The disposition brief follows the row's `SpecRef` to the closed spec, its
  immutable per-close report and that report's typed commit range, and lists
  the range's commits and changed paths clipped at a declared 80 lines; it
  refuses a clean close, which writes no report, and a report with no typed
  commit range. The evidence-gap brief re-runs the evidence-gap census rather
  than remembering it, joins each finding to its test case's method, expected
  and evidence cells and to the requirement or design text its targets name,
  and refuses a census that has come clean, a test case missing a listed cell
  and a target with no normative text. The consolidation brief is composed
  from the row's `Adjudicates` cluster re-derived live, every row of it or
  none; it refuses a row with no `Digests` cell, a cluster row no longer
  queued and a cluster whose overlap has dissolved.

  The amendment brief is bounded by the row's `Adjudicates` scope, which the
  amendment mint writes from the rows it routes, as the first-acceptance mint
  does; a row declaring no scope refuses rather than reading the empty cell
  as the whole tree. For each scoped row that claims acceptance and differs
  from its recorded copy in an accepted cell or an adjudicated link
  (LLR-484), it shows each moved accepted cell and each moved adjudicated
  link by its cell name with its before and after, a link marked as one, so a
  row whose only moved cells are adjudicated links is shown; a row under
  several requirements is shown once, naming each chain. It asks of each link
  whether the row's text states what the link now points at. A moved trace
  cell no adjudicator judges is not shown. A scoped row the recorded copy
  holds accepted and the live registry no longer carries is briefed as a
  removal, in one block naming it removed, with its accepted cells as the
  before and the removal as the after, its tier counted for the questions,
  baseline and aftermath as a shown row's tier. Need, assumption and
  surrogate rows in scope are shown with their moved accepted cells by the one
  owing rule. A scope token naming a row neither the live registries nor the
  recorded copy holds refuses, naming the token; a scope none of whose rows
  has anything to judge refuses, naming the scope; and each other scoped row
  with nothing to judge is named as not shown. Its baseline line names, for
  each registry shown, the commit that last wrote that registry's recorded
  copy, not the newest write anywhere in the record; it states one
  judged-text identity line per row shown (LLR-359); and its aftermath takes
  each verdict's held-rung arm from the one home of what a verdict owes on a
  held rung.

  The questions slot of the first-acceptance and amendment briefs is read at
  render time from the shipped questions home, one section per heading, each
  declaring on its next line the tiers it serves, `*` serving every tier. It
  composes, in home order and without that declaration line, the sections
  serving every tier and those serving a judged tier: a first acceptance's
  tiers are those of the registries its rows to accept sit in, an
  amendment's those of the rows shown, and a combined sitting composes each
  section as its own brief, so each carries its own questions. An absent or
  unreadable home, a section with no tiers declaration, a home with no
  section, or a home serving none of the judged tiers refuses the brief,
  naming the home; there is no fallback, and no prompt template or copy of
  the spine-authoring skill restates a question of it. Judging briefs order
  no act: a first-acceptance brief derives no registry argument for the act
  nor the rows each would cover, and the amendment aftermath names, for a
  later act turn, the mark each verdict owes: a CLARITY row is re-anchored
  later, naming its verdict on a held rung; a MEANING row whose new text the
  adjudicator would bless on a released rung is marked MEANING+BLESS; a held
  MEANING row is recommended to the operator."

- **Rationale:** "Two rules decide the shape. A judge's brief must not carry
  the claim under judgement as its premise - a leaked self-assessment anchors
  the judgement to it - so every value is registry-, git- or report-derived,
  and the one claim shown, the lane's report, is the template's own labelled
  subject. And a half-filled brief is worse than the generic prompt: hollow
  sections read as an investigation that was run and found nothing, which is
  the expensive way to be wrong, so there is no placeholder path at all. The
  discriminator is a declared cell rather than the reference cell's shape,
  because that inference is unsound - an amendment to a test-case row and an
  evidence-gap finding both cite the test-case registry while their briefs
  give contradictory instructions - and rather than a title substring, the
  fold LLR-161 retired. The amendment brief shows a moved adjudicated link
  beside the accepted cells because an act naming the row records it whole
  from live (LLR-245): a link the brief did not show would enter the record
  under a verdict that never saw it, and a scoped row left out unnamed lets a
  verdict and its scope disagree about what was judged."
- Parent check: SR-146 (strictly filled briefs), SR-144 (the disposition
  brief's per-close report) and SR-148 (an unfillable adjudication row held
  for an operator); the link clauses are brief content under SR-146 as the
  accepted-cell clauses were. The verdict-line clause states what TC-161
  already drives, so the case no longer exceeds its row.

### LLR-359 (Accepted; Detail and Rationale rewritten; title unchanged)

- **Detail:** "A row's accepted-text digest is the identity of the text a
  sitting judges on it, formed from its nonempty accepted cells and its
  nonempty adjudicated links (LLR-484), excluding its id and Status: carrier
  representation and an absent versus empty cell give the same identity, a
  moved accepted cell or adjudicated link changes it, and a moved trace cell
  no adjudicator judges does not. An amendment brief renders one judged-text
  identity line for each row it shows. Reservation writes those identities
  in the binding, and rewriting the binding as recorded or failed preserves
  them. A held CLARITY re-acceptance is actable only when the accepted
  binding's identity equals the committed row's digest, and an absent,
  malformed or unequal identity yields a refusal before launch naming the
  row and both digests; a held acceptance claim is excepted only under a
  CLARITY verdict whose binding records the row's equal digest. The contract
  covers registries, recorded copies and bindings the kit's own routes
  write; a hand-edited recorded copy, act ledger or binding is outside it."
- **Rationale:** "A verdict about one text cannot authorize a later text
  unless the text the verdict saw has a stable identity carried from brief
  reservation through the later act. The adjudicated links are in the
  identity because an act naming the row records them with its accepted text
  (LLR-245), so a link moved after the verdict would otherwise be recorded
  under a verdict that never judged it. Comparing the committed identity with
  the accepted binding keeps a changed, absent or malformed identity from
  being read as the judged row."
- Parent check: SR-208's criteria require the claim's verdict to bind "its
  equal accepted-text digest", which this defines; SR-178 reports moved text.

### TC-161 (Accepted; Method and Expected rewritten; verifies unchanged)

- **Method:** "Drive the real loop against a fake agent command over
  throwaway git repositories for the disposition, evidence-gap and amendment
  briefs, and capture what the session was handed: the brief its row
  declares, not the worker assignment. Assert the session writes the typed
  verdict line its brief demands to the path the brief named and commits it
  under the row's result trailer, ending the run done; that a session
  committing the trailer with no verdict, or with a label outside the brief's
  closed set, does not complete; that a row whose declared brief cannot be
  filled is held for an operator, no session run, the reason printed and
  nothing committed under the row; and that a row declaring no brief builds
  from the worker assignment. Compose each routed brief in process and assert
  each slot carries its real derivation: for the disposition brief, the
  lane's report verbatim, the closed spec and the commit facts; for the
  evidence-gap brief, the live census joined to each test case's method,
  expected and evidence cells and to the obligation its targets name; for the
  consolidation brief, the whole cluster, the other open rows, the cited
  requirement and design text (a stated literal when the cluster cites none),
  the overlap findings, the recorded and current digest pairs and what
  earlier consolidations absorbed; for the first-acceptance brief, the whole
  chain of each requirement holding a scoped row, the scoped Drafted rows
  marked as the question, a held or out-of-scope row labelled not this
  session's and contributing no registry, an unrelated chain left out, no
  snapshot command, no 'BY YOU', no Status flip, and the later act turn named;
  TC-368 verifies act-side command quoting and registry scope, and TC-321
  act-side completion. Assert no unfilled slot survives in the composed
  disposition, evidence-gap, amendment and first-acceptance text. Drive the
  refusals, each returning its reason and never part of a brief: a clean
  close with no per-close report, a report with no typed commit range, a
  census that has come clean, a test case missing a listed cell, a target
  with no normative text; a first-acceptance, amendment or consolidation row
  declaring no `Adjudicates` scope, a first acceptance whose scoped rows are
  all settled, gone from the spine or held for the operator, and an amendment
  none of whose scoped rows has a moved accepted cell or adjudicated link; a
  consolidation with no `Digests` cell, a cluster row no longer queued and a
  cluster whose overlap has dissolved. Pin the discriminator: two rows with
  one `SpecRef` and different declared `Brief` cells compose differently. Pin
  the routing both ways: the routed briefs are the shipped ones and each
  names a shipped template, every brief a mint declares is shipped and every
  routed brief is declared by a mint, a row declaring the retired conflict
  brief refuses as unknown, and an absent or unknown brief refuses. Pin each
  brief's typed verdict grammar: a well-formed line is accepted, and an
  absent file, a missing machine line, an out-of-set label or a missing
  counter is refused with its reason. Pin the amendment brief: the amendment
  mint writes the rows it routes as the row's scope, a one-row mint's brief
  renders that row alone while another row's unjudged drift stays out, and a
  row under two requirements is rendered once; the brief carries the
  recorded copy as its anchor, naming for each registry shown the commit that
  last wrote its copy, and with no recorded copy it holds and says first
  acceptance. Over a row whose accepted cell alone moved, a row whose
  adjudicated link alone moved and a row with both, the brief shows each
  moved cell and link by its cell name with before and after, the link marked
  and the link-only row shown, and asks of a link whether the row's text
  states what it now points at; a moved trace cell no adjudicator judges does
  not reach it; a scoped row with nothing to judge is named as not shown; a
  link-only row's verdict line reads as any row's. It renders a need,
  assumption or surrogate row in its scope with its moved accepted cells, and
  leaves out a moved row of those tiers the scope does not name. A scoped row
  removed from the live registry while its recorded copy holds it accepted is
  briefed as a removal, in a chained and an unchained tier, for the
  single-kind and combined briefs, a present scoped row with nothing to judge
  being named beside it; a scope token naming a row in neither home refuses,
  naming it; and a combined sitting's amendment section shows a link-only
  row. Compose the first-acceptance, released and held amendment, and
  combined briefs and find no snapshot command, no 'BY YOU' and no Status
  flip, the later act turn named. Compose a first-acceptance brief over a
  design row and amendment briefs over a requirement and a need: each
  carries the every-row questions and its own tier's section and no other,
  and a combined first-acceptance section carries its rows' questions. Point
  the renderer at a substitute questions home: its text is carried, a change
  to it changes the brief, and an absent home, a directory, an undecodable
  file, a section with no tiers line, or a home serving none of the judged
  tiers refuses naming the home. Assert no question opening appears in any
  prompt template or any copy of the spine-authoring skill."
- **Expected:** "Each brief is handed to the session its row declares, with
  its derived evidence and every slot filled; each refusal returns its
  reason, composes no part of a brief and holds the row for an operator with
  no session run; the discriminator, the routing and each verdict grammar
  hold both ways; the amendment brief shows every moved accepted cell and
  adjudicated link of its scoped rows, marks the links and names each scoped
  row it does not show; the questions come from their one home; and no
  judging brief orders an act."
- The IF-124 and IF-075 seams stay verified (the anchor and the model).

### TC-398 (Accepted; Method and Expected rewritten; verifies unchanged)

- **Method:** "Digest a requirement row, then the same row with its id, its
  Status and a trace cell no adjudicator judges changed, with an empty cell
  against an absent one, and on its other carrier; then with an accepted
  cell moved, and with an adjudicated link moved; and with the owner's
  digest width changed. Compose an amendment brief over committed rows, one
  with a moved accepted cell and one with a moved adjudicated link alone, and
  read its judged-text lines. Reserve a sitting from a composed prompt,
  round-trip and read its binding, and rewrite it as recorded and as failed.
  Derive the held act of a CLARITY verdict whose binding equals the committed
  row, one whose row's accepted cell moved after it, one whose row's
  adjudicated link moved after it, one whose binding was written over the
  row's accepted cells alone, one with no identity and one with a malformed
  identity cell, and launch the act turn over one whose text moved. Judge a
  held acceptance claim under a CLARITY verdict binding its equal digest, and
  one whose adjudicated link moved after the verdict."
- **Expected:** "The digest has the sha256 shape at the owner's width and is
  unchanged by the id, the Status, the unjudged trace cell, empty against
  absent and the carrier, and changes for the accepted cell and the
  adjudicated link. The brief states one judged-text line per shown row,
  carrying that row's committed digest. The binding records the prompt's
  identities, reading its requested kinds ignores them, and both rewrites
  keep them. The held act is owed only under the equal binding; the moved
  cell, the moved link, the accepted-cells-only binding of a row carrying a
  link, the missing and the malformed identity each refuse it naming the
  row, and the act turn refuses before launch. The claim is excepted under
  the equal binding and not when the link moved."

### TC-571 (new, `Drafted`, verifies SR-178 and LLR-484, phase 6)

- **Level** Unit, **Tier** Smoke, **Automated** Yes.
- **Method:** "Over a project whose accepted requirements each carry one
  accepted design row and one test case, record an acceptance copy. For each
  adjudicated link of each tier, move that link alone on one accepted row and
  read the acceptance model; check the links moved are the routing table's.
  Then move only the first design row's detail, add an interface to the
  second design row's constrains cell, move the third's detail and add an
  interface to its constrains cell, and move only the fourth's phase and
  perspective cells; read the model, and render the acceptance brief and the
  operator's decision page."
- **Expected:** "Each single moved link lists its row's chain, the row
  carrying that link as moved with no moved accepted cell. The model lists
  the first three chains and not the fourth; the second row carries its
  constrains cell, before and after, as a moved link alone, the third its
  detail as an accepted cell and its constrains cell as a link, and the first
  its detail alone. The brief and the page show the second and third rows'
  constrains cell by name with its before and after under the sitting label,
  the third's detail under the re-acceptance label, and a row's other moved
  trace cells under the label owing no act."

### Off-spine (`Drafted`; first acceptance already owed)

- **IF-129** notes: "The digest uses the cell classification
  split_changed_cells uses and adds the routed traced cells
  (record_rows.ROUTED_TRACED_CELLS), so a carrier representation, an absent
  versus empty cell and a silent traced cell do not change it, and a moved
  accepted cell or routed link does." Data unchanged.
- **IF-075** data: "reaccept_model entries (chain rows; changed cells with
  each row's accepted and routed subsets; baseline; copy stamps);
  assumption_owing_model rows (id, why, moved cells, chain); an empty model is
  valid".

## 5. The tests (red first)

A new fixture helper, `tests/routed_link_fixtures.py` (not collected),
writes a TOML project with SR-001 to SR-004, each with one design row and one
test case, two interfaces, every row `Accepted`, seeds the record, then
applies: LLR-001 `detail` moved (accepted only), LLR-002 `constrains` added
(link only), LLR-003 both, LLR-004 `phase` and `hat_refs` moved (silent
only). Git-backed consumers reuse their modules' existing git fixtures with
a link moved. "Red" means failing on this base before the code changes; each
red line is quoted in the Deliverable.

| Module (case) | Test, one line | Done-when | Red first? |
|---|---|---|---|
| `tests/test_routed_link_owed.py` (TC-571), new | A link moved alone, per (tier, cell) of the routing table, puts its chain in the model, the row's links set to it and no accepted cell | 1 | red |
| same | The parametrized pairs are the routing table | 1 | guard |
| same | A row moving only unjudged trace cells (phase, perspectives) selects no chain | 1 | guard |
| same | The row with both carries its accepted cells and links apart, accepted first | 1 | red |
| same | The acceptance brief lists the link-only row in its chain, the link by name with before and after under the sitting label | 1 | red |
| same | The operator page lists the link-only row's link as a diff under the sitting label | 1 | red |
| same | Both surfaces label the three groups alike for one row | 1 | red |
| `tests/test_adjudicate_brief.py` (TC-161) | Over the fixture's three rows, the brief shows the accepted-only row's cell, the link-only row's link marked, and both on the third | 2 | red |
| same | A scope of the link-only row alone composes (it refuses today) | 2, 4 | red |
| same | A silent trace cell never reaches the judge (the existing `Phase` test, its comment re-pointed, plus `Hat-Refs`), and the refusal names the scope | 2, 4 | guard |
| same | A scoped row with nothing to judge beside shown rows is named in the not-shown line, never as a block | 4 | red |
| same | The removal test's present scoped row is now named as not shown | 4 | red |
| same | A combined sitting's amendment section shows a link-only row | 2, 4 | red |
| same | The composed brief asks the link question and labels the listing | 2 | red |
| same | A link-only row's verdict line parses to its ruling as any row's | 2 | guard |
| same (TC-398) | The brief's judged-text line for the link-only row carries its committed digest | 3 | red |
| `tests/test_held_status.py` (TC-398) | The digest ignores id, Status and unjudged trace cells (`SN-Refs` leaves that list) and changes for an adjudicated link | 3 | red |
| `tests/test_adjudicate_act.py` (TC-398) | A held CLARITY act whose link moved after the verdict refuses, naming the row and both digests | 3 | red |
| same | A binding written over accepted cells alone refuses a held row carrying a link (fails closed) | 3 | red |
| `tests/test_held_status_git.py` (TC-398) | A held claim whose link moved after its CLARITY verdict is not excepted | 3 | red |
| `tests/test_intake_held_act.py` (TC-147) | A held MEANING row whose link moved after its verdict is not carried to the operator | 3 | red |

Done-when 5 is a statement in two rows, with no test of its own. Done-when 6
is the table, §4 and §6. Run besides: every importer of the changed modules
(`trace.py --tests-for` plus a grep), the modules holding TC-147, TC-161,
TC-398 and TC-571's tests, the four ratchets, `trace.py --root . --strict`,
`check_trajectory.py --root . --strict`, then `run_menu.py smoke` once.

## 6. Code, file by file

- `record_rows.py`: `routed_cells(rel)`; `_settled` reads it.
- `baseline_snapshot.py`: `routed_moved`.
- `trace.py`: import `record_rows` (both import branches; acyclic, it
  imports only the carrier and `kitlib`); `sr_chain_drifts`' second arm; the
  model row's `routed` and cell order; one grouping function
  `changed_cell_groups` (accepted "re-acceptance owed", routed "adjudicated
  link, goes to a sitting", other "trace cell, owes no act"), headed when more
  than one group shows or the row has no accepted group (D8), read by
  `_cell_diff_lines`; the brief's opening sentence names a moved adjudicated
  link; docstrings. A reviewed SLOC bump of its size baseline (3847), about
  +10, with the reason (D11). `reaccept_model` stays at its complexity 13:
  the `routed` set comes from a helper, not a new branch.
- `gen_open_items.py`: `_changed_cell_groups` reads trace's grouping, so the
  page and the brief cannot label a cell differently (the copy they kept in
  step by hand today goes).
- `amendment_brief.py`: `_scoped_chain_rows` keeps links, `_cell_block`
  marks them, a helper writes the not-shown line, the refusal wording, the
  module and `amendment_values` docstrings.
- `acceptance_record.py`: the digest reads `record_rows.routed_cells`; the
  IF-129 contract text and the comment block on the identity.
- `adjudicate_act.py`: the refusal wording and module docstring.
- `held_status.py`: its docstring's one line on the digest.
- `prompts/adjudicate-amendment.template.md`: §2's paragraph and labels;
  `prompts/CATALOG.md` regenerated in the same commit (as WI-1060 did for the
  act template).
- `docs/registry-machinery-reference.md` §12.10: one sentence that a moved
  `SR-Refs` also lists its row on the acceptance surfaces until an act names
  it.
- Registries: §4's rows, `trace.py --bump-ids`, `trunk_step.py --regen`
  before each registry commit, `tomllib` parse checks.
- If the smoke tier's count passes `[smoke-budget] max-tests`, a reasoned
  re-stamp.

## 7. The RESYNC entry

Anchored `[since d62f3c74b]`, after the WI-1027 entry:

> ### A moved routed link puts its row on the acceptance surfaces and in the amendment brief, and a verdict's identity covers it [since d62f3c74b]
>
> **What changed.** The acceptance model (`trace.reaccept_model`) now lists
> the chain of a row that claims acceptance and whose routed traced cell
> (`SN-Refs`, `Boundary-Refs`, `Constrains` on a requirement; `SR-Refs`,
> `Constrains` on a design row; `Verifies` on a test case) differs from its
> recorded copy, even when no accepted cell moved; a row whose only moved
> cells are other trace cells is still not listed. Each model row carries a
> new `routed` set. `docs/ratify/CURRENT.md` and `open-items.html` show
> changed cells in three labelled groups: accepted (re-acceptance owed),
> routed link (goes to a sitting) and other trace cells (no act). The
> amendment brief shows each moved routed link beside the accepted cells,
> marked `(link)`, shows a row whose only change is a link, names any scoped
> row it does not show, and its template asks of a link whether the row's
> text states what it now points at. `accepted_text_digest` now digests a
> row's routed cells with its accepted cells, so a verdict's binding covers
> the links, and a link moved after a verdict refuses a held act as moved
> text does.
>
> **What to do.** Regenerate the acceptance brief and the operator page:
> they may now list chains they did not. Before upgrading, take any held
> CLARITY act still owed under a verdict you have already bound: after the
> upgrade, a binding written before it refuses a held row that carries any
> routed link, naming both digests, and that row's verdict is re-sat. A
> binding on a row with no routed link reads as before. If you override
> `adjudicate-amendment.template.md`, carry the link paragraph into your
> copy. A script that reads `reaccept_model` can read `routed`; the other
> keys are unchanged.
>
> **Kit-owned files — overwrite:** `scripts/trace.py`,
> `scripts/baseline_snapshot.py`, `scripts/record_rows.py`,
> `scripts/acceptance_record.py`, `scripts/amendment_brief.py`,
> `scripts/gen_open_items.py`, `scripts/adjudicate_act.py`,
> `scripts/held_status.py`, `prompts/adjudicate-amendment.template.md`,
> `prompts/CATALOG.md`.

If the template edit moves a retained adjudicator's governing identity (the
build checks), the entry adds that it drains once, as WI-1060's said.

## 8. Close-out and acts owed

The close follows the brief: Deliverable before Context, `spec_move.py` to
`docs/archive/work/complete/`, `specref` cleared, `check_docs.py`, the log
fragment. Acts owed to automated adjudication, as planned:

- **Amendments to `Accepted` rows:** SR-178 (AcceptanceCriteria, Rationale);
  LLR-167 (Detail, Rationale); LLR-359 (Detail, Rationale); TC-161 (Method,
  Expected); TC-398 (Method, Expected).
- **Routed traced changes to `Accepted` rows:** none planned (no `SR-Refs`,
  `Verifies` or `Constrains` cell of an accepted row moves).
- **New `Drafted` rows owed a first acceptance:** LLR-484, TC-571.
- Off-spine `Drafted` rows amended, first acceptance already owed: IF-075,
  IF-129.

WI-1068 waits on this row; once it lands, its scope shows 26 rows, 21 of
them with a `Constrains` link, and these seven rows are owed beside it.

## 9. Decisions for the coordinator

- **D1. Drift stays the accepted half.** A moved routed link is a second
  reason a row owes, read by a new function beside `is_drifted`, not a
  widening of it. Widening would amend LLR-173 (blessed at the seventh
  sitting) and TC-153, and make `pending.py`'s "accepted text differs" line
  false.
- **D2. Amend SR-178's criteria and rationale.** Its "a merely traced cell
  moving is not" reported would be contradicted by LLR-484. The alternative,
  reading "merely traced" as "not adjudicated" with no SR edit, risks the
  sitting finding LLR-484 exceeding its parent. Amending puts all of SR-178
  before the sitting.
- **D3. One new row and case for selection (LLR-484, TC-571); the brief's
  links stay in LLR-167**, rewritten whole, rather than carved into a row of
  their own. Carving would also rewrite TC-161 and LLR-167 (both are
  rewritten anyway for their inherited code names) and add a second new row
  and case.
- **D4. The identity keeps its name** in code and rows ("accepted-text
  digest"), redefined in LLR-359 as accepted cells plus adjudicated links.
  Renaming it would amend SR-208's criteria and LLR-246 and stale WI-1045's
  prose.
- **D5. A pre-change binding is not versioned or migrated.** It still binds
  a row with no routed link and fails closed, to a re-sit, for a row with
  one. Measured: 0 affected tokens on a held tier here.
- **D6. A scoped row with nothing to judge, beside rows shown, is named in a
  not-shown line, not refused.** A whole scope with nothing still refuses by
  name. The stricter reading, refusing whenever any scoped row has nothing,
  would hold a sitting each time another act settles one of its rows first
  (the interrupts WI-572 removed).
- **D7. A link is shown by its registry column name, as accepted cells are
  (`Constrains`), marked `(link)`.** The link question lives in the
  amendment template's body, not the questions home, because it is the
  meaning-or-clarity method for a link, not a tier's blessing question.
- **D8. Three labelled groups on both operator surfaces, from one grouping
  function in `trace.py`** that the page reads, so the "traced — routes to
  adjudication" label stops covering cells that route nowhere. A lone
  non-accepted group is labelled; a lone accepted group stays unlabelled as
  today.
- **D9. `pending.py`'s status projection is left as it is** (SR drift on
  accepted text); a link-only SR shows on the two surfaces built on the model.
- **D10. LLR-118 and TC-123 are left as they are** (§4, checked).
- **D11. A reviewed SLOC bump of `trace.py`'s size baseline** of about +10.
- **D12. TC-147 gains one test tag** (the held-MEANING mint's consumer of the
  identity) with its evidence cell regenerated and its text unchanged; the
  alternative is stating that consumer in LLR-359, whose parents (SR-178,
  SR-208) do not hold the operator-row mint.
