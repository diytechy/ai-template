+++
id = "WI-1009"
title = "docs/open-items.html stops listing delegated decisions one by one; the operator reads them in their record files"
workstream = "process"
sr_refs = ["SR-225", "SR-049"]
specref = ""
buildtier = "medium"
safety_class = "spine"
priority = 3
planmode = "single"
+++

## Deliverable

`docs/open-items.html` lists no delegated decision. The operator reads them
in their record files, `docs/decisions/<run>.toml`, where an entry with no
`operator` key is not yet seen (the operator's ruling (c), 2026-11-19). The
page went from 2,001,004 bytes to 77,757. Built on the maintenance branch
`maint/wi-1009`, cut from `refactor_again` at `6a78f63a7`, outside the lane
workflow. The spec of record was the 2026-11-18 progress log in
`docs/plans/2026-11-11-test-tiers/HANDOFF.md` §12.6; the row's SpecRef cell
was cleared at close, as R-F asks of a terminal row.

- **The critique's dispositions** (`26c3bf808`): S1 settled by the
  operator's ruling (c), quoted in the Context; S3, S4, S5, B1 and B4
  adopted in that light. `planmode = "single"`.
- **The plan** (`08bcbe22b`): `docs/plans/WI-1009/plan.md`.
- **Tests first** (`9e127326c`): `tests/test_decisions_to_review.py`
  rewritten and `tests/test_open_item_queue.py`'s section-order test re-aimed.
  23 cases failed before the code, each for the missing read
  (`pending.decision_records`), the fourth section, the old status line or
  the old template header. The tests that existed only to render the section
  are cut: the overruled heading, its citing work items, the confirmed-count
  notice and the page's ordering (ruling B5).
- **The code** (`550369d99`):
  - `gen_open_items.py` loses section 4 with `_DECISION_FIELDS`,
    `_decision_card`, `_citing_field`, `OVERRULED_HEADING` and
    `decisions_block`. `record_findings_block` keeps the one part that was a
    check: each record's format findings, by file and entry, in a notice
    closing section 3, shown only when a record carries one. Nothing else
    reports them across all records whatever the dial: the merge slot reads
    only a closing lane's own record, and only under a recording dial. No
    CSS rule was the section's alone.
  - `pending.py`: `decisions_to_review` and `citing_rows` give way to
    `decision_records(root)`, which returns `(unseen count, findings)`.
  - `traj_status.py`: the status line reads `Delegated decisions not yet
    seen: N — docs/decisions/`, linking the directory, not the removed
    anchor. Kept rather than dropped, because across 132 files nothing else
    says how many entries are still unseen; that is the backlog DA-020's
    obstacle names, and TC-293 checks the count.
  - `kitlib/decisions.py`: its docstring only.
  - The shipped template's header and `PROCESS_OPTIONS.md` (-35 bytes) send
    the operator to the record files. The RESYNC entry forces nothing and
    migrates nothing.
- **The rows** (`23c951229`): SR-225 amended (its requirement, its
  acceptance criteria and one rationale sentence). LLR-118, LLR-283, TC-123
  and TC-293 amended to match, with LLR-283's `code_symbol` following the
  code. All five keep `Accepted` and now drift on the page for the operator's
  re-accept: 7 SR chains owe one, up from 5 (SR-225's and SR-049's are the
  new ones). IF-074 and IF-164 (Drafted) have new data cells. No id minted.
- **The close** (this commit): the page regenerated after the rows' commit,
  whose off-spine census now names WI-1009 among the rulings that touched
  `interfaces.toml`.

**DA-020 is unchanged.** "The operator reads each entry listed as not yet
seen" still holds under (c): the record lists every entry, and one with no
verdict reads as not yet seen there.

**Left undone, and why.**

- **`kitlib.decisions.review_queue` still orders its lists and returns the
  overruled list and the confirmed count**, which nothing renders now. Only
  its unseen list is read. Cutting the rest changes IF-256's stated call
  contract, and WI-1004 is working in that file in parallel, so it was left.
- **The October backlog** (1,141 entries not yet seen) is the operator's to
  mark or read, as the Context says; not this row.
- **No review rounds.** On this maintenance branch the parent session reviews
  the diff.

## Context

Filed by hand on 2026-11-18 at the operator's direction: the "Decisions to
review" section is too much for `docs/open-items.html`. On 2026-11-18 it held
1,144 cards, 110 of them high-risk, almost all from coordinator sessions of
October. They crowd out the page's purpose: the pending decisions and the
acceptance act.

The entries already have a home. Each delegated run writes its own record,
`docs/decisions/<run>.toml` (132 files on 2026-11-18). The page only renders
them, through `pending.decisions_to_review`. Taking them off the page loses no
data.

SR-225 still requires a listing of each entry the operator has not yet seen,
and of each overruled entry beside the open work that carries it. So the
listing moves; it is not dropped. The scope critique picks where:

- (a) **Recommended:** its own generated page, `docs/decisions.html`, from the
  renderer that draws the section today. `docs/open-items.html` keeps one line
  with the counts and a link. SR-225 stays as written; only the rows that name
  the page change.
- (b) A listing printed in the terminal (`pending.py`), with no page.
- (c) Amend SR-225 so that the record files are the listing. This changes the
  requirement's meaning, so it needs the operator's ruling.

**The operator's ruling (2026-11-19): option (c).** In the operator's words: "I
thought there was already a decisions.toml file? ... I think that would be the
preferable location. No html / more formally generated report needs to be
here." So the delegated-decisions record files themselves,
`docs/decisions/<run>.toml` (one per run), are where the operator reads the
entries, and an entry with no `operator` key is not yet seen. There is no
`docs/decisions.html`, no terminal listing and no other generated report.
SR-225 is amended to say so, and keeps every check it promises. A second
ruling the same day (B5) covers the code: tests and code that no longer serve
a requirement are cut with the section.

Whether the October backlog should be marked seen in bulk is a separate
question for the operator. It is not part of this item.

Text that names the section and will change with it: IF-074's contract (in
`gen_open_items.py` and `interfaces.toml`); LLR-118 and LLR-283; TC-123 and
TC-293's methods and evidence; the `Decisions to review` line `traj_status.py`
writes into `docs/status.md`, which links the page's anchor; and the header of
`project-trajectory/decisions.template.toml`, which ships. One more shipped
text names the section: the "Delegated decisions record" layer of
`project-trajectory/PROCESS_OPTIONS.md`.

