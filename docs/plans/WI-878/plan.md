# WI-878 implementation plan: a dispute sitting's binding records the findings file it ruled, and the coverage gate reads exactly that file

Planner: a fresh session (Claude Opus), 2026-10-24. Sources read:

- the spec `docs/work/active/wi-878/WI-878-dispute-binding-findings.md`;
- its specref `project-trajectory/scripts/plan_coverage.py`;
- the dispute verdict it was filed from,
  `docs/reviews/wi-853-findings-gate-in-rework/006-ADJUDICATE-349bb13.md`,
  with its binding, and `docs/decisions/wi-853.toml` D-006;
- the producer and consumer code the spec's Trust section names:
  `kitlib/dispute.py`, `kitlib/sitting.py`, `adjudicate_brief.py`,
  `coordinator_adjudicate.py`, `review_brief.py` and `plan_gate.py`, all under
  `project-trajectory/scripts/`;
- `prompts/adjudicate-dispute.template.md` and `prompts/CATALOG.md`;
- the tests that exercise them;
- the rows SR-232, SR-234, SR-236, LLR-069, LLR-310, LLR-313, LLR-314,
  LLR-315, TC-069, TC-327, TC-333, TC-334, IF-060, IF-115, IF-283, IF-287,
  IF-290, CMP-006 and CMP-008, in `docs/requirements/system-requirements.toml`,
  `docs/requirements/low-level-requirements.toml`, `docs/test/test-cases.toml`,
  `docs/requirements/interfaces.toml` and `docs/requirements/components.toml`;
- Flow 6 of `docs/runtime-flows.md`;
- the coordinator-cycle skill's dispute-sitting and rework-coverage recipes.

The code was read in the lane worktree `C:/Projects/ai-template.wt/wi-878` at
its trunk base `a7c89a5da`.

DELTA: within

**The architectural-delta answer.** Yes on two of the four, and the plan's
rows carry both:

- *A value is added to a domain.* The binding's cell set gains a
  `findings_file` cell (IF-287), and the composed dispute brief's request
  gains a `FINDINGS-FILE:` line (IF-290). Both are optional on read, so every
  binding and brief written before this change still reads, as "record
  absent".
- *An output depends on a new input.* The coverage gate's verdict on a cited
  dispute exclusion now depends on the binding's record and on the one file it
  names. It stops depending on the input it reads today, the listing of
  `*.toml` files beside the verdict.
- *No new state.* The binding file, its one writer, the moments it is written
  (reservation, composition, the outcome rewrite) and its outcome alphabet are
  unchanged. The record is a cell, written by the same call as the requested
  ids.
- *No new boundary.* `plan_coverage` already reads the binding through
  `kitlib.sitting` (IF-287) and the findings file through `kitlib.dispute`
  (IF-290). `adjudicate_brief` already calls both. No module, component or
  seam is added, and CMP-006 and CMP-008 are unchanged.

P1 carries the IF-287 and IF-290 contract edits and Flow 6's bind step. P4 and
P5 carry the code. No sub-component split and no refactor outside this item
is needed.

## The design, decided

### 1. The record rides the brief (IF-290; LLR-314, LLR-315)

The entry point is handed only the composed brief, so the record reaches the
binding writer on the brief, as the requested ids do (the Trust section's
Producer).

- `kitlib/dispute.py` gains two pure functions:
  - `file_line(path)` returns `FINDINGS-FILE: <path>`;
  - `requested_file(brief_text)` returns the stripped text after
    `FINDINGS-FILE:` on the brief's FIRST such line, or `None` when there is
    none or it is empty. It uses the one-physical-line reading `requested_ids`
    uses (`_keyword_rests`).

  `request_line` and `requested_ids` are unchanged.
- **Why its own line, not a `file=` key on the `DISPUTE:` line.**
  `requested_ids` takes everything after `findings=` as the id list. A second
  key would change that parse for every brief and every existing reader. A
  path is free text to the end of its line, and a line of its own reads it
  whole.
