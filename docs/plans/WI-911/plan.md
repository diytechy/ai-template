# WI-911 implementation plan: review-churn batch 1, text

Revision 2, the plan's one allowed revision. The in-lane single plan for
WI-911, written after the claim. Spec of record:
`docs/work/active/wi-911/WI-911-review-churn-b1-process-text.md`, with its
`specref` target, the "Owner rulings, 2026-10-11" section of
`docs/plans/2026-10-11-review-churn/README.md` (revisions 6 to 8, 33, 35, 36
and 37 included). Rows are this work item's steps, in build order. Inputs
read: SR-146, SR-154 and SR-235 in `docs/requirements/system-requirements.toml`,
the 15 TCs that verify them in `docs/test/test-cases.toml`, the touched rows
of `docs/requirements/interfaces.toml` and `docs/requirements/components.toml`,
and `docs/runtime-flows.md`. The first critique's one finding, F1, is covered
by P11 (reading 6).

Deliverable to step: 1 to P11, 2 to P10, 3 to P6, 4 to P9, 5 to P8, 6 to P2,
7 to P7, 8 to P3, P4 and P5.

## Readings this plan rests on

1. **The ordinary stance renders today's brief.** `review --stance
   convergence` adds its one fixed ROUND FACTS line. `ordinary`, given or by
   default, adds no line, so every ordinary attended brief, the loop's
   briefs (which never build a `Round`) and the template's slots stay as they
   are. That is how this plan reads D3's "an absent `--stance` renders the
   ordinary stance", and the spec's S2 answer and deliverable 7 speak of a
   convergence marking only.
2. **SUCCESSOR resolves a finding only for the consumer the Trust section
   names.** `plan_coverage.py --findings` excludes a finding whose cite is an
   accepted verdict ruling it SUCCESSOR, as it excludes a DISMISS. The single
   plan's cap is not in that consumer list, and SR-154's approved acceptance
   lets "only an accepted dispute dismissal" write a pass record. So the cap
   stays DISMISS-only (`plan_gate._dismissals`, unchanged), and P4 pins it.
3. **A reason that cites no verdict stays a plain reasoned exclusion**
   (SR-236 as approved). The gate does not read prose for a deferral claim:
   that would be a promise over an open grammar. That only the dispute
   sitting defers a BLOCKER or MAJOR is the coordinator's procedure, which P11
   states, as the spec's S2 answer puts it.
4. **Where each target cites its ruling (D1).** A shipped prompt's sent body
   names no record of this repository (CLAUDE.md's adopter rule; the
   `_RECORD_ID` rule in `tests/test_prompts.py`). Its ruling citation goes in
   its dispatcher or maintainer notes, a script's in its docstring or comment,
   and PROCESS.md's in its own dated "(owner ruling <date>)" form, as its §4
   already does. This repository's own files (the skill, the rubric, the
   Terra prompt) cite the plan's rulings directly.
5. **The convergence round's reading exclusion moves into the render.** The
   by-hand addendum kept a convergence reviewer out of `docs/reviews/` and
   out of the lane's decisions record, which summarizes every earlier finding
   (recipes §7, citing wi-913 D-009). P7's template paragraph carries that
   exclusion, so retiring the addendum in P11 loses nothing.
6. **The last round the cap allows runs in convergence stance.** Ruling 4
   says "the last allowed round runs in convergence mode", and item 4's own
   text keeps the cap's last round from becoming a fresh sample of the input
   space. The revision 7 clarification adds two uncounted rounds in the same
   stance, the gate over the checkpoint tip and a round over a rebase that
   changed code or rows, and withdraws nothing. The spec's deliverable 1
   names only those two, and its Context makes the ruling govern where the
   row and a ruling differ. So counted rounds 1 and 2 render the ordinary
   stance, and the third counted round renders `--stance convergence`, after
   the same convergence map as every convergence round (P11). A review after
   a fix round that the cap's sitting orders comes after the last allowed
   round, so it renders convergence too.

## Architectural delta

The four questions, answered for this row:

- **A new state?** No. Nothing new is stored: the dispute verdict and its
  binding exist today, and a review brief's convergence marking carries no
  authority (the spec's S2 answer).
- **A new value in a domain?** Yes, two. The dispute ruling set gains
  SUCCESSOR (P3), and `review` gains a closed stance domain, `ordinary` by
  default or `convergence` (P6). A finding gains one terminal disposition
  with it.
- **An output on a new input?** Yes, three. The critique brief depends on a
  fixed registry set and each file's presence (P6), a review brief on
  `--stance` (P6), and the rework coverage gate's exit on a SUCCESSOR ruling
  (P4).
- **A new boundary?** No. Every reader and writer exists today
  (`kitlib.dispute` and its readers, `review_brief`'s argument and exit
  seams, the prompt loader). Every changed module stays in its component in
  `docs/requirements/components.toml` (CMP-008, and CMP-006 for
  `plan_coverage`), and no component is added or split. No flow in
  `docs/runtime-flows.md` changes: none of the five crosses the attended
  review render, the dispute grammar or the rework coverage gate, and the
  loop's review sessions inside Flow 1 read the same reviewer template with
  their round facts empty, so its convergence paragraph never applies there.

The rows carry each change: the domain edits in P3 and P6, each consumer's
policy in P4 (the rework gate takes SUCCESSOR, the plan cap does not), and the
interface contracts in P3, P6 and P12 (IF-288, IF-289, IF-290). Reading 6
changes this repository's procedure text only (P11) and adds nothing here. No
refactor outside this row is needed.

DELTA: within

## Steps

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | The plan gate: this revision passes the coverage gate over the first critique's findings and a second, fresh critique, and its pass record is committed before any build commit | D5; SR-154 | IF-295 (the plan gate's hold, read by the commit check); IF-152 and IF-060 (the coverage gate the plan step runs) | |
| P2 | Terra's spine prompt states ruling 5 and stops sending a file name to SR acceptance | D1 | no interface: this repository's own prompt template, filled by its own coordinator tool | P1 |
| P3 | The dispute grammar gains SUCCESSOR, and any other unknown ruling still refuses the whole verdict | D1; D3; SR-234; TC-334 | IF-290 (the grammar every dispute reader calls) | P1 |
| P4 | The rework coverage gate excludes a finding an accepted verdict rules SUCCESSOR, and the plan cap stays DISMISS-only | D1; D3; SR-236; SR-154; TC-069; TC-333; TC-367 | IF-290 (plan_coverage requests the grammar); IF-060 (an accepted SUCCESSOR cite no longer exits 1) | P3 |
| P5 | The dispute brief offers SUCCESSOR, never for a convergence-class finding | D1; SR-234; SR-146; TC-334; TC-332; TC-157; TC-192 | IF-113 (the adjudication templates the composer loads); IF-097 (the catalogue digest) | P3 |
| P6 | review_brief.py: the critique names the registries; review gains a stance, ordinary by default, convergence as one fixed ROUND FACTS line, refused with a narrow scope | D1; D3; SR-146; SR-154; TC-333 | IF-288 (the command's arguments and outputs); IF-289 (exit 2 for a refused stance) | P1 |
| P7 | The reviewer template: severity tied to reachability, the fail-closed and fail-open classification, and the convergence stance | D1; SR-146; SR-233; SR-235; TC-332; TC-333; TC-082; TC-157; TC-192 | IF-099 (the REVIEWER template the loader serves); IF-097 (the catalogue digest) | P6 |
| P8 | spine-questions.md section 3 in ruling 5's contract voice, the traced module and code_symbol cells kept binding | D1; SR-146; TC-161; TC-157; TC-192 | IF-113 (the composed question home); IF-097 (the catalogue digest) | P1 |
| P9 | PROCESS.md section 3 states the record-at-event rule beside the guard rule; the byte-budget row is re-stamped | D1 | no interface: process text | P1 |
| P10 | The scope-critique rubric: S3, S4, the delta and dependency anchors, B3, B4, the widened artifact line and the verdict section | D1 | no interface: this repository's rubric, read through the critique brief P6 renders (IF-288) | P6 |
| P11 | The coordinator-cycle skill and its recipes carry the review shape with its convergence rounds (the third counted round among them), binding dispositions and the program's rules; the copies are synced | D1; D2; F1 | no interface: this repository's coordinator procedure, which gives the commands of IF-288 and IF-152 | P4; P5; P7; P10 |
| P12 | The spine change set: Terra drafts the amendments at intent, the checkpoint reconciles them, and one combined sitting judges them | D3; SR-146; SR-154; SR-235; SR-233; SR-234; SR-236; TC-333; TC-334; TC-069; TC-332 | IF-288; IF-289; IF-290 (the contract bodies and Drafted rows the change amends) | P2; P3; P4; P5; P6; P7; P8 |
| P13 | One RESYNC_PACK.md entry for the shipped changes, with no forced migration | D4 | no interface: the kit's re-sync reference text | P3; P4; P5; P6; P7; P8; P9 |
| P14 | Landing: the baseline manifest is on trunk, the lane lands alone, and the bar is green on the landing tip | D6; D7 | no interface change: the existing bar and the plan gate's landing walk (IF-295) | P11; P12; P13 |

Multi-covered clauses, by design. D1 names eight deliverables across ten
targets (deliverable 8 spans three), and each row from P2 to P11 delivers one
target with its citation, so D1 has ten covering rows and none duplicates
another's file. D3 names behaviours in three modules plus the trace rows: P3
(the parser), P4 (the coverage gate), P6 (the critique and the stance) and
P12 (the rows, sat).

## Step detail

Every new test below is named with what it fails on before the change. "Pin"
marks a test that passes before and after: it holds an existing behaviour
the change must not move, and is not claimed as red-before evidence.

### P1: the plan gate (D5)

WI-913's gate is on trunk (`b803dd019`) and in this lane's base, so the
build cannot start before it. The first plan was committed verbatim as
`docs/plans/WI-911/plan.md` and critiqued once. This revision replaces it
verbatim and must pass the coverage gate over the first critique's findings:

    plan_coverage.py --item <spec> --findings docs/plans/WI-911/critique-1.md docs/plans/WI-911/plan.md

Then a second, fresh critique from another family than the planner judges it
in convergence stance. An APPROVE, or a change request whose findings are all
MINOR, lets the pass record be written and committed alone. Otherwise the
second critique's BLOCKER and MAJOR findings go to one dispute sitting, and
only an accepted DISMISS of each lets the record be written; anything else
goes to the owner and the lane closes partial, never to the build. The
plan-gate hook step refuses any build commit before the record.

- Done when: `docs/plans/WI-911/pass.toml` is committed, and the first build
  commit passes the hook's plan-gate step.
- Tests: adds none. The gate is WI-913's, under TC-367.

### P2: Terra's spine prompt (deliverable 6; ruling 5, revisions 35 and 36)

Target: `scripts/coordinator/terra-spine-prompt.template.md`. This
repository's tooling, so no RESYNC entry.

- The R2 line (line 13) is replaced by ruling 5 as refined:
  - text the turn writes into a requirement row names no implementation
    carrier (a code file, function or symbol);
  - SN and SR rows name no file in any cell, acceptance included:
    current-carrier evidence lives in the TC rows that verify them, never in
    SR acceptance;
  - a shipped boundary artifact (a registry, template, config file or
    launcher) may be named in LLR and TC rows only;
  - LLR text is written in contract voice, by pointer to `spine-questions.md`
    section 3, never by a copy of it;
  - an approved cell amended by addition keeps its approved text verbatim,
    names included, as recipes §5 already briefs Terra, until item 5's schema
    lane migrates it;
  - the traced `module` and `code_symbol` cells stay filled and binding until
    item 5's schema lane removes them (`trace.py --strict-schema` requires
    both; `check_doc_refs --strict` binds the symbol);
  - "One decision per row; one `shall`" stays.
- The back-link line (14) and the TC evidence line (15) stay: both cells
  remain binding until item 5's migration.
- It lands in build round 1, before Terra's intent turn, so this lane's own
  spine set (P12) is drafted under it.
- Done when: no line sends a file name to SR acceptance as current-carrier
  evidence, the new line cites ruling 5 and revisions 35 and 36, and it
  agrees with recipes §5's amend-by-addition rule.
- Tests: adds none, since no test reads this template. The evidence is the
  corrected line, checked by inspection.

### P3: SUCCESSOR in the dispute grammar (deliverable 8, part 1; owner, 2026-10-14, in session)

Target: `project-trajectory/scripts/kitlib/dispute.py`.

- `RULINGS` becomes `("FIX", "SUCCESSOR", "DISMISS", "ESCALATE")`. SUCCESSOR
  takes no reason class, and like FIX and ESCALATE it needs a reason on its
  own line. `parse` stays the one parser, and a ruling outside the set still
  refuses the whole verdict.
- The module docstring's verdict grammar gains `RULING: <id> SUCCESSOR <why>`
  with its meaning: the finding becomes a successor row, filed on trunk at
  the landing from the sitting's binding. The docstring cites the ruling.
- Every reader takes the new value through `parse`.
  `adjudicate_brief.verdict_refusal` and the adjudication entry point accept
  it and bind the call `accepted`. `plan_coverage.ruling_problem` resolves it
  for the rework gate only (P4). `plan_gate._dismissals` still refuses it
  (P4's pin).
- Tests:
  - `tests/test_dispute.py::test_a_successor_ruling_is_accepted_and_parsed`:
    `parse` returns `("SUCCESSOR", None, <why>)`, and `verdict_refusal`
    accepts the file. Fails before: the reason says the ruling is not one of
    FIX, DISMISS or ESCALATE.
  - `tests/test_dispute.py::test_a_malformed_or_incomplete_verdict_is_refused`
    gains a SUCCESSOR with no reason, refused as "gives no reason". Fails
    before: the refusal names an unknown ruling instead. It also gains
    lowercase `successor` and `SUCCESSORS`, still refused (pins).
  - `tests/test_dispute.py::test_an_unknown_ruling_is_refused_naming_the_four_rulings`:
    `WONTFIX` is refused, naming FIX, SUCCESSOR, DISMISS and ESCALATE in
    `RULINGS` order. Fails before: the reason names three rulings.
  - `tests/test_coordinator_adjudicate.py::test_a_dispute_verdict_ruling_a_finding_successor_is_valid_and_bound`:
    the entry point exits 0 and binds `outcome = accepted`. Fails before:
    exit 1, `outcome = failed`. It is the smoke-tier pin of the grammar,
    since `tests/test_dispute.py` has been slow-tier since WI-869.
- Runs: TC-334's evidence.

### P4: the rework coverage gate takes SUCCESSOR; the plan cap does not (deliverable 8, part 3)

Target: `project-trajectory/scripts/plan_coverage.py`.

- `ruling_problem` takes the resolving set of the consumer calling it, a
  `resolving` keyword whose default is today's `("DISMISS",)`. The plan
  cap's filing check, `review_brief._ruled_findings`, keeps calling it
  unchanged, so that seam does not move. `resolution_findings`, the
  `--findings` exclusion path, passes a named constant,
  `RESOLVING = ("DISMISS", "SUCCESSOR")`.
- Every other refusal of a cite is unchanged: a verdict or binding that is
  absent, a binding that is not a dispute's, an outcome other than accepted,
  a refused parse, a verdict that does not rule that id, and a findings file
  beside it that records another finding under the id. Each leaves the
  finding open. The refusal names the set its consumer accepts: "only a
  DISMISS or a SUCCESSOR resolves a finding" here, and "only a DISMISS" at
  the cap.
- The module docstring's exit-1 list and the docstring of `ruling_problem`
  say the same, and both cite the ruling.
- The plan cap, `plan-file --pass` and the commit-time gate, stays
  DISMISS-only through `plan_gate._dismissals`, unchanged. SR-154's approved
  acceptance requires that.
- Tests:
  - `tests/test_plan_coverage.py::test_a_successor_ruling_citing_its_verdict_passes`:
    the plan excludes F2 citing an accepted verdict that rules F2 SUCCESSOR,
    and its findings file records F2 as written. Exit 0, with the exclusion
    listed. Fails before: exit 1, "cites a refused verdict".
  - `tests/test_plan_coverage.py::test_a_successor_ruling_of_another_finding_refuses`:
    a SUCCESSOR of F1 cited for F2, and another round's F2 under the same id,
    each exit 1 with "is not this review's F2". Fails before: the parse
    refusal comes first, so the correspondence message is never reached.
  - `tests/test_plan_coverage.py::test_a_cited_ruling_that_does_not_dismiss_refuses`
    gains a SUCCESSOR verdict whose binding is pending, refused with
    "outcome pending" (a pin: binding is read before parse, so the message is
    the same before). Its FIX and ESCALATE cases now assert that the refusal
    names "a DISMISS or a SUCCESSOR". That fails before, when it names
    DISMISS alone.
  - `tests/test_plan_filing.py::test_at_the_cap_a_successor_ruling_never_passes`:
    an accepted verdict ruling the second critique's blocking finding
    SUCCESSOR writes no pass record. The refusal says "rules it SUCCESSOR" and
    "only a DISMISS", and nothing in it says SUCCESSOR resolves. Fails
    before: the verdict is refused as malformed, so neither phrase appears.
- Runs: TC-069, TC-367 (the cap's code is unchanged, but the grammar it
  parses grew) and TC-333's plan-filing arms.

### P5: the dispute brief offers SUCCESSOR and bounds it (deliverable 8, part 2)

Target: `project-trajectory/prompts/adjudicate-dispute.template.md`.

- A Method bullet for SUCCESSOR: the finding is real, in scope and worth its
  change, but belongs in its own row rather than this lane. The sitting says
  in one line what that row must do, and the row is filed on trunk when the
  lane lands, from this verdict. A convergence-class finding (fail-open, data
  loss or a Done-when gap) is never ruled SUCCESSOR: it is ruled FIX or
  escalated.
- The machine-line block gains `RULING: <id> SUCCESSOR <what the successor
  row must do, on the same line>`. The closing refusal sentence is
  unchanged.
- No new slot. The §6 threat-model link stays, and no boundary example is
  restated. The sent body names no record of this repository; the
  dispatcher notes cite the ruling.
- `prompts/CATALOG.md` is regenerated (`gen_prompt_catalog.py`) in the same
  commit.
- Tests:
  - `tests/test_prompts.py::test_the_dispute_brief_offers_successor_and_never_for_a_convergence_class_finding`
    pins the SUCCESSOR machine line and the convergence-class bound. Fails
    before: the template has no SUCCESSOR.
- Runs: the brief-composition tests in `tests/test_dispute.py` (TC-334), the
  TC-332 test (the brief still cites §6 and restates none of its examples),
  TC-157 and TC-192 (the catalogue is fresh).

### P6: `review_brief.py`: the critique names the registries; review gains a stance (deliverable 3)

Target: `project-trajectory/scripts/review_brief.py`, the move in its own
commit first.

- **(a) A structural move, in its own commit** (PROCESS.md §3, "A structural
  move is its own commit"). No test pins the planner brief's input lines
  today: the planner-brief tests in `tests/test_plan_pass.py` assert its
  clauses, contract and delta question, never those lines. So a pin lands
  first, `tests/test_plan_pass.py::test_the_planner_brief_names_each_input_by_its_registry`:
  over a tmp lane holding one of the five registries, the brief carries each
  input's line exactly as today, its label and path, and marks the four
  missing ones "(absent here)". It passes on its parent. Then the move
  commits alone: `_PLAN_INPUTS` and `_input_lines` become one table of named
  registry inputs (a label and a repo path) and one renderer, from which the
  planner's brief selects today's five. The pin passing unchanged is the
  move's evidence, and the "absent here, never dropped" rule then has one
  home.
- **(b) The critique (`render_critique`).** Beside the spec and its
  `specref` target, the artifact recipe names the fixed registry set, each
  as a registry and never code:
  - `docs/requirements/components.toml`;
  - `docs/requirements/interfaces.toml`;
  - `docs/requirements/components.derived.toml` (the derived architecture);
  - `docs/runtime-flows.md`;
  - `docs/dependencies.md`.

  A path the repository lacks is marked "(absent here)", which is the
  adopter case for the dependency ledger. `critique --plan` is unchanged.
- **(c) The review (`--stance`).**
  - The flag takes `ordinary` (the default) or `convergence`, its choices
    drawn from one `STANCES` constant.
  - `Round` gains `stance`, defaulting to ordinary. It refuses an unknown
    stance, and convergence with a narrow scope, with `BriefError`: exit 2,
    one "REFUSED" line, no brief.
  - `round_facts` renders convergence as one fixed line, a module constant on
    one physical line, placed after the range line. It marks the round and
    points at the template's convergence stance (P7), restating none of it.
    Ordinary renders no stance line.
- The module docstring's Contract IF-288 gains the flag and the critique's
  registry list. Contract IF-289 gains the refusal of a narrow round in
  convergence stance. Usage gains the convergence example. The new code
  cites revision 8 and ruling 4 (the stance) and item 12's revision 20 (the
  registries). New tagged symbols carry `Implements: SR-146, LLR-313`, and
  LLR-313's `code_symbol` follows them (P12).
- Tests, all in-process in `tests/test_review_brief.py` (smoke tier), apart
  from (a)'s pin. The command-line cases patch `lane_commits`, as the
  existing unfilled-slot test does.
  - `test_the_scope_critique_names_the_registries_beside_the_spec`: over a
    tmp lane holding four of the five registries, and a stub rubric that
    names none of them (so only the render can put a path in the brief),
    the brief names all five, marks only the missing one "(absent here)",
    says they are registries and never code, and leaves no slot. Fails
    before: none of the five paths is in the brief.
  - `test_a_convergence_round_renders_the_one_fixed_stance_line`: a
    convergence brief carries the constant exactly once, after the ROUND
    FACTS header and beside the FULL-LANE line, and the constant holds no
    newline. Fails before: `Round` takes no `stance` (TypeError).
  - `test_an_absent_stance_renders_the_ordinary_round`: `Round()` has stance
    ordinary, and its brief equals an explicit ordinary brief and carries no
    stance line. The command line with no `--stance` writes the same bytes as
    `--stance ordinary`. Fails before: `stance` and `--stance` are unknown.
  - `test_a_narrow_round_refuses_the_convergence_stance`: `Round(scope=
    "narrow", findings=..., stance="convergence")` raises `BriefError`
    naming the stance. The command line exits 2 with a "REFUSED" line naming
    convergence and writes no brief, and an unknown stance value is refused by
    the parser. Fails before: TypeError rather than `BriefError`, and the
    command line's exit 2 comes from argparse's "unrecognized arguments",
    with no "REFUSED" line. The test asserts the reason, never the bare exit
    code.
- Runs: all of TC-333's evidence.

### P7: the reviewer template (deliverable 7)

Target: `project-trajectory/prompts/reviewer.template.md`.

Constraints: no new slot (an adopter's override would fail preflight, a
forced migration), no second machine line, no re-wrap, every pinned phrase
intact, and "Write your verdict to" not repeated (the fake-CLI harness
matches it).

- **Severity tied to reachability (item 4).** A BLOCKER or MAJOR states a
  scenario reachable in normal use, or a fail-open, data-loss or security
  path. A rare or contrived edge case is at most MINOR. It sits beside the
  §6 threat-model sentence and restates none of §6's examples.
- **Classification (item 1).** An input outside the spec's declared set that
  the change fails closed on is a coverage-extension note: prose outside the
  finding lines, with no severity bracket, so it never moves the count. One
  the change fails open on stays a finding at its severity. The reviewer
  decides which, not the set's author.
- **The convergence stance**, for a round whose round facts say so (P6's
  line):
  - read no earlier verdict and no record of one: nothing under
    `docs/reviews/` or `docs/decisions/`;
  - confirm each fix through its regression test failing on the pre-fix
    code, or, for a fix with no executable test, through independently
    checkable evidence (the corrected text at the cited site, or an
    inspection record);
  - check each Done-when item's coverage, and look for regressions;
  - tag each new BLOCKER or MAJOR, in its own finding line, as
    convergence-class (fail-open, data loss or a Done-when gap) or not.

  The tag is advice to the dispute sitting, which alone defers a finding.
  The verdict's grammar, its word and its count are unchanged.
- The dispatcher notes cite ruling 1, ruling 4, revision 8 and revision 33.
  `prompts/CATALOG.md` is regenerated in the same commit.
- Tests:
  - `tests/test_prompts.py::test_the_reviewer_brief_ties_severity_to_reachability_and_classifies_out_of_set_inputs`.
    Fails before: neither clause exists.
  - `tests/test_prompts.py::test_the_reviewer_brief_states_the_convergence_stance`
    pins the four duties, the reading exclusion and the unchanged grammar.
    Fails before: there is no such paragraph.
  - `tests/test_review_brief.py::test_a_convergence_brief_carries_the_stance_and_its_marking`:
    a convergence render carries the paragraph and P6's line, and an ordinary
    render carries the paragraph but not the line. Fails before: there is no
    stance.
  - `tests/test_review_brief.py::test_a_convergence_tagged_finding_files_with_its_count_unchanged`:
    a review whose MAJOR line carries the tag files as one finding, and the
    rollup shows one. A pin: it holds deliverable 7's "grammar unchanged".
- Runs: `tests/test_agent_loop_review.py` whole (TC-082's arms, plus the
  arms of TC-084 and TC-257 in that module), TC-082's other nodes, the
  TC-332 test, TC-157 and TC-192.

### P8: `spine-questions.md` section 3 (deliverable 5)

Target: `project-trajectory/prompts/spine-questions.md`.

- The first bullet of section 3, "LLRs name modules and symbols by design",
  becomes ruling 5's contract voice:
  - an LLR's text states the observable obligation (its inputs, outcome and
    refusal boundary), in words that survive a refactor that keeps
    behaviour;
  - it names no implementation carrier; a shipped boundary artifact may be
    named at the LLR and TC tiers, and SN and SR rows name no file in any
    cell;
  - no concrete name is laundered up into the SR;
  - the traced `module` and `code_symbol` cells stay filled and binding
    while the schema requires them (`trace.py --strict-schema` requires
    both; `check_doc_refs --strict` binds the symbol), so a sitting never
    returns a row for keeping them;
  - "No `shall` in an LLR" stays.
- Section numbers are kept. The composed body names neither "item 5" nor any
  record of this repository; the maintainer notes cite ruling 5 and
  revisions 35 and 36.
- The new bullet's opening appears in no kit template and no
  `spine-authoring` file: `test_no_second_copy_of_the_questions_exists`, a
  TC-161 arm, refuses a copy there. Terra's prompt (P2) lies outside that
  test's reach and points at section 3 rather than copying it, by the same
  one-home rule.
- `prompts/CATALOG.md` is regenerated: the composed question home stales it.
- Tests:
  - `tests/test_prompts.py::test_the_llr_questions_ask_for_contract_voice_and_keep_the_trace_cells_binding`.
    Fails before: the old bullet is present and the new clauses are absent.
- Runs: TC-161 (its tier-question composition arms compose section 3 into
  the first-approval, amendment and combined briefs), TC-157 and TC-192.

### P9: the record-at-event rule (deliverable 4, ruling 2)

Target: `project-trajectory/PROCESS.md` §3, directly after "When a guard is
owed".

- A bold-lead bullet: a decision a later step depends on is recorded by the
  step that makes it, in the commit where it is made, and checked against
  that commit's parent. A later reader trusts the record and never
  recomputes it from history or from current state. It closes with "(owner
  ruling 2026-10-11)".
- Shipped text, so it is in P13's entry.
- `byte-budget-guard` before and after. PROCESS.md is a watched file
  (baseline 96,606), so its row is re-stamped with the byte delta and
  reason. The skill's own capped row is re-stamped until its baseline equals
  its new size. The source and both copies (`.claude/skills/`,
  `.agents/skills/`) go in one commit through `bootstrap.py --dest . --sync`.
- Tests:
  - `tests/test_prompts.py::test_the_record_at_event_rule_has_one_home`: the
    lead occurs once in PROCESS.md, directly after the guard bullet. Fails
    before: there is no such bullet.
- Runs: TC-157's module evidence (the new test joins `tests/test_prompts.py`,
  which TC-157 cites whole, beside the fan-out and threat-model one-home
  tests), and `tests/test_bootstrap.py -k "byte_caps or size_budget or
  capped_doc_baselines"`.