**Which parts are rendering and which are checks.** `pending.decisions_to_review`
returns four things. The unseen entries (ordered high-risk first), the
overruled entries with their citing work items (`citing_rows`) and the
confirmed count exist only to draw section 4. The format findings are a
check: `kitlib.decisions.record_findings` over every record, whatever the
dial. Section 4 is the only place that reports them across all records; the
merge slot reports a closing lane's own record only, and only under a
recording dial. So the findings stay on the page, and the rest goes. The other
checks are not in this path and do not change: the overrule sync's refusal
(`acceptance_record`, through `kitlib.decisions.overrule_sync_lines`) and the
close refusal (`integrate`).

**The architectural delta.** No new file output, module, interface row or
generated view. `scripts/gen_open_items` (CMP-009) still owns
`docs/open-items.html`; IF-074's contract loses section 4 and gains the
findings notice closing section 3. `scripts/traj_status`'s line in
`docs/status.md` (IF-164) links `docs/decisions/` instead of the removed
anchor. `bootstrap_manifest.py`, `[generated]` in `docs/stack.ini` and
`trunk_step.py` do not change. `kitlib/decisions.py` changes in its docstring
only.

**What each state renders.**

- `docs/decisions/` absent: no findings notice on the page and no line in
  `docs/status.md`. A repo that records nothing has nothing unseen, which is
  not the same claim as having seen everything.
- Present, no record carrying a finding: the page shows nothing about the
  records. `docs/status.md` carries one line, the count of entries not yet
  seen (0 when every entry has a verdict), linking `docs/decisions/`.
- A record carrying a finding (an unparseable record included): a notice
  closing section 3 lists each finding, naming its file and entry.
- A confirmed or overruled entry is not counted. Its record shows the
  verdict. An overrule's open work cites the entry, and the overrule sync
  refuses the commit that sets `overruled` without it.

## Done-when

- [x] `docs/open-items.html` renders no "Decisions to review" section and no
      card for a delegated-decisions entry; its sections run 1 to 3. The code
      and tests that existed only to render the section are removed.
- [x] Each record's format findings are still reported, by file and entry, in
      a notice closing section 3 of `docs/open-items.html`, shown only when a
      record carries one. The overrule sync's refusal and the close refusal
      under a recording dial are unchanged.
- [x] `docs/status.md`'s line no longer links the removed anchor. It is one
      plain count of the entries not yet seen, linking `docs/decisions/`, and
      appears only when that directory exists.
- [x] SR-225 is amended to the ruling: the record files are where the operator
      reads the entries, an entry with no verdict is not yet seen, and every
      check it promised stays. IF-074 (its row and the `Contract IF-074:`
      block), LLR-118, LLR-283, TC-123 and TC-293 are amended to match, and
      IF-164's data names the new line. The shipped template header and
      `PROCESS_OPTIONS.md` say the operator reads not-yet-seen entries in the
      record files, and a RESYNC entry covers the shipped change.
- [x] The amended `Accepted` rows (SR-225, LLR-118, LLR-283, TC-123, TC-293)
      keep `status = "Accepted"` with their amended text, so they show as
      drifted on `docs/open-items.html` for the operator's re-accept. This
      row completes without that act; the build takes no operator act.
- [x] `gen_open_items.py --check`, `trace.py --strict`,
      `check_trajectory.py --strict` and the touched test modules pass.

## Critique dispositions

Round 1 (Gemini Argon, 2026-11-19,
`docs/reviews/2026-11-19-scope-critiques/WI-1009.md`): CHANGES-REQUESTED, four
MAJORs and two MINORs. The operator ruled S1 the same day, and the other five
are settled in that light. None grows the row.

- **S1, the surface: settled by the operator as option (c), not the critique's
  (a).** Quoted in the Context. The Context and the Done-when now name (c):
  no new page, SR-225 amended, the record files are the listing. The pieces
  land together on one branch, so `gen_open_items.py --check` and
  `trace.py --strict` hold at its tip.
- **S4, `planmode`: adopted as `planmode = "single"`.** The row touches four
  modules (one in its docstring only), a shipped template, a shipped document
  and seven registry rows, so a short plan precedes the code.
- **S3, the state space: adopted, and smaller under (c).** "What each state
  renders" closes it. No `docs/decisions.html` exists to render the cards,
  the confirmed count or the overruled list. The findings keep a home on the
  page; the count of unseen entries goes to `docs/status.md`.
- **S5, the architectural delta: adopted, and smaller under (c).** The
  Context's "architectural delta" states it: no new output or IF row, IF-074
  narrows, IF-164's link moves, nothing in the bootstrap manifest, the
  generated-view list or `trunk_step.py` changes.
- **B1, the rows named in the Done-when: adopted.** The fourth item names
  SR-225, IF-074, LLR-118, LLR-283, TC-123, TC-293 and IF-164.
- **B4, no operator act inside the row: adopted.** The fifth item says the
  amended rows stay `Accepted` and drift for a later re-accept, which this
  row does not wait for. SR-225's amendment needed the operator's ruling, and
  the ruling is given.