- `adjudicate_brief.dispute_values` fills the template's `{request}` slot with
  `request_line(ids)`, a newline, then `file_line(scope[0])`. `scope[0]` is the
  `Adjudicates` token it has just read the file from (`Path(root) /
  scope[0]`), so the record is the file the brief was composed over, as the
  row writes it.
- The template's body is unchanged. Its `{request}` slot already sits before
  `{findings}`, so the composed line is the first such line, as `DISPUTE:` is.
  An adopter's override that renders `{request}` carries the line with no
  edit. The dispatcher note's `{request}` entry is updated (P6).

### 2. The binding records it (IF-287; LLR-310)

- `kitlib/sitting.py`:
  - `render_requested(brief, kinds, outcome="pending", identities=None,
    findings_file=None)` writes a `findings_file = <path>` line after
    `outcome` when `findings_file` is given, and nothing otherwise. Every
    non-dispute binding, and a dispute binding from a brief with no line,
    stays byte-identical to today's.
  - `write_binding(..., findings_file=None)` passes it through.
  - A new reader, `read_findings_file(text)`, returns the cell's stripped
    value, or `None` when the binding carries none or an empty one. It reads
    cells as `read_requested` does (one `" = "` split per line).
  - `read_requested` is unchanged and still ignores the cell.
  - The cell's name is one constant beside `IDENTITY_CELL`.
- `adjudicate_brief.bind_pending` passes
  `findings_file=kdispute.requested_file(prompt)` for a dispute brief, `None`
  otherwise. Both routes reach it with no change at their call sites: the
  entry point's `bind_requested` (exclusively, at reservation) and the loop's
  `session_body` (at composition). A brief with no line binds no record. The
  entry point does not refuse it: the Trust says it "binds without one".
- `adjudicate_brief.record_outcome` reads the binding's text once and carries
  both the identity cell and the record through its rewrite, accepted or
  failed, through the same writer.
- `coordinator_adjudicate.bind_requested` changes only in its docstring (what
  the binding holds).
- **Size watch.** `adjudicate_brief.py` measures 977 SLOC
  (`check_complexity.module_sloc`) against the module-size ratchet's
  1000-line threshold. This growth is about six lines. Keep it under 23, or
  the module enters the ratchet as an unlisted monolith and the exact-match
  test reds.

### 3. The gate reads exactly that file (LLR-069)

- **What stays.** `ruling_problem` keeps every check it makes today, in
  today's order: binding absent, not a dispute binding, outcome pending or
  failed, the verdict refused, the id unruled, the ruling not one that
  resolves. All of them come before any findings file is read, so every
  existing refusal message, `rules A FIX` included, is unchanged.
- **What changes.** Only the last step. `_correspondence_problem` takes the
  binding text `ruling_problem` has already read, in the same reading as the
  verdict (the working tree, or the commit `rev`). It no longer takes the
  verdict's directory and requested ids. Then:
  1. *No record* (`read_findings_file` is `None`): `cites <verdict>, whose
     binding records no findings file: re-sit the dispute, or exclude <F#>
     with a reason that cites no verdict`.
  2. *The recorded file cannot be read at that reading* (`_tree_text` is
     `None`: absent, a directory, or not in the commit): `cites <verdict>,
     whose recorded findings file <path> cannot be read`.
  3. *`kitlib.dispute.read_findings` refuses it*: `cites <verdict>, whose
     recorded findings file is refused: <its reason>`.
  4. *It records no finding under the ruled id*: `cites <verdict>, whose
     recorded findings file <path> records no finding <id>`.
  5. *It records another text under that id* (the `_finding_key` comparison,
     unchanged): `cites <verdict>, whose finding <id> is not this review's
     <F#>`. This is today's wording, kept.

  No arm reads any other file. `_ruled_texts`, `_tree_tomls` and the
  `posixpath` import are deleted.
- **No ids-equality check.** The gate does not check that the recorded file's
  ids equal the binding's requested ids. The spec's Ruling states no such
  check. The case it would catch, a findings file rewritten after its sitting,
  is outside the Trust section's supported-workflow bound, "with no guard".