### P10: the scope-critique rubric (deliverable 2)

Target: `docs/rubrics/scope-critique.md`, this repository's rubric, so no
RESYNC entry.

- **S3: coverage is closed (ruling 1).** A promise over an input space is an
  enumerated set with a declared default, or a construction that makes the
  space irrelevant; for an unbounded grammar the spec chooses deny by
  default, and the answer becomes spec text before the claim.
- **S4: the planning need (ruling 9),** recorded as `planmode`, on its
  three criteria, with no size threshold.
- **S5: the architectural delta,** in item 12 entry point 2's own words.
  Within scope, the spec carries the change; beyond it, a refactor row is
  filed on trunk before the claim. It points at no rubric that does not
  exist yet.
- **S6: dependencies,** each in `needs` with its reason, and any new
  third-party package, tool or service with a reviewed row in
  `docs/dependencies.md` before the build.
- **B3** (ruling 2) and **B4** (revision 35).
- **The widened artifact line:** the spec file, its `specref` target, and
  the five registries P6 names, which are registries, never code.
- **The verdict section:** every recommendation will be dispositioned
  before the claim, so each is one concrete change. In a confirming round, a
  new finding is BLOCKER or MAJOR only if it is fail-open, data loss or a
  Done-when gap, and a failed confirmation keeps its original severity.
