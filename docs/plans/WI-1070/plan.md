# WI-1070 plan, revision 1: the amendment brief shows a linked row's own text and the rows its moved links name

Written in the worktree `D:/ai-template-wt-wi1070`, branch `maint/wi-1070`,
cut from `refactor_again` at `ec188f984`. `planmode = "single"`: this commit
carries the plan alone, and nothing else changes until the coordinator's
go-ahead.

**Approved** by the coordinator 2026-11-24 (revision 1, `19572aff6`), D1 to
D12 confirmed: D9 with no optional IF-131 requestor, and a stop-and-report if
the strict trace reports an uncovered cross-component edge; D12 filed by the
coordinator as its own work item; TC-398's wording routed to WI-1071.

Read in full: the spec `docs/work/queued/WI-1070-brief-shows-link-targets.md`;
its scope critique `docs/reviews/2026-11-24-scope-critiques/WI-1070.md`; the
specref, the eighth sitting's verdict
`docs/reviews/wi-1068-adjudicate-eighth-sitting/001-ADJUDICATE-fbd50be.md`
(its first `## amendment` disposition and the 21 link rows', LLR-167's and
TC-161's MEANING lines); WI-1069's spec (`## Deliverable`, `## Trust`) and
plan. Code read: `amendment_brief.py` (whole); `adjudicate_brief.py`
(`compose`, `combined_values`, `_render_acceptance_rows`, `_spine_excerpt`,
`requested_identities`, the IF-115 contract); `trace.py` (`reaccept_model`);
`acceptance_record.py` (`SPINE_TRACED_CELLS`, `spine_cell_class`,
`accepted_text_digest`); `record_rows.py` (`ROUTED_TRACED_CELLS`,
`routed_cells`); `spine_carrier.py` (the tier tables, `load`, `load_needs`);
`arch_interfaces.py` (`contract_homes`, `_declaration_sites`);
`gen_arch_map.py` (`file_contracts`, `scan_contracts`); `arch_seams.py` (the
cross-component cover); `prompts.py` (`fill`, `strict_check`);
`kitlib/spine.py` (`refs`); `prompts/adjudicate-amendment.template.md` and
`adjudicate-combined.template.md`. Registries read: the interfaces registry
header (what an interface's contract is), the external registry's boundary
and entity tiers, the needs registry. Rows read: SR-144, SR-146, SR-148,
SR-178; LLR-167, LLR-359, LLR-484; TC-161, TC-331, TC-398, TC-461; IF-075,
IF-115, IF-131. Tests read: `test_amendment_brief_links.py`,
`routed_link_fixtures.py`, the amendment cases of `test_adjudicate_brief.py`,
`test_done_when_blessing.py`'s assembler stub, `test_prompts.py`'s slot rule,
and the size, import and complexity ratchets.

## Ids

None minted (D8). LLR-485 to LLR-489 and TC-572 to TC-580 stay unminted. No
SR, IF, DA, SUR or WI id.

## Measured (this branch's base, `ec188f984`)

Read-only, the worktree's Python 3.11, over the live registries.

- **The tiers a routed link names.** Every id in a routed traced cell
  (`record_rows.ROUTED_TRACED_CELLS`), by the tier its prefix names:
  a requirement's `SN-Refs` name needs (219 ids) and its `Boundary-Refs`
  boundary crossings (178); a requirement's `Constrains` names none today; a
  design row's `SR-Refs` name requirements (418) and its `Constrains`
  interfaces (28); a test case's `Verifies` names requirements (512), design
  rows (507) and interfaces (195). Five tiers: need, boundary crossing,
  requirement, design row, interface. No routed cell names any other tier.
- **The 21 link rows.** Their `Constrains` cells name 26 interface ids, each
  once, all live, all `Drafted`: IF-011, 012, 014, 017, 018, 019, 029, 030,
  032, 035, 036, 039, 041, 048, 074, 088, 139, 140, 149, 157, 158, 164, 227,
  254, 292, 293. Each has exactly one file stating its contract (the kit's
  harvest: 238 of the 239 live interface rows do), and each has a `Data`
  cell.
- **Sizes of the candidate cells** (characters; min / median / p90 / max):

  | Tier | Cell | min | median | p90 | max | whole at 2,400 |
  |---|---|---|---|---|---|---|
  | need (31) | `Need` | 101 | 207 | 283 | 656 | 100% |
  | crossing (7) | `Carries` | 99 | 162 | 196 | 305 | 100% |
  | requirement (141) | `Title` | 17 | 57 | 89 | 136 | 100% |
  | requirement | `Requirement` | 74 | 268 | 508 | 1,836 | 100% |
  | design row (369) | `Title` | 15 | 53 | 93 | 212 | 100% |
  | design row | `Detail` | 38 | 786 | 2,123 | 11,429 | 92% |
  | interface (239) | `Data` | 16 | 113 | 186 | 800 | 100% |
  | interface (238 stated) | stated contract | 144 | 611 | 1,541 | 6,261 | 95% |
  | the 26 targets | stated contract | 144 | 646 | 852 | 2,300 | 100% |

  Needs, crossings and interfaces carry no `Title` cell.
- **The contract harvest costs 2.2 s** on this tree (`contract_homes`, one
  scan of the declared surface); reading the 26 bodies after it, 0.02 s.
- **The brief at the base.** The dry compose (the brief's command, output in
  the scratchpad) composes all 54 of WI-1068's tokens without refusing:
  **188,802 characters**. It shows 24 amendment rows (the 21 link rows,
  LLR-167, TC-161, TC-398) with 24 identity lines, names the 15 rows the
  sitting blessed on its not-shown line, and drops the 11 first acceptances
  it accepted (their chains hold no `Drafted` row of the scope). Over the 28
  tokens still owed (those 24 amendments and TC-530, TC-571, LLR-423,
  TC-533): **188,615 characters**, the amendment section 82,288 of them. In
  that brief LLR-017's block is its link alone, and no interface's text
  appears anywhere.
- **Estimate of the growth** (computed over the model, not composed): the 21
  link rows' unmoved accepted cells add about 2,600 characters (titles, and
  the three link-only rows' details), the 26 listed interfaces about 20,400,
  the template about 1,200; LLR-167's and TC-161's own amendments add their
  own growth. About 213,000 characters over the 28 tokens. The Deliverable
  replaces this with the composed figure.

## 1. The linked row's own text (Done-when 1)

- **Which rows.** A row shown with at least one moved adjudicated link (the
  model row's `routed` cells that moved, as WI-1069 selects them). That is
  every tier with a routed cell: requirements, design rows and test cases.
  A row whose moved cells are all accepted cells is shown as today: its
  question is whether those cells' new text changed the obligation, which
  its unmoved cells do not bear on, and showing them for every amended row
  would add every amended row's whole text to every sitting.
- **What is shown.** After the row's moved accepted cells and moved links,
  one labelled sub-list of its other nonempty accepted cells, as they now
  read, sorted by cell name as the first-acceptance brief sorts a whole row.
  A moved cell is not repeated there: its current text is its `after` line
  above. The id cell and `Status` are left out, as the identity leaves them
  out, and so are the trace cells and the unmoved links (the block's head
  already names the row's chains). The cells are classed by the same
  classifier the identity uses (`acceptance_record.spine_cell_class`), so
  the moved accepted cells, the moved links and this list are the identity's
  text less its unmoved links; a test pins that the shown cells and links
  digest to the row's identity line (D10).
- **Layout.** For a link-only row and a row with both:

  ```
  - LLR LLR-017 (chain of SR-017)
    - Constrains (link)
      - before: (empty)
      - after: IF-032
    - Unmoved accepted cells (with the cells above, the row's whole accepted text):
      - Detail: Always-on scan of staged diff/message/outgoing range ...
      - Title: Secrets pattern scan

  - LLR LLR-010 (chain of SR-010)
    - Detail
      - before: ...
      - after: ...
    - Constrains (link)
      - before: (empty)
      - after: IF-014
    - Unmoved accepted cells (with the cells above, the row's whole accepted text):
      - Title: ...
  ```

  The moved cells stay first, so the judge sees what moved before reading
  the row whole; the label says the list did not move. A row with a moved
  link and every accepted cell moved shows the label with `(none)`. The
  unmoved cells are judged text, inside the row's identity, and are shown
  verbatim as the moved cells are, never clipped (a clipped judged text is
  the half-filled brief). The sub-list is indented, so no count of shown
  rows (lines opening `- <tier> `) reads it, and the verdict's row grammar
  is unchanged.

## 2. The named rows' identifying text (Done-when 2)

- **Which ids.** Every id a moved link names, before or after (split by the
  kit's one ref splitter, `kitlib.spine.refs`): the question is what the
  link now points at, and a removed target is part of what moved. Unmoved
  links name nothing to list.
- **Where.** A new section after the shown rows and before the identity
  lines, filled by a new template slot `{linked}` (D2) under its own
  heading: `ROWS THE MOVED LINKS NAME (context for the LINKS question: not
  under judgement, and in no JUDGED-TEXT identity)`.
- **Once per brief, pointed at by id.** Each id is listed once in the
  amendment brief (in a combined sitting, once in its amendment section,
  the one section that shows links), in tier order (need, crossing,
  requirement, design row, interface) then by id, each naming the shown rows
  and cells whose links name it and on which side: `- IF-032 (interface),
  named by LLR-017 Constrains (after)`. A link's `before`/`after` line keeps
  its bare ids; the listing is keyed by them. In the case each of the 26 is
  named once; under test cases' `Verifies` one requirement is commonly named
  by many rows, which is what the once-per-brief rule saves.
- **The cells shown, per tier** (the Done-when's "title and the cell that
  states what it is", from the registries' own schemas):

  | Tier | Registry (read) | Cells shown |
  |---|---|---|
  | need | the needs registry, through its own loader | `Need` |
  | boundary crossing | the external registry (off-spine) | `Direction`, `Entity` (its id, with the entity's `Name` when that row is live), `Carries` |
  | requirement | the requirement registry | `Title`, `Requirement` |
  | design row | the design registry | `Title`, `Detail` |
  | interface | the interfaces registry (off-spine) and the stated contracts | `Channel`, `Owner`, and the stated contract; the `Data` cell where no single file states one |

  The interface's contract is what its registry header defines it as: the
  `Contract IF-###:` body stated beside the code, read through the kit's own
  harvest (`arch_interfaces.contract_homes`, the one file stating each id,
  then `gen_arch_map.file_contracts` on that file); "until code states it,
  the row's data cell is the contract's home", so the `Data` cell stands in
  when no single file states one (none stated, stated twice, a refused or
  unreadable header, files mode or no scan root). Every one of the 21 rows'
  26 targets has a stated contract. The harvest runs only when a moved link
  names an interface (2.2 s here).
- **Off-spine rows are context, never judged.** The interfaces and external
  registries are read for this; their rows are listed as context, get no
  identity line, are named on no not-shown line and carry no verdict line;
  the spine rows listed (needs, requirements, design rows) are context in
  the same way unless they are themselves shown for judgement, when they are
  listed as `shown above for judgement` and not repeated.
- **An id naming no live row** of those five tiers (removed, mistyped, an
  example `-000` id, a tier no routed cell names) is listed as `names no
  live row`. An absent registry makes every id of its tier such an id. A
  registry that exists and does not parse fails the compose as the brief's
  other registry reads do (the commit floor refuses such a file, so it is
  outside the coverage bound).
- **The size bound.** Each listed cell is shown on one line, its whitespace
  collapsed, and clipped at **2,400 characters**: cut at the last space at
  or before the cap, followed by `… [clipped: 2,400 of N characters]`. Why
  2,400: it shows every need, crossing, requirement, title and data cell
  whole, 95% of stated contracts and 92% of design-row details, and every
  one of the case's 26 targets whole (the largest, IF-074, is 2,300); what
  it cuts is the tail of an outlier (contracts to 6,261, details to 11,429)
  while keeping its opening, where a row states what it is. Per brief the
  listing is then bounded by the number of distinct ids named times 2,400
  plus the label lines (D4). One line per cell also means no line of a
  listed text can read as an identity line or a verdict line (the binding
  reads `^JUDGED-TEXT:` over the whole prompt); a test drives a listed cell
  holding one.
- **A brief whose shown rows move no link** fills the section with one line,
  `(no moved link in this brief names a row)`, so the strict fill always has
  a value and the judge is told why it is empty.

## 3. The identity (Done-when 3)

- **Unchanged in what it covers.** `acceptance_record.accepted_text_digest`
  is not touched: one identity line per row shown for judgement, digesting
  its nonempty accepted cells and its nonempty adjudicated links. Every cell
  §1 adds is an accepted cell of that row, so the identity already covered
  it; §2's listed rows are not in it. No module that reads an identity
  changes (`kitlib.sitting.recorded_identities`, the held act, the held-claim
  exception, the held-MEANING mint).
- **Why the listed rows stay outside it** (WI-1069's `## Trust` terms). The
  binding decides whether an act may take a row on a held rung, and the act
  records that row: its text and its link ids, never the named row's text.
  A named row's text is judged at its own tier (a spine row by its own
  sitting, an interface by its own registry's hand-flipped status), and
  binding it would let an edit to one interface's contract refuse every
  held act on every row naming it. The residual is stated, not hidden: a
  verdict ruled a link against the named row's text as the brief listed it,
  and a later edit to that named row is that row's own amendment.
- **How the brief says so.** The section heading (§2); the identity heading
  becomes `JUDGED TEXT (the identity of each row shown for judgement: its
  accepted cells and adjudicated links; the rows listed as context above
  are not in it)`; the LINKS paragraph tells the judge to write no verdict
  line for a listed row; the dispatcher notes for `{linked}` and
  `{identity}` say the same.
- **A binding written before this change** reads exactly as before: the same
  row text gives the same digest, the identity lines a brief states are the
  same set, and no consumer reads the brief's context. Nothing is versioned
  or migrated. A verdict given over the old brief was given without the
  context; that is a sitting's question (the 21 rows are re-sat), not the
  identity's.
- **Coverage bound (Done-when 6).** The promises reach registries, recorded
  copies and bindings as supported workflows and the kit's own routes write
  them, and contract statements as the contract grammar admits them;
  hand-edited kit-written state (a recorded copy, an act ledger, a binding)
  is outside them (PROCESS.md §6, "Review threat model"). LLR-167 states it
  in a closing sentence, as LLR-359 does.

## 4. The rows (Done-when 4)

Each row written whole under the three row rules: no code names (inherited
ones scrubbed; LLR-167 and TC-161 carry none after WI-1069, checked again),
every clause driven by a test its case names (§5), nothing beyond or against
its parent. Amendments change text only.

Searched, the design and test-case registries for any row saying what the
amendment brief shows (`amendment brief`, `moved cell`, `moved link`,
`adjudicated link`, `per row`): LLR-167 and TC-161 state the contract;
LLR-359 says the brief renders an identity line "for each row it shows"
(D7); TC-398 (held by WI-1071) expects "one judged-text line per shown row"
(routed, below). Checked and left unchanged: SR-178, SR-207, LLR-245,
LLR-484, TC-571 (the acceptance model, surfaces and act, not this brief's
content); LLR-273 (the anchor stamps); TC-331 (admission); TC-461 (digest
width). SR-146, LLR-167's first parent, requires strictly filled, shipped,
reviewable prompt files: the new slot is strictly filled and declared, so
nothing here exceeds it; SR-144 and SR-148 are untouched by these clauses.

### LLR-167 (Accepted; Detail and Rationale amended; title unchanged)

**Detail**, whole (the amended sentences are the ninth to the eleventh from
"For each scoped row", the identity clause and the closing sentence):

> The session route reads an adjudication row's `Brief` and `Adjudicates` cells through the same reading the merge slot uses, so a spelling or scope one accepts cannot move the other's bound. The row's declared `Brief` cell selects the brief's template: the trunk mint writes it at every adjudication it mints with a brief to declare, its report-less cancellation and clean-close spot-check rows declare none, and a row declaring an unknown brief, the retired conflict brief included, refuses. The brief is filled under the prompt loader's strict check, which refuses an unknown slot and an unfilled declared one, and both of the loop's routing arms reach it by one path, so a claimed adjudication row gets the same brief whether or not a routing registry is configured. Every shipped brief, the Done-when and combined briefs included, is composed whole by its own evidence derivation or refused with a reason, never in part. A refusal is a hold, never a fallback: the loop prints the reason on its stop banner and exits asking for an operator, running no session, so a judge is never briefed as a builder; only a row declaring no brief builds from the worker assignment. A session handed a judging brief completes only when it commits, under the row's result trailer, the typed verdict line the brief demands at the path the brief names; no verdict, a missing machine line, a label outside the brief's closed set or a missing counter leaves it incomplete. The disposition brief follows the row's `SpecRef` to the closed spec, its immutable per-close report and that report's typed commit range, and lists the range's commits and changed paths clipped at a declared 80 lines; it refuses a clean close, which writes no report, and a report with no typed commit range. The evidence-gap brief re-runs the evidence-gap census rather than remembering it, joins each finding to its test case's method, expected and evidence cells and to the requirement or design text its targets name, and refuses a census that has come clean, a test case missing a listed cell and a target with no normative text. The consolidation brief is composed from the row's `Adjudicates` cluster re-derived live, every row of it or none; it refuses a row with no `Digests` cell, a cluster row no longer queued and a cluster whose overlap has dissolved. The amendment brief is bounded by the row's `Adjudicates` scope, which the amendment mint writes from the rows it routes, as the first-acceptance mint does; a row declaring no scope refuses rather than reading the empty cell as the whole tree. For each scoped row that claims acceptance and differs from its recorded copy in an accepted cell or an adjudicated link (LLR-484), it shows each moved accepted cell and each moved adjudicated link by its cell name with its before and after, a link marked as one, so a row whose only moved cells are adjudicated links is shown; a row under several requirements is shown once, naming each chain. A row with a moved link is also shown with each of its other nonempty accepted cells as it now reads, after its moved cells and labelled unmoved, so the judge reads the link against the row's whole accepted text; a row whose moved cells are all accepted cells is shown with those cells alone. After the shown rows, in a section labelled as context that is not under judgement and is in no judged-text identity, the brief lists once each id a moved link names, before or after, naming the shown rows whose links name it: a need by its statement; a boundary crossing by its direction, its entity and what it carries; a requirement by its title and requirement; a design row by its title and detail; an interface by its channel, its owner and its stated contract, or by its data cell where no single file states a contract. Each listed cell is shown on one line and clipped at 2,400 characters, the clip and the cell's full length stated; an id naming no live row of those tiers is listed as naming none; a named row that is itself shown for judgement is listed as shown above; and a brief whose shown rows move no link says so there. It asks of each link whether the row's text states what the link now points at, and asks for no verdict line on a listed row. A moved trace cell no adjudicator judges is not shown. A scoped row the recorded copy holds accepted and the live registry no longer carries is briefed as a removal, in one block naming it removed, with its accepted cells as the before and the removal as the after, its tier counted for the questions, baseline and aftermath as a shown row's tier. Need, assumption and surrogate rows in scope are shown with their moved accepted cells by the one owing rule. A scope token naming a row neither the live registries nor the recorded copy holds refuses, naming the token; a scope none of whose rows has anything to judge refuses, naming the scope; and each other scoped row with nothing to judge is named as not shown. Its baseline line names, for each registry shown, the commit that last wrote that registry's recorded copy, not the newest write anywhere in the record; it states one judged-text identity line per row shown for judgement (LLR-359) and none for a listed row; and its aftermath takes each verdict's held-rung arm from the one home of what a verdict owes on a held rung. The questions slot of the first-acceptance and amendment briefs is read at render time from the shipped questions home, one section per heading, each declaring on its next line the tiers it serves, `*` serving every tier. It composes, in home order and without that declaration line, the sections serving every tier and those serving a judged tier: a first acceptance's tiers are those of the registries its rows to accept sit in, an amendment's those of the rows shown, and a combined sitting composes each section as its own brief, so each carries its own questions. An absent or unreadable home, a section with no tiers declaration, a home with no section, or a home serving none of the judged tiers refuses the brief, naming the home; there is no fallback, and no prompt template or copy of the spine-authoring skill restates a question of it. Judging briefs order no act: a first-acceptance brief derives no registry argument for the act nor the rows each would cover, and the amendment aftermath names, for a later act turn, the mark each verdict owes: a CLARITY row is re-anchored later, naming its verdict on a held rung; a MEANING row whose new text the adjudicator would bless on a released rung is marked MEANING+BLESS; a held MEANING row is recommended to the operator. These promises reach registries, recorded copies and bindings as the kit's own routes write them, and contract statements as the contract grammar admits them; a hand-edited recorded copy, act ledger or binding is outside them.

**Rationale**, whole (one sentence added before the last):

> Two rules decide the shape. A judge's brief must not carry the claim under judgement as its premise - a leaked self-assessment anchors the judgement to it - so every value is registry-, git- or report-derived, and the one claim shown, the lane's report, is the template's own labelled subject. And a half-filled brief is worse than the generic prompt: hollow sections read as an investigation that was run and found nothing, which is the expensive way to be wrong, so there is no placeholder path at all. The discriminator is a declared cell rather than the reference cell's shape, because that inference is unsound - an amendment to a test-case row and an evidence-gap finding both cite the test-case registry while their briefs give contradictory instructions - and rather than a title substring, the fold LLR-161 retired. The amendment brief shows a moved adjudicated link beside the accepted cells because an act naming the row records it whole from live (LLR-245): a link the brief did not show would enter the record under a verdict that never saw it, and a scoped row left out unnamed lets a verdict and its scope disagree about what was judged. It shows that row's whole accepted text and the rows its links name because the question it asks of a link cannot be answered from a link's ids or a link-only row's empty diff; the named rows are context outside the identity because their text is judged at their own tier, and binding it would let an edit to one named row refuse every held act on a row naming it; and the clip bounds what one named row adds to a brief while keeping the opening where a row states what it is.

Parent check: SR-146 (strictly filled, shipped prompt files; the new slot is
declared and strictly filled), SR-144 and SR-148 (untouched clauses). Every
clause kept; the added clauses are tested under TC-161 (§5).

### TC-161 (Accepted; Method and Expected amended; verifies unchanged)

**Method**, whole (the sentence from "Over a row whose accepted cell alone
moved" is extended, two sentences follow it, and the combined clause is
widened):

> Drive the real loop against a fake agent command over throwaway git repositories for the disposition, evidence-gap and amendment briefs, and capture what the session was handed: the brief its row declares, not the worker assignment. Assert the session writes the typed verdict line its brief demands to the path the brief named and commits it under the row's result trailer, ending the run done; that a session committing the trailer with no verdict, or with a label outside the brief's closed set, does not complete; that a row whose declared brief cannot be filled is held for an operator, no session run, the reason printed and nothing committed under the row; and that a row declaring no brief builds from the worker assignment. Compose each routed brief in process and assert each slot carries its real derivation: for the disposition brief, the lane's report verbatim, the closed spec and the commit facts; for the evidence-gap brief, the live census joined to each test case's method, expected and evidence cells and to the obligation its targets name; for the consolidation brief, the whole cluster, the other open rows, the cited requirement and design text (a stated literal when the cluster cites none), the overlap findings, the recorded and current digest pairs and what earlier consolidations absorbed; for the first-acceptance brief, the whole chain of each requirement holding a scoped row, the scoped Drafted rows marked as the question, a held or out-of-scope row labelled not this session's and contributing no registry, an unrelated chain left out, no snapshot command, no 'BY YOU', no Status flip, and the later act turn named; TC-368 verifies act-side command quoting and registry scope, and TC-321 act-side completion. Assert no unfilled slot survives in the composed disposition, evidence-gap, amendment and first-acceptance text. Drive the refusals, each returning its reason and never part of a brief: a clean close with no per-close report, a report with no typed commit range, a census that has come clean, a test case missing a listed cell, a target with no normative text; a first-acceptance, amendment or consolidation row declaring no `Adjudicates` scope, a first acceptance whose scoped rows are all settled, gone from the spine or held for the operator, and an amendment none of whose scoped rows has a moved accepted cell or adjudicated link; a consolidation with no `Digests` cell, a cluster row no longer queued and a cluster whose overlap has dissolved. Pin the discriminator: two rows with one `SpecRef` and different declared `Brief` cells compose differently. Pin the routing both ways: the routed briefs are the shipped ones and each names a shipped template, every brief a mint declares is shipped and every routed brief is declared by a mint, a row declaring the retired conflict brief refuses as unknown, and an absent or unknown brief refuses. Pin each brief's typed verdict grammar: a well-formed line is accepted, and an absent file, a missing machine line, an out-of-set label or a missing counter is refused with its reason. Pin the amendment brief: the amendment mint writes the rows it routes as the row's scope, a one-row mint's brief renders that row alone while another row's unjudged drift stays out, and a row under two requirements is rendered once; the brief carries the recorded copy as its anchor, naming for each registry shown the commit that last wrote its copy, and with no recorded copy it holds and says first acceptance. Over a row whose accepted cell alone moved, a row whose adjudicated link alone moved and a row with both, the brief shows each moved cell and link by its cell name with before and after, the link marked and the link-only row shown, and asks of a link whether the row's text states what it now points at; the link-only row and the row with both are each shown with their other nonempty accepted cells after their moved cells, labelled unmoved and no moved cell repeated, the row whose accepted cell alone moved is shown with that cell alone, and each shown row's cells and links digest to its judged-text line. Move one link on each routed cell, to rows of each tier a link names, an interface whose contract one file states and one whose contract none states, and an id no row carries: the brief lists once, after the rows and labelled as context outside every identity, each id a moved link names before or after, naming the rows and cells that name it: a need by its statement, a boundary crossing by its direction, its entity and what it carries, a requirement and a design row by their title and their requirement or detail, the first interface by its channel, owner and stated contract and the second by its data cell; the absent id is listed as naming no live row, a named row also shown for judgement is listed as shown above, a cell over 2,400 characters is clipped stating the clip and its full length, a cell spanning lines is shown on one, and a brief moving no link says so. No listed row gets a judged-text line, a listed cell holding an identity-shaped line included, and the template asks for no verdict line on a listed row. A moved trace cell no adjudicator judges does not reach it; a scoped row with nothing to judge is named as not shown; a link-only row's verdict line reads as any row's. It renders a need, assumption or surrogate row in its scope with its moved accepted cells, and leaves out a moved row of those tiers the scope does not name. A scoped row removed from the live registry while its recorded copy holds it accepted is briefed as a removal, in a chained and an unchained tier, for the single-kind and combined briefs, a present scoped row with nothing to judge being named beside it; a scope token naming a row in neither home refuses, naming it; and a combined sitting's amendment section shows a link-only row with its unmoved accepted cells and lists once the rows its links name. Compose the first-acceptance, released and held amendment, and combined briefs and find no snapshot command, no 'BY YOU' and no Status flip, the later act turn named. Compose a first-acceptance brief over a design row and amendment briefs over a requirement and a need: each carries the every-row questions and its own tier's section and no other, and a combined first-acceptance section carries its rows' questions. Point the renderer at a substitute questions home: its text is carried, a change to it changes the brief, and an absent home, a directory, an undecodable file, a section with no tiers line, or a home serving none of the judged tiers refuses naming the home. Assert no question opening appears in any prompt template or any copy of the spine-authoring skill.

**Expected**, whole:

> Each brief is handed to the session its row declares, with its derived evidence and every slot filled; each refusal returns its reason, composes no part of a brief and holds the row for an operator with no session run; the discriminator, the routing and each verdict grammar hold both ways; the amendment brief shows every moved accepted cell and adjudicated link of its scoped rows, marks the links, shows a row with a moved link with its whole accepted text, lists once as context outside every identity each row a moved link names by its identifying cells, clipped where long, and an id naming no row as naming none, and names each scoped row it does not show; the questions come from their one home; and no judging brief orders an act.

Parent check: every added clause matches an LLR-167 clause (whole text,
listing, per-tier cells, contract or data, clip, missing id, shown above,
empty listing, no identity, no verdict line on a listed row, combined
section); nothing beyond it. Its `Evidence` cell is regenerated (a silent
trace cell).

### LLR-359 (Accepted; Detail amended, one sentence; D7)

The sentence "An amendment brief renders one judged-text identity line for
each row it shows." becomes "An amendment brief renders one judged-text
identity line for each row it shows for judgement." Nothing else changes.
Under the old brief every shown row was shown for judgement, so a correct
implementation of the old text passes the new one; the negative half (none
for a listed row) is LLR-167's clause and TC-161's test, so LLR-359 states
no clause TC-398 does not already drive.

### Routed to the coordinator (WI-1071 holds it)

- **TC-398** `expected`: "Each brief states one judged-text line per shown
  row" reads, once a brief lists named rows, as if a listed row were owed a
  line. Proposed: "per row shown for judgement". Its method composes a brief
  over a link-only row, whose link (in its fixture) names no live row and is
  therefore listed as naming none; its test still passes, since it reads the
  identity lines alone.

### Off-spine, not judged

None changed (D9). The new reads go through call surfaces whose owner
component is already covered for the brief's component (IF-075 names the
brief's component among its requestors, and the cross-component cover is
per component pair).

## 5. The tests (red first)

The fixture `tests/routed_link_fixtures.py` gains, written before the seed
so the record holds them: a needs registry (SN-001, SN-002), an external
registry (EXT-001 and the crossing B-01), an interfaces registry (IF-001
with a data cell only; IF-002 with a data cell and a contract stated by a
module under the fixture's default scan root, `src/`), and a helper that
moves one link to a given value. "Red" is failing on this base before the
code changes; each red line is quoted in the Deliverable. All in process.

| Module | Test, one line | Done-when | Red? |
|---|---|---|---|
| `tests/test_amendment_brief_links.py` (TC-161) | The link-only row is shown with its title and detail under the unmoved label after its link, and no trace cell, `Status` or id | 1 | red |
| same | The row with both shows its detail before and after, its link, then its title under the unmoved label, the detail not repeated | 1 | red |
| same | The row whose accepted cell alone moved is shown as before, with no unmoved label | 1 | guard |
| same | Each shown row's moved cells, links and unmoved cells digest to its judged-text line | 1, 3 | red |
| same | A link moved on each routed cell lists each id it names, before and after (an id the move removed included), by its tier's cells (need, crossing with entity name, requirement, design row, interface by data) | 2 | red |
| same | An interface whose contract one file states is listed by its channel, owner and contract; with no scan root it is listed by its data cell | 2 | red |
| same | A link naming an id no row carries is listed as naming no live row | 2 | red |
| same | An id named by two shown rows is listed once, naming both, each with its cell and side | 2 | red |
| same | A listed cell over 2,400 characters is clipped at the last space, stating the clip and its full length; a cell spanning lines is shown on one | 2 | red |
| same | A named row also shown for judgement is listed as shown above, its text not repeated | 2 | red |
| same | A brief whose shown rows move no link fills the listing with its one line | 2 | red |
| same | No listed row gets an identity line: the binding's reading of the composed brief names the scoped rows alone, a listed cell holding an identity-shaped line included | 3 | red |
| same | The template labels the listing as context in no identity, the identity heading says so, and the LINKS paragraph asks for no verdict line on a listed row | 3 | red |
| same | A combined sitting's amendment section shows the link-only row's unmoved cells and lists the rows its links name, once | 1, 2, 5 | red |
| same (changed) | WI-1069's exact LLR-002 block assertion gains the unmoved list | 1 | changed |
| `tests/test_done_when_blessing.py` (changed) | The stubbed amendment assembler returns the new slot | 5 | changed |
| `tests/test_prompts.py` | Every slot is declared in its template's dispatcher notes (`{linked}` with its clip) | 2 | guard |

Done-when 4 is §4; 6 is a statement in LLR-167 with no test of its own (as
WI-1069's bound); 7 is §6. Run besides, per the brief: every test module
importing a changed module (`amendment_brief`, `adjudicate_brief`, by grep
and `trace.py --tests-for`: about 23 modules), the modules holding TC-161's
and TC-398's tests, `tests/test_prompts.py`, the four ratchets,
`trace.py --root . --strict`, `check_trajectory.py --root . --strict`, then
`run_menu.py smoke` once. About 16 new in-process cases: the smoke tier's
membership stays under `max-tests = 4060` (3,905 at WI-1069's close), so no
re-stamp is expected.

## 6. The measure (Done-when 7)

The brief's dry compose, from the worktree root, writing nothing under
`docs/` (checked with `git status` after each run), output in the session
scratchpad:

```
.venv/Scripts/python.exe scripts/coordinator/compose_lane.py WI-1068 combined "<tokens>" "<WI-1068's 32 sr_refs>" docs/reviews/wi-1068-dry/001-ADJUDICATE-dry.md <scratchpad>/<name>.md
```

Run at the base (done: 188,615 characters over the 28 owed tokens,
188,802 over all 54) and again at the tip, over the same two token sets.
The compose drops the tokens the eighth sitting settled (the blessed
amendments are named not shown; the accepted first acceptances add
nothing), so the **28 owed tokens are the measure of record**, the 54
reported beside it. The Deliverable gives, per set, the total characters
before and after, the amendment section's characters, the listing's
characters, the number of rows listed and of cells clipped, and the identity
line count (24 before and after: the listing adds none). At the tip the
brief also shows LLR-167's and TC-161's new text and, in the 54-token set,
LLR-359 (amended again, D7); the Deliverable separates that growth from the
listing's. A `fig:` line carries each figure's command and revision.

## 7. Code, file by file

- `amendment_brief.py`: the model row's unmoved accepted cells for a row with
  a moved link (a helper beside `_judged_cells`, the selection split kept
  under the complexity limit); `_cell_block` renders them under the label;
  `_amended_rows` also returns each shown row's moved links; a per-tier
  table of the linked rows' registries and cells (`LINKED_TIERS`) and the
  clip (`LINKED_CLIP = 2400`); the `{linked}` renderer (collect ids by
  `kitlib.spine.refs`, load each named tier once, the interface contract
  read through `arch_interfaces.contract_homes` and
  `gen_arch_map.file_contracts`, both imported in the function, only when an
  interface is named); `amendment_values` returns `linked`; the module and
  `amendment_values` docstrings. About +110 SLOC (258 now; the module is far
  under the 1,000 watch threshold).
- `adjudicate_brief.py`: the IF-115 contract body's sentence on identity
  lines says "each row it shows for judgement; the rows its moved links name
  are listed as context, with none"; `docs/interface-reference.md`
  regenerated.
- `prompts/adjudicate-amendment.template.md`: the `{linked}` slot and heading,
  the identity heading, one sentence in the LINKS paragraph (the unmoved
  cells, the listing, no verdict line on a listed row), the dispatcher notes
  for `{rows}`, `{linked}` (its clip declared) and `{identity}`;
  `prompts/CATALOG.md` regenerated in the same commit.
- Not changed: `acceptance_record.py` (989 of 1,000 SLOC, 28 importing test
  modules; D10), `arch_interfaces.py` and `gen_arch_map.py` (read through
  their existing public functions; D9), every identity consumer.
- Registries: §4's three rows; `trunk_step.py --root . --regen` before the
  registry commit, `tomllib` parse checks, TC-161's evidence regenerated.

## 8. The RESYNC entry

Anchored `[since ec188f984]`, after the last entry:

> ### The amendment brief shows a linked row's whole accepted text and lists the rows its moved links name [since ec188f984]
>
> *(Anchored at the preceding commit: the change lands in the commits after it.)*
>
> **What changed.** For a scoped row with a moved adjudicated link, the
> amendment brief now also shows the row's other nonempty accepted cells, as
> they now read, under an "unmoved" label after its moved cells. After the
> shown rows, a new section lists once each id a moved link names, before or
> after: a need by its statement; a boundary crossing by its direction,
> entity and what it carries; a requirement or design row by its title and
> requirement or detail; an interface by its channel, owner and the
> `Contract IF-###:` body one file states, or its `data` cell when none
> does; each cell on one line, clipped at 2,400 characters with the clip
> stated; an id naming no live row is listed as such. The section is
> labelled context: not under judgement and in no `JUDGED-TEXT` identity.
> The identity and every reader of a binding are unchanged.
>
> **What to do.** If you override `adjudicate-amendment.template.md`, add the
> new `{linked}` slot under its heading, and carry the identity heading and
> the LINKS sentence into your copy: the strict fill refuses an override
> without the slot, naming it, and the loop holds the amendment row until
> it is added. Bindings written before the upgrade read as before. The
> template edit moves the retained-session identity, which hashes the
> template file's bytes, so a retained adjudicator whose classes include
> the amendment brief drains once. Composing a brief whose links name
> interfaces now runs the contract harvest once (seconds on a large tree).
>
> **Kit-owned files — overwrite:** `scripts/amendment_brief.py`,
> `scripts/adjudicate_brief.py`, `prompts/adjudicate-amendment.template.md`,
> `prompts/CATALOG.md`.

`scripts/check_resync.py` checks it in the smoke tier.

## 9. Close-out and acts owed

As the brief orders: the Deliverable before Context (each Done-when's change,
the red-first lines, the tests run with real summary lines, the measure, the
acts owed), `spec_move.py` to `docs/archive/work/complete/`, `specref`
cleared, `check_docs.py --root .`, the log fragment
`docs/log.d/WI-1070-brief-shows-link-targets.md`. Acts owed, as planned:

- **Amendments to `Accepted` rows:** LLR-167 (Detail, Rationale); TC-161
  (Method, Expected); LLR-359 (Detail).
- **Routed traced changes to `Accepted` rows:** none (no `SN-Refs`,
  `Boundary-Refs`, `SR-Refs`, `Constrains` or `Verifies` cell moves).
- **New `Drafted` rows owed a first acceptance:** none.

The 21 link rows, LLR-167 and TC-161 stay owed; the re-sitting is filed when
this and WI-1071 land (spec, "Not in scope").

## 10. Decisions for the coordinator

- **D1. The row's own text sits inside its block, after its moved cells,
  labelled "Unmoved accepted cells", the moved cells not repeated; only for
  a row with a moved link.** Alternatives: the whole row again below the
  diff (repeats every moved cell's `after`), or a whole-row listing for
  every amended row (adds every amended row's full text to every sitting
  for a question only a link asks).
- **D2. A new required template slot `{linked}`, under its own heading
  between the rows and the identity lines,** rather than appending the
  listing inside `{rows}`. It keeps the context visibly apart from the text
  under judgement and lets the template label it. Cost: an adopter who
  overrides the amendment template must add the slot; the strict fill
  refuses until they do (fail-loud, never a quiet half-filled brief), and
  the RESYNC entry says so. Inside `{rows}` would force no migration but
  puts context under the "AMENDED CELLS" heading.
- **D3. The cells per tier (§2's table), and an interface's contract read
  from the kit's contract harvest, its `Data` cell the fallback.** The
  interfaces registry calls the stated body the definition and `data` "the
  row's typed summary, not the definition"; the sitting asked for the
  definition. The off-spine interfaces and external registries are read;
  their rows are context, never judged. A crossing shows its entity's name
  beside the id, which is the one extra lookup beyond the Done-when's list.
- **D4. The bound: 2,400 characters per listed cell**, whitespace collapsed,
  cut at a space, the clip and full length stated. Shows the whole case and
  ≥92% of every tier whole. Alternatives: 1,200 (clips 2 of the case's 26,
  and 28% of design details) or no clip (one 11,429-character detail per
  named design row).
- **D5. Every id a moved link names, before and after, listed once per brief
  in tier then id order, naming the rows, cells and sides that name it**; a
  named row also shown for judgement listed as shown above. Alternative:
  only the ids a move added or removed (smaller, but the judge then cannot
  read what the link now points at as a whole).
- **D6. The identity is unchanged; the listed rows stay outside it** (§3's
  argument). A binding written before reads as before; nothing migrates.
- **D7. LLR-359's sentence gains "for judgement"** (one more amendment owed,
  expected to read as clarity), so a sitting cannot read LLR-167's
  context listing against "for each row it shows". Alternative: leave
  LLR-359 and rely on LLR-167's wording. TC-398's "per shown row" routed to
  WI-1071 (§4).
- **D8. No id minted: LLR-167 and TC-161 carry the whole contract**, as the
  Done-when names them. Alternative: a new design row (LLR-485) and case
  (TC-572) for the listing, leaving LLR-167 one sentence pointing at it:
  smaller rows to judge, but two more first acceptances and LLR-167 still
  amended.
- **D9. No module of the architecture component and no interface row
  changes.** The brief calls the existing `contract_homes` and
  `file_contracts`, imported in the one function that needs them; the
  cross-component check covers the edge through the pair IF-075 already
  declares. Optional instead: add the brief's component to IF-131's
  requestors (a `Drafted`, off-spine row), which states the contract-header
  readers.
- **D10. `acceptance_record.py` is not touched.** The unmoved list is
  selected with the identity's own classifier, and a test pins that the
  shown text digests to the identity line. Extracting one shared
  "judged cells" function there would be the stronger structure, but the
  module sits at 989 of the 1,000-SLOC watch line and 28 test modules
  import it.
- **D11. The measure of record is the 28 owed tokens,** the 54 reported
  beside it, since the compose drops the settled tokens without refusing.
- **D12. A separate finding, not fixed here:** a judged cell is rendered
  verbatim, so a registry cell whose text holds a line opening
  `JUDGED-TEXT: <id> <digest>` would be read by the binding as an identity
  line. The listing in this plan cannot do that (one line per cell); the
  rows' own cells could already, before this change. Worth its own row if
  the coordinator agrees.