- **Both routes inherit it with no code change.** They are the gate's command
  line (`resolution_findings`, from `_check_one`) and the pass-record step
  (`review_brief._ruled_findings`, read at HEAD). Only `_ruled_findings`'
  docstring changes, to "the findings file the verdict's binding records".
- **Docstrings.** The module docstring's Findings bullet and `ruling_problem`'s
  docstring are rewritten to the rule above.

### 4. What this plan does not change

- **The other readers.** `plan_gate._dismissals` (the pass-record check at a
  commit) is untouched, so a pass record filed before this change still passes
  the landing walk. These are untouched too: `kitlib.sitting`'s `accepted`,
  `accepted_at`, `accepted_identities`, `branch_verdicts`,
  `uncovered_refusal` and `unaccepted_refusal`, plus `held_status.py`,
  `kitlib/done_when.py` and `adjudicate_act.py`. `read_requested` ignores the
  new cell.
- **The SRs.** SR-236 is unchanged: its acceptance already refuses "another
  round's same-numbered finding" and "a finding that cannot be shown". P1
  walks SR-232 and SR-234 clause by clause. Neither states the binding's
  cells or the brief's lines, so this plan finds neither made untrue. Both
  stay the approved parents of LLR-310 and of LLR-314/LLR-315, and are amended
  only if P1's walk finds a clause that reads untrue.
- **Note (ii) of sitting 006.** That note covers a disputed finding excluded
  with a reason that cites no verdict. It is not taken here, because the
  Done-when does not name it.
- **No loop-route test.** No kit route mints a dispute row for the loop
  (Trust), and the loop binds through the same `bind_pending` the entry-point
  tests drive.

## The plan table

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | Spine intent set, TC-first, after the pass record and before build round 1: LLR-069, LLR-310, LLR-314, LLR-315, TC-069, TC-327 and TC-334 amended with the arms below, their trace cells naming P2's tests and P4/P5's symbols; IF-287 and IF-290 data and notes; Flow 6's bind step; SR-232 and SR-234 walked clause by clause; statuses unchanged; the arms map | D4; SR-236; SR-232; SR-234; TC-069; TC-327; TC-334 | IF-287; IF-290 | |
| P2 | Tests alone, before the code: eight new tests, seven as strict expected failures and one characterization; the plan-coverage dispute fixtures and the cap fixture record their findings file | D1; D2; D3; SR-236; SR-232; SR-234; TC-069; TC-327; TC-334; TC-333 | IF-060; IF-283; IF-287; IF-290; IF-115 | P1 |
| P3 | RESYNC_PACK.md section 3 entry anchored at the lane's trunk base, in or before the first commit that touches a shipped file | D5; SR-236 | no interface: adopter-facing prose naming the changed surfaces of IF-287 and IF-290 | P2 |
| P4 | Producer: `file_line` and `requested_file` (kitlib/dispute.py), the `findings_file` cell and `read_findings_file` (kitlib/sitting.py), `dispute_values`, `bind_pending` and `record_outcome` (adjudicate_brief.py), both contract docstrings and the entry point's docstring; P2's producer marks removed | D1; SR-234; SR-232; SR-236; TC-334; TC-327 | IF-290; IF-287; IF-115 | P3 |
| P5 | Consumer: `ruling_problem` reads exactly the recorded file and refuses a binding without it; `_ruled_texts` and `_tree_tomls` deleted; docstrings in plan_coverage.py and review_brief.py; P2's consumer marks removed | D1; D2; D3; SR-236; TC-069; TC-333 | IF-287; IF-290; IF-060 | P4 |
| P6 | Text: the dispute template's `{request}` note with the regenerated prompt catalog; the coordinator-cycle recipes drop the unique-ids workaround, three copies synced | D1; D2; SR-234; SR-236 | IF-290 (the template slot that carries its two lines); no code seam crossed | P4; P5 |
| P7 | Iterate: each tip attested through `integrate.py attest`, the lints after each build round, counted full-lane review rounds in the coordinator-cycle skill's shape | D1; D2; D3; SR-236; TC-069; TC-327; TC-334; TC-333 | IF-060; IF-287; IF-290 | P6 |
| P8 | Checkpoint: P1's set reconciled against settled code, the closure checks, one combined sitting over the amended rows with the IF contracts in the set, then the act turn | D4; SR-236; SR-232; SR-234; TC-069; TC-327; TC-334 | IF-287; IF-290 | P7 |
| P9 | Land: rebase onto trunk, the RESYNC entry re-anchored at the landing's parent, the full suite once, trunk-only views regenerated at the landing | D5; D4; SR-236; TC-069; TC-327; TC-334 | IF-287; IF-290; IF-060 | P8 |