- S1 and S2 are kept, so the existing render test still finds their
  phrases. The S5 and S6 ids are this plan's proposal, for the critic to
  judge.
- Tests:
  - `tests/test_review_brief.py::test_the_scope_rubric_names_every_registry_the_critique_brief_renders`:
    every path P6's critique brief names appears in the live rubric's
    artifact line, and the rubric declares S3 to S6, B3 and B4. Fails
    before: the rubric names no registry.

### P11: the coordinator-cycle skill and recipes (deliverable 1, D2, F1)

Targets: `project-trajectory/skills/coordinator-cycle/SKILL.md` and
`references/recipes.md`. This is a `scope: this-repo` skill, so no RESYNC
entry. Each rule cites its ruling: the plan's rulings section by link once,
then the ruling or revision number.

- **Roles and the review shape** (rulings 4 and 7, revisions 6 to 8, 33 and
  37):
  - no narrow rounds;
  - each round runs the full-lane reviewers in parallel, each from its own
    `review_brief.py review --scope full` render with its own `--scratch`,
    hence its own verdict path and `--basetemp`;
  - REVIEW-A is Codex Sol at medium. REVIEW-B is another family or model: a
    Claude stand-in, recorded as a substitution in the lane's decisions,
    until WI-815's Gemini route has one verified launch;
  - a Claude reviewer is a sub-agent given only its brief's path;
  - the program's third-reviewer trial: both Claude reviewers file REVIEW-B
    under their own numbers, and the lane's decisions name the model behind
    each file and who raised each accepted finding. Nothing is built for a
    third slot;
  - the Roles table and its independence line say so, and a Codex-outage
    substitute (the "Never" list's fresh Opus reviewer, recipes §7's Luna)
    names the REVIEW-A slot it fills.
- **Rounds and the cap** (ruling 4, revision 7):
  - at most three counted full rounds before the checkpoint, run until one
    has no BLOCKER or MAJOR code finding, and the checkpoint follows it;
  - counted rounds 1 and 2 render with no `--stance`, the ordinary default;
  - the third counted round, the last the cap allows, renders
    `review --scope full --stance convergence` (ruling 4: the last allowed
    round runs in convergence mode), only after the convergence map below;
  - the gate over the checkpoint tip, and a round over a rebase that changed
    code or rows, run uncounted and render `--stance convergence` after the
    same map (revision 7), as does a review after a fix round the cap's
    sitting orders (reading 6);
  - at the cap, and after a convergence round, every open BLOCKER or MAJOR
    goes to one dispute sitting (FIX, SUCCESSOR, DISMISS or ESCALATE), and
    only that sitting moves a finding to a successor row;
  - a convergence-class finding is never deferred: the sitting orders one
    more fix round or escalates;
  - successor rows are filed on trunk at the landing, one per SUCCESSOR
    ruling of an accepted verdict, from its binding; without one nothing is
    filed and the finding holds the landing (the spec's Trust section);
  - a MINOR goes to the spine change list or a successor row;
  - an in-flight lane restarts its count at zero, recorded as a decision.
- **The convergence round:** before each one (the third counted round, the
  checkpoint-tip gate, a rebase round, a review after an ordered fix round),
  the coordinator maps every accepted finding to a regression test that
  fails on the pre-fix code, or to checkable evidence, and records the map in
  the lane's decisions, which the reviewers do not read. A round that cannot
  be mapped in full does not start.
- **What reviewers get:** the WI definition, never the coverage plan. This
  removes iterate step 2 and "carry the table into the next review"; the
  builder writes one coverage plan per round file. The checkpoint's
  first-review shortcut (one fresh full-lane review as both the first review
  and the gate) goes with them: a counted round precedes the checkpoint, and
  the gate follows it.
- **Before the claim** (rulings 1 and 9; owner, 2026-10-14):
  - every critique recommendation is dispositioned, adopted (quoting the
    carrying spec text) or rejected (with a reason);
  - a confirming round, in convergence stance, confirms the adoptions before
    the claim, marked by one appended line, because the rubric now holds the
    rule (P10);
  - a queued row born before S3, S4 and the delta question is re-critiqued
    when it comes up for claim, one at a time.
- **Lints after each build round** (ruling 6): `trace.py --strict` and
  `check_trajectory.py --strict` with the commit bar, at the closure check
  and at the landing check, never in the hook.
- **Sub-agents** (revision 37), within the bounds the ruling states. This
  section never restates PROCESS.md §6's fan-out sentence:
  `test_the_fan_out_rule_has_one_home_and_no_brief_or_skill_restates_it`
  refuses that phrase in any skill.
- **Tests across lanes** (owner, 2026-10-14): one basetemp per runner, a
  quiet budget reading at landing, the disk checked before fan-out, the
  full suite alone at phase close, and a red that passes when re-run quietly
  filed as a load-sensitive defect.
- **§4's two landing rules:** a mechanism change lands alone, and the next
  waits for the cycle to run through the changed step. A defect is fixed
  forward in a lane with a regression test, never by a revert. A step it
  blocks runs by hand, attended and recorded, never through a bypass flag or
  fallback, and a hook that refuses the fix commit is the owner's to decide.
- **§3's plan cap:** a FIX, SUCCESSOR or ESCALATE goes to the owner.
- **Recipes:**
  - §1's review recipe becomes the full-lane recipe for both slots: rounds 1
    and 2 render with no `--stance`; the third counted round, the
    checkpoint-tip gate, a rebase round and a review after an ordered fix
    round render with `--stance convergence`, each only after the
    convergence map is recorded; each review files with
    `file --phase REVIEW-A` or `file --phase REVIEW-B`; its step 2 (the
    appended coverage plan and the narrow-round wording) goes;
  - the coverage-plan and dispute recipes take the SUCCESSOR ruling and its
    exclusion form
    `successor: docs/reviews/<lane>/NNN-ADJUDICATE-<sha7>.md#<id>`;
  - §3 gains successor-row filing at the landing;
  - §7's by-hand addendum bullet and "keep review rounds narrow" go; the
    bullet's launch detail for a Claude reviewer (the brief's path, the lane
    worktree, a two-line reply) moves to the review recipe;
  - §8's "a narrow sitting" is reworded, so no review-round sense of
    "narrow" is left.