## P1: the spine intent set

Terra authors the whole set once, through the coordinator's codex route,
after the pass record and before build round 1 (coordinator-cycle §3,
"Intent"; spine-authoring `references/in-lane.md`). Existing statuses stay
unchanged. These rows are on rungs the `human_approval_through` dial releases
at this base. Every new clause below has its TC clause in the arms map.

- **LLR-069 (the gate).** Replace "the findings file beside that verdict
  records the ruled finding with that F#'s text" with: the findings file the
  verdict's binding records, read in the same reading as the verdict and its
  binding, records the ruled finding with that F#'s text. Then add:
  - a binding that records no findings file refuses by name;
  - so does a recorded file that cannot be read at that reading, is outside
    the declared shape, records no such id, or records another text;
  - no other findings file is read.

  `code_symbol` loses `_tree_tomls` and `_ruled_texts`. Arms: the two-round
  pass, the cross-round refusal, record absent, and each of the four
  recorded-file refusals.
- **LLR-310 (the binding).** Add: a dispute binding also records the findings
  file its composed brief names. It is written by the one writer in the same
  call as the requested ids, on either route. The outcome rewrite carries it
  unchanged, as it carries the identity cell. A brief that names none binds
  none, which every reader reads as absent. `code_symbol` gains
  `read_findings_file`. Arms: bound at reservation; kept through an accepted
  and through a failed outcome; none from a brief without the line.
- **LLR-314 (the dispute grammar).** Add: the composed brief's findings-file
  line is written by `file_line`, and `requested_file` reads the path off its
  first such line, or none when there is no such line. `code_symbol` gains
  `file_line/requested_file`. Arms: written; read back; absent reads none.
- **LLR-315 (the dispute brief).** Add: the request value carries, after the
  requested ids, the findings-file line naming the one reference the
  assembler read. Arm: the composed brief names the row's findings-file
  reference.
- **TC-069.**
  - Method and Expected gain:
    - two dispute rounds in one lane reusing ids each resolve their own
      finding;
    - round 1's verdict cited for round 2's same-id finding refuses;
    - a binding without the record refuses by name with a matching findings
      file beside it;
    - a recorded file that is missing, a directory, not TOML, or records no
      such id refuses by name with a matching file beside it;
    - the pass-record route at HEAD refuses a dismissal bound without its
      record;
    - a dispute bound through the entry point resolves only its own round's
      finding.
  - Evidence gains the P2 tests T1 to T5 and T8.
  - Its existing "unshown" wording stays.
- **TC-327.** Method and Expected gain: a dispute brief's findings-file record
  is bound beside the verdict at reservation and kept through the outcome
  rewrite, accepted or failed; a brief without the line binds none. Evidence
  gains T7.
- **TC-334.** Method and Expected gain: the composed dispute brief names its
  findings file on a line the grammar reads back. Evidence gains T6.
- **IF-287.**
  - `data`: append "the dispute findings-file record cell and its reader".
  - `notes`: append "a findings-file record is carried the same way when a
    pending binding is rewritten as accepted or failed; an absent record reads
    as none".
  - No cell names a file.