- Done when:
  - `grep -n -i -E "narrow|one fresh Sol|Sol gate|Sol review|Opus reviewer|single reviewer"`
    over both files finds no line describing a narrow review round or a
    single code reviewer; the scope and plan critiques keep their one
    critic, since ruling 4's reviewer count governs review rounds only;
  - both files state, citing ruling 4, that the third counted round renders
    `review --scope full --stance convergence` only after the convergence
    map is recorded, as the checkpoint-tip gate, a rebase round and a review
    after an ordered fix round do: `grep -n -- "--stance convergence"` over
    both files finds each case, and each hit is read at its site;
  - D2: `bootstrap.py --dest . --sync` leaves `.claude/skills/coordinator-cycle/`
    and `.agents/skills/coordinator-cycle/` byte-equal to the source
    (`diff -r` clean), committed together, and `check.py`'s `skills-sync`
    step passes;
  - the fan-out test still passes.
- Tests: adds none. This is this repository's procedure text, and its
  evidence is the corrected text at each cited site.

### P12: the spine change set (D3's trace rows)

Terra drafts once at intent, after build round 1, under P2's prompt. It
amends approved rows by addition, in contract voice (recipes §5), and keeps
any new row Drafted. The candidate set:

- **SR-234, LLR-314, TC-334.** The ruling set gains SUCCESSOR. TC-334's
  evidence gains P3's tests, and its tier follows recipes §5's rule: it
  cites `tests/test_dispute.py`, which has been slow-tier since WI-869.
- **SR-236, LLR-069, TC-069.** An accepted dismissal or successor ruling of
  the same finding resolves a rework exclusion, and the plan cap's
  correspondence check keeps DISMISS. TC-069's evidence gains P4's coverage
  tests.
- **LLR-313, TC-333.** The stance (ordinary by default, convergence as one
  fixed line, refused with a narrow scope) and the critique's registry set.
  TC-333 gains P4's cap pin and the P6 and P7 render and filing tests.
  `code_symbol` takes any new tagged symbol, a traced-only cell.
- **SR-233, LLR-311, TC-332.** Reachability-tied severity, the
  classification clause and the dispute brief's convergence-class bound,
  with the P5 and P7 template pins as evidence. Whether SR-233's acceptance
  changes, or LLR-311 alone carries them, is Terra's draft and the sitting's
  call.
- **IF-288, IF-289, IF-290** (Drafted, no act). Their contract bodies are
  already edited in P3 and P6. IF-288's data cell is at 153 of its 160
  characters, so `--stance` lives in its contract body. IF-290's requestors
  gain `scripts/plan_gate` and `scripts/review_brief`, which read the grammar
  today and are this change's counterparts, in the cell's current
  module-path form, which item 11's migration replaces.
- No new SN or SR. A new LLR only where the sitting finds an obligation no
  approved row can carry by addition.