- **IF-290.** `data` becomes `read_findings(text, where); request_line(ids);
  file_line(path); requested_ids(brief_text); requested_file(brief_text);
  parse(text, requested, where)`.
- **Flow 6 (`docs/runtime-flows.md`).** The step "reserve path and bind the
  judging brief and its judged rows' identities (LLR-306, LLR-359)" becomes
  "reserve path and bind the judging brief, its judged rows' identities and a
  dispute brief's findings file (LLR-306, LLR-359, LLR-310)". No other flow
  changes, and no flow is added.
- **SR-232 and SR-234.** Walked clause by clause, and amended only where a
  clause reads untrue (see "What this plan does not change").

## P2: the tests, and what each fails on before the change

They are committed alone, before any code (coordinator-cycle §3, "Intent",
step 2). New behaviour is marked
`@pytest.mark.xfail(strict=True, raises=(AssertionError, pytest.fail.Exception))`,
and each test's red reaches its own assertion, never an import or attribute
error: assertions are ordered so the first one that fails on today's code is
an assertion. P4 removes the marks on T6 and T7; P5 removes the rest. Every
fixture writes LF.

**Fixture changes, green before and after** (today's reader ignores an
unknown binding cell):

- `tests/test_plan_coverage.py`:
  - `write_dispute` gains `verdict=` (default `DISPUTE_VERDICT`) and
    `recorded=` (default: the repo-relative path of the first findings file it
    writes; `None` writes no record). It writes the literal line
    `findings_file = <path>`, so the tests pin the on-disk grammar.
  - The section comment above `REVIEW` says the findings file the binding
    records, not the one beside the verdict.
- `tests/test_plan_coverage.py::test_a_dismissal_whose_finding_cannot_be_shown_refuses`:
  - *"none" case.* No findings file and no record. It still refuses and says
    `no findings file` (arm 1's wording contains it).
  - *"two" case, re-specified.* The record names `004-DISPUTE-findings.toml`,
    which records LAUNCHER under F2, while `002-DISPUTE-findings.toml` beside
    it records the matching WORDING. It still refuses with `is not this`.
  - Adequacy witness, in the docstring: a gate that accepted any agreeing file
    beside the verdict would pass the re-specified case.
- `tests/test_plan_filing.py::cap`: the binding gains
  `findings_file = docs/reviews/wi-950/002-DISPUTE-findings.toml` (the
  `FINDINGS` constant), and a `recorded=True` parameter drops it. Without it,
  P5 would turn TC-333's cap tests red.

**New tests:**

- **T1**
  `tests/test_plan_coverage.py::test_two_dispute_rounds_reusing_ids_each_resolve_their_own_finding`
  (xfail).
  - *Setup.* One lane directory holds two rounds:
    - round 1: `002-DISPUTE-findings.toml` (F2 = an old typo finding) and its
      verdict `003-ADJUDICATE-abc1234.md`, ruling `F2 DISMISS` and bound with
      a record of 002;
    - round 2: `004-DISPUTE-findings.toml` (F2 = WORDING) and its verdict
      `005-ADJUDICATE-def5678.md`, bound with a record of 004.
  - *Expected.* Round 1's review (its F2 the typo) with a plan citing 003
    exits 0. Round 2's `REVIEW` with a plan citing 005 exits 0.
  - *Before the change.* Both exit 1, `F2 is not this review's F2`: the
    sibling scan reads both rounds' files.
- **T2**
  `tests/test_plan_coverage.py::test_round_ones_verdict_cited_for_round_twos_same_id_finding_refuses`
  (characterization, unmarked).
  - *Setup and expected.* T1's directory. Round 2's plan cites 003 for its
    F2, and the gate exits 1 with `F2 is not this review's F2`.
  - *Before the change.* It refuses as well.
  - *Adequacy witness, in the docstring.* A gate that resolved by the ruled id
    alone, or accepted any agreeing file beside the verdict (004 agrees), would
    pass it.
- **T3**
  `tests/test_plan_coverage.py::test_a_binding_without_the_findings_record_refuses_and_reads_no_sibling`
  (xfail).
  - *Setup.* An accepted `F2 DISMISS` bound with no record, and
    `002-DISPUTE-findings.toml` beside it recording the matching WORDING.
  - *Expected.* Exit 1, `whose binding records no findings file`.
  - *Before the change.* Exit 0: the sibling scan passes it. This is D2.
- **T4**
  `tests/test_plan_coverage.py::test_a_recorded_findings_file_that_cannot_show_the_finding_refuses`
  (xfail, parametrized over four arms).
  - *Arms.* The record names one of:
    - a missing file (`cannot be read`);
    - a directory named `*.toml` (`cannot be read`);
    - a file that is not TOML (`is refused`);
    - a file that records only F1 while the verdict rules F2 (`records no
      finding F2`).
  - *Setup.* Every arm has a `004-DISPUTE-findings.toml` beside the verdict
    that records the matching WORDING under F2.
  - *Expected.* Each arm exits 1 by name.
  - *Before the change.* Each arm exits 0: the scan skips the recorded file
    and the matching sibling passes it.
- **T5**
  `tests/test_plan_filing.py::test_at_the_cap_a_dismissal_bound_without_its_findings_file_is_refused`
  (xfail).
  - *Setup.* `cap(..., recorded=False)`.
  - *Expected.* `rb.write_pass` raises `BriefError` matching `records no
    findings file`, and no pass record exists. This is the HEAD route through
    `_ruled_findings`.
  - *Before the change.* The record is written: the sibling scan at HEAD
    finds `FINDINGS` beside the verdict, so `pytest.raises` fails with "DID
    NOT RAISE".
- **T6**
  `tests/test_dispute.py::test_the_dispute_brief_names_the_findings_file_it_was_composed_over`
  (xfail).
  - *Expected.* `ab.compose` over `_row()` gives a brief containing
    `FINDINGS-FILE: findings.toml`, placed after the `DISPUTE:` line and before
    the first finding block. Then:
    - `kdispute.requested_file(text) == "findings.toml"`;
    - `kdispute.requested_file("DISPUTE: findings=F1\n") is None`;
    - `ab.requested_for("dispute", text)` is still `("F1", "R2-3")`.
  - *Before the change.* The first assertion fails, since no such line is
    composed.
- **T7**
  `tests/test_coordinator_adjudicate.py::test_a_dispute_binding_records_its_findings_file_through_the_outcome`
  (xfail).
  - *Setup.* The `_dispute_call` pattern, with `DISPUTE_BRIEF` plus a
    `FINDINGS-FILE: docs/reviews/wi-1/002-DISPUTE-findings.toml` line after its
    `DISPUTE:` line.
  - *Expected.*
    - An accepted verdict leaves a binding with that `findings_file = ...`
      line and `outcome = accepted`.
    - A verdict leaving R2 unruled leaves the same line with
      `outcome = failed`.
    - Today's `DISPUTE_BRIEF` binds no `findings_file` line.
  - *Before the change.* No binding carries the line.
- **T8**
  `tests/test_coordinator_adjudicate.py::test_the_entry_points_dispute_binding_resolves_only_its_own_rounds_finding`
  (xfail).
  - *Setup.* The producer end to end:
    - the lane holds `docs/reviews/wi-1/002-DISPUTE-findings.toml` (F1 = text
      A, range `HEAD..HEAD`; an empty range composes, as
      `test_an_empty_lane_range_composes_and_says_it_holds_no_commits`
      shows);
    - the brief is composed through `adjudicate_brief.compose` over a dispute
      row naming that file;
    - it is sat through `coordinator_adjudicate adjudicate --brief dispute`
      with the verdict path `docs/reviews/wi-1/003-ADJUDICATE-abc1234.md`, the
      stubbed session writing `RULING: F1 DISMISS refuted ...`;
    - a later round's `004-DISPUTE-findings.toml` (F1 = text B) is then put
      beside it.
  - *Expected.* `plan_coverage.ruling_problem(root, RULING_CITE_RE.search(
    "<verdict>#F1"), "F1", A, resolving=RESOLVING)` is `None`, and with text B
    it returns the `is not this review's F1` refusal.
  - *Before the change.* The first call refuses: the scan reads 004, whose F1
    differs.

The eight tests run in the smoke tier, since none of the four modules is in
`SLOW_MODULES`. Their cost is reported by the commit bar and judged only at
the audit.

## P3: the RESYNC entry

- **Where.** In `project-trajectory/RESYNC_PACK.md` §3, after the last entry
  and before §4.
- **Heading.** `### A dispute sitting's binding records its findings file,
  and the coverage gate reads only that file [since a7c89a5da]`, followed by
  the "(Anchored at the preceding commit: the change lands in the commit
  after it.)" line.