At the checkpoint, Terra (resumed) reconciles the set against the settled
code. Then the closure check runs: `trace.py --strict-integrity`,
`check_trajectory.py --strict`, and ruling 6's `trace.py --strict` with no
finding beyond LLR-292's. One combined sitting judges every amendment, and
the amendment act is the lane's last spine commit.

- Done when: the accepted verdict covers each amended row, and the act is
  committed.
- Tests: adds none. It amends the TC rows above and runs their evidence.

### P13: the RESYNC entry (D4)

Target: one new `### ... [since <sha>]` entry after the last one in
`project-trajectory/RESYNC_PACK.md`.

- **What changed:** the review's convergence stance and `--stance`, the
  critique's registry list, severity by reachability and the
  classification, SUCCESSOR in the dispute grammar and in the rework gate
  (never at the plan cap), section 3's contract voice, and PROCESS.md §3's
  record-at-event rule.
- **Kit-owned files to overwrite:** `scripts/review_brief.py`,
  `scripts/kitlib/dispute.py`, `scripts/plan_coverage.py`,
  `prompts/reviewer.template.md`, `prompts/adjudicate-dispute.template.md`,
  `prompts/spine-questions.md` and `prompts/CATALOG.md` (regenerate), plus
  `docs/process.md` from PROCESS.md, in its §2 class.
- **What to do:** nothing is forced. No registry, setting, record format or
  template slot changes, so an override reviewer template still renders.
  Dispute verdicts written before still parse, and a reader of
  `kitlib.dispute.RULINGS` sees one more value.
- Anchored at the lane's trunk base in the lane. The landing re-anchors it
  at its parent (recipes §3).
- Done when: the entry lists those files and says no migration is forced.
- Runs: `tests/test_resync_pack.py` (the header grammar and the anchor
  resolve).

### P14: landing (D6, D7)

- **D6:** on trunk, `git log -1 --format=%h --
  docs/plans/2026-10-11-review-churn/baseline/baseline-manifest.md` prints
  a commit. Today that is `fa4bd0c49`, already an ancestor of this lane's
  base. Without it, the lane does not land.
- WI-911 changes the machinery the cycle runs on, so it lands alone (the
  rule P11 adds). A rebase that changes code or rows gets an uncounted
  convergence round.
- **D7,** on the landing tip:
  - the smoke tier, then `scripts/check_smoke_budget.py --mode enforce`,
    read quiet;
  - `check_trajectory.py --strict` clean;
  - `trace.py --strict` with no finding beyond LLR-292's (none, if B2 has
    landed first).
  - `max-tests` in `docs/stack.ini` is re-stamped only if the tier passes
    its 2600 ceiling.
- Then the coordinator regenerates the trunk views (`trunk_step.py
  --regen`), re-anchors P13's entry, and files a successor row for any
  accepted SUCCESSOR ruling.
- Tests: adds none.

## Exclusions

Excludes: TC-046 — agent-route resolution (LLR-044); no file in its evidence or under its row changes.
Excludes: TC-048; TC-085 — the loop's critique scheduling, rework and cap (LLR-048, LLR-082) run through agent_brief and the unchanged critique template; the attended critique brief this row changes is TC-333's.
Excludes: TC-083 — the review scorer's grammar is unchanged (deliverable 7 keeps the verdict grammar); P7's filing pin holds a convergence-tagged finding to it under TC-333.
Excludes: TC-084 — the loop's swap, tier-up and escalation branches (LLR-081) are untouched; its arms in tests/test_agent_loop_review.py run with P7's run of that module.
Excludes: TC-205; TC-257; TC-259 — the verdict record's identity, a REVIEW session's write scope and the merge gate's evidence (LLR-140, LLR-207, LLR-262) are untouched; TC-257's arms in tests/test_agent_loop_review.py run with P7's run of that module.
Excludes: TC-331 — the in-lane act and approval rung (LLR-158 and its siblings) is untouched.

## Commits and the bar

- Each build commit passes the commit bar: `python -m pytest -q -n auto -m
  smoke` and `python scripts/check_smoke_budget.py --mode enforce`, plus
  ruling 6's `trace.py --strict` and `check_trajectory.py --strict` after
  the round.
- P6(a)'s pin commits first, then the move alone, before P6(b) and (c).
- Each prompt edit (P5, P7, P8) carries its regenerated `prompts/CATALOG.md`,
  because `test_the_catalogue_on_disk_is_FRESH` is smoke-tier.
- Each skill edit (P9, P11) carries its synced copies.
- New smoke cases stay in-process, except those that join a smoke module's
  existing fixture: P4's coverage cases run the gate as a subprocess, as
  their module does, and P3's entry-point case uses the lane worktree its
  three dispute siblings use, since the entry point refuses a primary
  checkout. Every other git-backed case goes to a slow module.
- Red-before evidence: on a scratch worktree at the pass-record commit,
  copy in only the new and changed test files and run them. Each named
  red-before test fails, for the reason given above. The summary lines go to
  the build report, where the coordinator's convergence map can cite them.

## Outside this row

These are surfaced here, not changed by this row.

- PROCESS.md §6 says a review, critique or adjudication session does not
  fan out, while revision 37 lets this program's reviewers spawn bounded
  sub-agents. P11 states the ruling for this repository's cycle without
  restating §6. Reconciling §6 is not in this row's Done-when, so it is for
  the coordinator to put to the owner.
- `review_brief._ruled_findings` and `plan_gate._dismissals` each read the
  dispute verdict at the plan cap (WI-913). They are unchanged here; P4
  keeps the first's call compatible.
- P4 adds a keyword, defaulting to today's set, to `ruling_problem`, the
  in-process seam `review_brief` crosses from CMP-008 into CMP-006 with no
  interface row of its own. Its call is unchanged. Declaring that seam is
  item 11's work (interfaces as the measured boundary), not this row's.
- IF-113's data cell lists five of the nine adjudication templates the
  composer loads, without ADJUDICATE-CONSOLIDATE, ADJUDICATE-DISPUTE,
  ADJUDICATE-FIRST-APPROVAL and ADJUDICATE-REJUDGE. P5 edits the dispute
  template's text across that seam without changing the seam. The gap
  predates this row and spans templates it does not touch, so it is not
  amended here.