- **When.** `scripts/check_resync.py` reads trunk base to working tree, so
  the entry is committed in or before P4's first commit.
- **What changed.**
  - The composed dispute brief names its findings file on a `FINDINGS-FILE:`
    line, inside the existing `{request}` slot.
  - The binding beside a dispute verdict records that path
    (`findings_file = <path>`), and the outcome rewrite keeps it.
  - An `F#` exclusion citing a dispute verdict is judged against that one
    file. A binding without the record refuses the citation by name, and the
    gate no longer reads other findings files beside the verdict.
- **Kit-owned files, overwrite.**
  - `scripts/plan_coverage.py`, `scripts/kitlib/sitting.py`,
    `scripts/kitlib/dispute.py`, `scripts/adjudicate_brief.py`,
    `scripts/review_brief.py` and `scripts/coordinator_adjudicate.py`
    (docstrings only in the last two);
  - `prompts/adjudicate-dispute.template.md` (its dispatcher note only) and
    `prompts/CATALOG.md`;
  - `skills/coordinator-cycle/`, a `scope: this-repo` skill, only if you
    vendored it.
- **What to do.**
  - A dispute sat before this change has no record, so a rework plan citing
    it now refuses. Re-sit the finding through the kit's route, or exclude it
    with a reason that cites no verdict.
  - Pass records already filed still pass the landing walk, since the plan
    gate's check is unchanged.
  - A `--prompt-map` override of the dispute template needs no edit if it
    renders `{request}`.
  - No setting or registry format changes.

## P4 to P6: the build

- **P4.** The code as design §1 and §2 state, in one commit. Then:
  - remove T6 and T7's marks;
  - update the IF-290 and IF-287 contract docstrings in `kitlib/dispute.py`
    and `kitlib/sitting.py`, plus the `bind_pending`, `record_outcome` and
    `bind_requested` docstrings, and the IF-115 paragraph of
    `adjudicate_brief.py`'s module docstring (the findings-file line beside
    the identity lines);
  - add `__all__` entries for the new names;
  - put an `Implements:` line on each new function: `SR-234, LLR-314` for
    `file_line` and `requested_file`, and `SR-232, LLR-310` for
    `read_findings_file`.
- **P5.** The code as design §3 states, in one commit. Remove the remaining
  marks (T1, T3, T4, T5, T8). Every touched function stays under the
  cognitive-complexity threshold of 15, so no `docs/complexity-baseline` row
  is added. `_correspondence_problem` scores 2 today and about 6 after.
- **P6.**
  - *The template.* The dispatcher note's `{request}` entry in
    `project-trajectory/prompts/adjudicate-dispute.template.md` becomes: "the
    `DISPUTE: findings=<ids>` line naming the findings to rule, then the
    `FINDINGS-FILE: <path>` line naming the file they were read from; the
    entry point binds both beside the verdict, and the coverage gate reads
    that file alone". `project-trajectory/prompts/CATALOG.md` is regenerated
    (`gen_prompt_catalog.py`) in the same commit: the hook's `prompt-catalog`
    step refuses a stale catalogue on a lane commit.
  - *The rework-coverage recipe.* In coordinator-cycle
    `references/recipes.md`, replace "or whose findings file beside the
    verdict records another finding under that id ... Until WI-878 binds the
    findings file into the sitting, keep finding ids unique within a lane: a
    second dispute reusing ids refuses a valid dismissal." with: "or whose
    findings file, the one its binding records, records another finding
    under that id. The gate reads no other file, so finding ids may repeat
    across a lane's sittings. A dispute bound before the binding recorded its
    file refuses: re-sit it, or exclude the finding with a reason that cites
    no verdict."
  - *The dispute-sitting recipe.* Step 1's "Keep the file after the sitting:
    the coverage gate reads it." becomes "Commit the file and keep it: the
    composed brief names it, its binding records that path, and the coverage
    gate reads that file alone."
  - *Sync.* `bootstrap.py --dest . --sync` brings `.claude/skills/` and
    `.agents/skills/` into step.

## P7 to P9: iterate, checkpoint, land

- **P7.** Each tip is committed through `integrate.py attest`, with `--tests`
  covering:
  - the touched modules: `tests/test_plan_coverage.py`,
    `tests/test_plan_filing.py`, `tests/test_dispute.py` and
    `tests/test_coordinator_adjudicate.py`;
  - the binding's other consumers: `tests/test_done_when_blessing.py`,
    `tests/test_adjudicate_brief.py`, `tests/test_adjudicate_act.py`,
    `tests/test_held_status.py` and `tests/test_integrate_admission.py`;
  - the text guards: `tests/test_prompts.py`, `tests/test_skills_sync.py`,
    `tests/test_resync_pack.py` and `tests/test_check_resync.py`.

  After each build round, run `trace.py --strict` and
  `check_trajectory.py --strict`. The commit bar, `run.cmd smoke`, runs on
  every commit. Then come counted full-lane review rounds in the skill's
  shape, the third in convergence stance. Row wording raised there goes to
  the spine change list.
- **P8.** Terra reconciles P1's set and the change list against settled code.
  The closure checks:
  - each row's parent is in the set or approved;
  - each TC names its LLR and that LLR's SR;
  - IF-287 is cited by TC-327 and TC-331, and IF-290 by TC-334;
  - `check_trajectory.py --strict` passes, and so does `trace.py` at the
    strictness the rung asks.

  Then one combined sitting, whose `Adjudicates` holds an `amendment:` token
  for each amended approved row (LLR-069, LLR-310, LLR-314, LLR-315, TC-069,
  TC-327 and TC-334, plus SR-232 or SR-234 only if P1 amended them). The
  IF-287 and IF-290 contract edits are in the set it is shown. The act turn
  follows from the accepted verdict. LLR-069's change is one of meaning on a
  released rung, so it acts only under the `[MEANING+BLESS]` mark.
- **P9.**
  - Rebase onto trunk and re-anchor the RESYNC entry at the landing's parent.
  - Re-sit only if the rebase changed code or authored rows.
  - Run the full suite once (`python -m pytest -q -n auto`).
  - At the landing, regenerate the trunk-only views the landing recipe lists,
    `docs/interface-reference.md` among them since IF-287 and IF-290 changed.
  - Run the commit bar on the landing tip.

## Risks the builder should watch

- **Order the fixture before the consumer.** P2's `write_dispute` and `cap`
  fixtures must carry the record before P5 lands, or P5's commit reds every
  existing dispute-citation test, TC-333's cap tests included.
- **Repo history after landing.** This repository's own dispute bindings
  carry no record. After landing, a rework plan citing one of them refuses:
  the recipe and the RESYNC entry say so. Filed pass records are unaffected.
- **The brief's line order.** The `FINDINGS-FILE:` line must precede
  `{findings}` in the composed brief, so that a finding's own text cannot
  supply the first such line. The template already orders it so; T6 pins the
  order.
- **The module-size ratchet.** Watch `adjudicate_brief.py`'s SLOC (design §2).
- **Keep the scope.** Make no change to `plan_gate.py`, and no ids-equality
  or path-normalization guard in the gate: both are outside the Trust
  section's bound, and adding them would grow the scope.
