+++
id = "WI-943"
title = "The merge slot authorizes a MEANING re-attestation only for a row its verdict marks blessed, through the one reader the act derivation also reads"
workstream = "process"
sr_refs = ["SR-232", "SR-178"]
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "single"
needs = ["~WI-929", "~WI-942"]
+++

## Deliverable

Closed in its lane on 2026-10-18, after its gate and act:

- The merge slot authorizes a MEANING re-attestation only for a row its
  accepted amendment verdict marks `[MEANING+BLESS]` alone. A plain
  `[MEANING]` row, or one tagged both ways, is refused, through the backing
  check and through a named verdict alike, and a combined act carrying one
  such row is refused whole. The refusal names the row as authorized by no
  accepted verdict; only a refused amendment row carries the remedy to re-sit
  it for the mark. A held rung still re-attests only a CLARITY row.
- One reader, `kitlib/sitting.judged_rows`, serves both the slot and the act
  brief's derivation in `adjudicate_act.py`, so an act lists exactly the rows
  the slot admits. `PROCESS_OPTIONS.md` and the coordinator recipes state the
  clause.
- Spine: LLR-278, LLR-310, LLR-338 and TC-278 amended and re-attested
  (sitting 003-ADJUDICATE-f01e04c, all MEANING+BLESS); TC-278's and TC-368's
  evidence extended (traced). `RESYNC_PACK.md` carries the entry, anchored at
  the landing's parent.
- Reviews: counted round 1 (001-REVIEW-A CHANGES-REQUESTED 1 MINOR,
  002-REVIEW-B APPROVE 2 MINOR; the wording fixed before the checkpoint) and
  the gate in convergence stance (004-REVIEW-A APPROVE 0, 005-REVIEW-B
  APPROVE 2 MINOR, to status.md's follow-ups). Decisions:
  `docs/decisions/wi-943.toml` D-001 to D-008.

## Context

Filed on trunk from WI-912's lane (wi-912 D-008; status.md's unfiled
follow-ups, "from the adjudication split's lane"). D-008 kept round 1's
002 F2 MINOR: "the bless mark is honoured only by the act session keeping to
its listed command, since the merge floor's judged_rows admits an unblessed
MEANING re-attestation". It named the merge floor as the owning boundary and
did not build the fix in WI-912, whose Trust section listed the floor
unchanged. It recorded the cost: "making the floor read the mark changes how
lanes in flight merge acts their verdicts took without marks". It declined
the reviewer's second remedy, a post-call check in the act command, as "a
second check where one boundary should own the rule". This row is the
reviewer's first remedy.

**The original rationale, read before drafting.** WI-841 (rounds 14 and 16)
made the merge admit an act only when an accepted verdict in the branch
judged its own rows, and WI-849 made that the actor test for every lane
(owner ruling 6, 2026-10-07). At the time a sitting judged and acted in one
turn. The pre-WI-912 composer's released-rung aftermath read "a CLARITY
verdict, and a MEANING verdict you would bless, is re-attested BY YOU, in
this session" (`adjudicate_brief._RELEASED_AFTERMATH` at `5604f0fd9^`). So a
MEANING ruling plus the act in the same turn was the blessing, and the
floor's `_AUTHORIZING` table reasonably counted MEANING and CLARITY alike. WI-912 split the act into a later turn. The blessing now
travels on the verdict as the `[MEANING+BLESS]` row tag (Q2 of
coordinator-2026-10-14 D-003). The floor's table was not updated, so a plain
`[MEANING]` ruling ("I would not bless it") still authorizes the act.

**The code path today, checked on trunk `cd6ba3160`.**
- The merge slot (`integrate.py integrate`): `integrate_one` →
  `_merge_refusal` → `_approval_act_refusal` →
  `acceptance_record.merge_approval_refusal`. That function calls
  `kitlib.sitting.unaccepted_refusal` for an act that names a verdict
  (`_named_line`) and `backed_act_refusal` → `kitlib.sitting.uncovered_refusal`
  for every acted row. Both read `kitlib.sitting.judged_rows`, which admits
  `(amendment, row)` for any ruling in `_AUTHORIZING["amendment"] =
  ("MEANING", "CLARITY")`.
- `kitlib.verdict.row_rulings` reads both `- [MEANING]` and
  `- [MEANING+BLESS]` as `MEANING`, by design, so every rulings reader is
  unchanged. `blessed_rows` is the mark's one reader. Its only caller is
  `adjudicate_act._authorized`, which passes `blessed` to `_arm`.
- So the rule "a MEANING row is re-attested only with the mark" has one
  home, the act derivation. The floor does not hold it.

**Probe** (`C:/Projects/ai-template.wt/review-tmp/2026-10-17e/drafts/probe/probe_floor.py`,
output `probe_floor.out`; trunk's own test helpers, the real snapshot
writer, a released rung). An Approved SR row is amended. An accepted
amendment verdict rules it plain `[MEANING]`, and the act
`intake.py snapshot --reattests` is taken by hand. The act derivation says
the verdict "owes no act: it authorizes none". The floor admits the act
(`None`), both for a lane scoped to that amendment and for an unscoped lane.
With the proposed reader patched in memory, the floor refuses the plain
`[MEANING]` act and admits the `[MEANING+BLESS]` one.

**Lanes in flight** (D-008's concern). The rule binds only acts a branch
adds over its merge base; acts already on trunk are never re-read. The
tracked claims on trunk are wi-798, wi-902, wi-915, wi-916 and wi-929.
- **wi-902** took acts 113 to 117 in-lane on 2026-10-11, under verdicts
  006, 007 and 013. Each rules its re-attested rows plain `[MEANING]`, with
  the blessing in prose. So under this rule its branch would not merge
  through the slot as it stands. The review-churn plan already settles those
  acts: WI-902 is reshaped first (the handoff's B4), and "the reshape
  decides those acts (re-judged or retired) before rebasing" (plan item 2,
  revision 34). A re-judged act comes from a re-sat verdict, which carries
  marks.
- **wi-798**'s verdict 004 (combined) rules ten MEANING rows plain
  `[MEANING]`, four of them "I would NOT bless", and returns every
  first-approval row. The lane took no act, and it owes its checkpoint
  rework. Its owed act is covered by recipes §3 "The act turn" item 5: "a
  verdict sat before it whose act is still owed carries no bless marks, so
  re-sit it".
- **wi-915, wi-916 and wi-929** hold no verdict.

So no open lane is affected beyond what is already planned. Downstream, an
adopter's loop lane whose sitting re-attested a MEANING row in-turn before
its WI-912 resync is refused at the slot after this one. Its remedy is to
re-sit those rows. The RESYNC entry says so (deliverable 5).

**The hand landing is outside the floor.** The coordinator lands a lane with
`git merge --squash` and the pre-commit hook (recipes §3). The hook's steps
(`check.py`: held-status, text-then-act, done-when-blessed, plan-gate,
ruling-sync) read no verdict's authorization. `merge_approval_refusal` runs
only in the merge slot, `integrate.py integrate`. So on this repository's
landing path this row changes nothing until WI-808 lands (the residue in
`## Trust`, Ruling).

**The anchor.** SR-232 (Approved): a combined adjudication "shall present
and validate one sitting that preserves each kind's own scope, evidence and
decision grammar". The amendment kind's grammar distinguishes `[MEANING]`
(would not bless) from `[MEANING+BLESS]` (would bless). A merge that reads
both as authority does not preserve that decision. LLR-310, which owns the
floor's authorization reader and the bless reader, hangs from SR-232.
LLR-278, the merge-time statement of the same rule, hangs from SR-178 and
SR-228. No SR changes: SR-228 already limits a held rung to CLARITY, and
this row narrows only the released-rung MEANING case. The need behind it is
SN-029: "releasing a tier means the review is delegated, never skipped".

## Deliverables

1. **The authorization reader holds the bless condition**
   (`project-trajectory/scripts/kitlib/sitting.py`). `judged_rows` admits an
   amendment part's MEANING row only when that part marks it
   `[MEANING+BLESS]`, read through `kitlib.verdict.blessed_rows` (the mark's
   one reader). It reads CLARITY and APPROVE rows as before. It joins
   `__all__`. Its two callers change with it and stay one reading:
   `uncovered_refusal` (every acted row) and `unaccepted_refusal` through
   `_named_line` (an act that names a verdict). Their lines say "authorized
   by no accepted verdict" and "(does not authorize ...)". The remedy gains
   one sentence: an amendment's MEANING row authorizes a re-attestation only
   when its verdict marks it `[MEANING+BLESS]`, so re-sit the row.
   `acceptance_record.held_reattest_refusal` is unchanged: on a held rung
   only CLARITY re-attests.
2. **The act derivation reads the same reader**
   (`project-trajectory/scripts/adjudicate_act.py`). `_authorized` takes the
   rows `judged_rows` returns. `_arm` loses its `blessed` argument and keeps
   only the held-rung policy (`intake.adjudication_action`). The bless
   condition thus moves from the derivation into the shared reader, in the
   same commit as deliverable 1. Neither lands alone: deliverable 2 first
   would list unblessed MEANING rows, and deliverable 1 alone leaves the
   condition in two homes (PROCESS.md §3, "Consolidate, don't duplicate").
   The derivation's output is unchanged.
3. **Contract and doc text.**
   - IF-287's contract sentence in `kitlib/sitting.py` names `judged_rows`
     as the one reader of what an accepted verdict authorizes an act on: an
     APPROVE row, a CLARITY row, and a MEANING row only with its bless mark.
     The merge's backing checks and the act assembler both read it.
     `docs/interface-reference.md` is regenerated.
   - `project-trajectory/PROCESS_OPTIONS.md`, "Who performs the approval
     act", "How it is held" item 1: after "that judged that act's own rows",
     add "(a meaning row's re-attestation only by a verdict that blesses
     it)". The file is byte-watched: report the delta with
     `byte-budget-guard`.
   - The `coordinator-cycle` skill, `references/recipes.md` §3 "The act
     turn" item 5 gains: an act a lane already took from such a verdict on a
     MEANING row is not authorized either, so re-sit the row before the
     landing. The kit source is `project-trajectory/skills/coordinator-cycle/`,
     and its copies in `.claude/skills/` and `.agents/skills/` stay
     byte-identical (`bootstrap.py --dest . --sync`).
4. **Spine rows** (Terra authors; judged at the lane's checkpoint sitting).
   The quoted text is trunk's. LLR-310's is read as WI-929 leaves it.
   - **LLR-310** (Approved), **amended**:
     - "every row it re-attests needs a MEANING or CLARITY ruling in an
       accepted amendment part among the branch's own bindings" becomes
       "every row it re-attests needs a CLARITY ruling, or a MEANING ruling
       carrying the bless mark, in an accepted amendment part among the
       branch's own bindings".
     - "a named verdict must judge each row its act re-attests" becomes "a
       named verdict must authorize each row its act re-attests in the same
       way".
     - The last sentence gains: "One reader of the rows an accepted verdict
       authorizes, a MEANING row only when so marked, serves both the merge
       and the act assembler."
   - **LLR-278** (Approved), **amended**:
     - "any row it re-attests lacks a MEANING or CLARITY ruling in an
       accepted amendment part among the branch's bindings" becomes "any row
       it re-attests lacks a CLARITY ruling, or a MEANING ruling carrying the
       bless mark, in an accepted amendment part among the branch's
       bindings".
     - "a named verdict must also judge every row its act re-attests"
       becomes "a named verdict must also authorize every row its act
       re-attests in the same way".
   - **LLR-338** (Approved), **amended**, the last sentence. "Each row's act
     is read from the one held-rung act policy that also informs the judging
     brief; the bless mark is the added condition for a released-rung
     MEANING row" becomes "Which rows a verdict authorizes, a MEANING row
     only with its bless mark, is read from the one reader the merge's
     backing check also reads, and each authorized row's act from the one
     held-rung act policy that also informs the judging brief". The sitting
     may rule it CLARITY.
   - **TC-278** (Approved), **amended**:
     - Method: "every row it re-attests MEANING or CLARITY" becomes "every
       row it re-attests CLARITY, or MEANING with the bless mark". It gains:
       "On a RELEASED rung, an act re-attesting a row that its accepted
       amendment verdict rules plain MEANING, or tags MEANING+BLESS and
       another way, is refused naming the row, through the backing check
       and through a named verdict alike. A combined act carrying one is
       refused whole. The same act under a MEANING+BLESS ruling merges."
     - Expected: "its re-attested rows MEANING- or CLARITY-ruled by accepted
       branch bindings" becomes "its re-attested rows CLARITY-ruled, or
       MEANING-ruled with the bless mark, by accepted branch bindings".
     - Evidence: the new tests.
   - **Unchanged:** SR-232, SR-178, SR-228, SR-231, LLR-158 ("an accepted
     verdict that judges its own rows" stays true at that level), TC-331,
     TC-153. TC-368 is unchanged in text. Its evidence cell is traced upkeep
     if the arm test is renamed.
5. **`RESYNC_PACK.md` entry**, anchored at the landing's parent. The kit-owned
   files are `scripts/kitlib/sitting.py`, `scripts/adjudicate_act.py` and
   `PROCESS_OPTIONS.md`. The entry says the merge slot now refuses a MEANING
   re-attestation whose verdict does not mark the row `[MEANING+BLESS]`.
   A loop lane in flight whose sitting re-attested such a row in-turn,
   before the adopter's WI-912 resync, is refused at the slot until those
   rows are re-sat. Nothing migrates, and no setting changes.

## Trust

A verdict file already holds authority over the merge gate's admission of an
act (owner ruling 6; WI-841; WI-912's Trust section). This row moves one
part of that authority: on a released rung, an amendment verdict now
authorizes a MEANING re-attestation only through its bless mark. Written
before the claim, under
[`PROCESS.md` §3, "When a guard is owed"](../../../../project-trajectory/PROCESS.md#3-traceability--anti-duplication).

- **Producer.** The judging turn writes the input: an adjudicator session
  launched from the lane by `coordinator_adjudicate.py adjudicate`, or by the
  loop's session body. Before launch, the entry point reserves the verdict
  path and writes the binding (`kitlib.sitting.write_binding`, outcome
  `pending`). The session writes the verdict, including each amendment row's
  tag, in the brief's grammar (`prompts/adjudicate-amendment.template.md`:
  `[MEANING|MEANING+BLESS|CLARITY]`), and commits it. Then
  `adjudicate_brief.record_outcome` validates it against the bound kinds and
  records `accepted` or `failed`. The verdict is model output, a trust
  boundary that the one parser (`kitlib.sitting.parse`) and the one row
  reader (`kitlib.verdict.row_rulings`, `blessed_rows`) validate. A failed
  write looks like one of these:
  - a binding `pending` or `failed`;
  - a verdict outside the grammar;
  - a verdict or binding left uncommitted, which is absent at the head;
  - a mark the session omitted, misspelt or doubled. That one is not a
    failed file: it is a row that authorizes nothing.
- **Consumers** (grep over `project-trajectory/scripts` for `judged_rows`,
  `blessed_rows`, `accepted_at`, `row_rulings` and `verdict_rulings`):
  - `kitlib/sitting.py`: `judged_rows`, read by `_named_line` →
    `unaccepted_refusal`, and by `uncovered_refusal`.
  - `acceptance_record.py`: `merge_approval_refusal` calls
    `unaccepted_refusal`, and `backed_act_refusal` calls
    `uncovered_refusal`. `_held_act_lines` reads the parsed rulings
    directly, CLARITY only, so the mark does not reach it (a blessed MEANING
    row still reads MEANING and is refused on a held rung).
  - `integrate.py`: `_approval_act_refusal` → `_merge_refusal` →
    `integrate_one`, the merge slot.
  - `adjudicate_act.py`: `_authorized` (today it reads `blessed_rows`;
    after this row, `judged_rows`) → `_derive` → `owed_acts`, `left_owed`,
    `act_values`, `compose_act`, consumed by `coordinator_adjudicate.py act`.
  - `kitlib/done_when.py`: reads `accepted_at` for the Done-when kind only,
    never an amendment row. Unaffected.
  - **Not a consumer: the hand landing.** The pre-commit hook's steps on a
    `git merge --squash` landing read no verdict's authorization, so an act
    on that path is admitted whatever its verdict says (residue below).
- **Ruling.** Every consumer reads the verdict through `accepted_at` and the
  rows through `judged_rows`. A verdict or binding that is absent at the
  branch head, unreadable (`git_out` returns None), `pending`, `failed` or
  malformed is not accepted. It authorizes nothing, and every row an act
  takes under it is refused by name. A row line the reader does not match
  authorizes nothing: an absent mark (`- [MEANING]`), a misspelt one
  (`- [MEANING + BLESS]` matches no tag) or a row tagged two ways. The
  merge refuses the act naming the row, and the derivation lists no act for
  it. The authority binds to the verdict and binding as committed at the
  branch head, among the bindings the branch changed since its merge base
  (`branch_verdicts`). On a held rung it also binds to SR-228's CLARITY-only
  rule, unchanged. The binding records no digest of the verdict text, so a
  committed verdict edited after its outcome was recorded is read as the
  verdict. That is WI-912's stated bound, unchanged here. **No consumer
  fails open on the slot.** **Residue**
  (docs/decisions/coordinator-2026-10-17.toml#D-009): the coordinator's
  squash landing runs no approval-act reader until WI-808 lands. WI-808
  moves those landings onto the operation the loop uses, which runs
  `merge_approval_refusal`; this row corrects the rule that path will
  enforce.

## Done-when

Each new test fails on the code before the change; the pins pass before and
after.
- **A plain MEANING re-attestation is refused at the merge.** On a released
  rung, an act re-attesting an Approved row whose accepted amendment verdict
  rules it `[MEANING]` is refused, naming the row, with the remedy naming
  the bless mark. That holds for a lane scoped to that amendment and for an
  unscoped lane. It fails before: the probe shows both admitted.
- **A row tagged two ways is refused.** It is tagged `[MEANING+BLESS]` and
  `[CLARITY]`, or `[MEANING+BLESS]` and `[MEANING]`. It fails before: the
  row reads MEANING, which authorizes.
- **A combined act is refused whole.** It carries a plain-MEANING
  re-attestation beside a backed first approval. It fails before.
- **A named verdict is refused the same way.** The act names a verdict
  (`--verdict`) on a released rung that rules the row plain MEANING, and it
  is refused through the named-verdict check, naming the verdict. It fails
  before.
- **Pins.** The same act under a `[MEANING+BLESS]` ruling merges. A held
  rung's existing tests (`test_a_held_rung_*` in
  `tests/test_snapshot_readers.py`) pass unchanged.
- **One home for the condition.** `blessed_rows` is called only from
  `kitlib/sitting.py` (`grep -rn blessed_rows project-trajectory/scripts`
  names only `kitlib/verdict.py` and `kitlib/sitting.py`), and `_arm` takes
  no bless argument. It fails before: `adjudicate_act.py` calls it.
  `tests/test_adjudicate_act.py`'s bless and derivation tests pass with
  their expectations unchanged. The arm test's "with and without the bless
  mark" half moves to a verdict-text case through `_authorized`.
- **The text.** IF-287's sentence is in place, and
  `docs/interface-reference.md` is regenerated. The `PROCESS_OPTIONS.md`
  clause is in, with `byte-budget-guard`'s delta reported. The recipes
  item is in, and the skill copies are byte-identical.
- **The spine.** LLR-310, LLR-278, LLR-338 and TC-278 carry the amended
  text, judged at the lane's checkpoint sitting. TC-278's evidence names
  the new tests.
- **`RESYNC_PACK.md`** carries the entry.
- **On the landing tip**, the commit bar is green (smoke tier and budget
  enforce), and `check_trajectory.py --strict` and `trace.py --strict` are
  clean.

## Scope answers

- **S1.** One landable unit. Deliverables 1 and 2 move one condition and
  land in one commit (deliverable 2). The text, spine and RESYNC entry
  describe that change and ride with it. The lone-retirement row
  (WI-942) is separate: it reads a different input, it carries a deadline,
  and either lands alone. Both amend LLR-278, TC-278 and the recipes'
  act-turn paragraph, so WI-942 lands first.
- **S2.** Yes: the verdict's bless mark gains authority over what the merge
  gate admits. See `## Trust`.
- **S3.** Closed, deny by default. The input is a verdict's row lines,
  model output in an unbounded grammar. An act on a row is authorized only
  by an exact authorizing line in an accepted part of the right kind:
  - first approval: `- [APPROVE] <id>`;
  - amendment: `- [CLARITY] <id>`, or `- [MEANING+BLESS] <id>` with no
    other tag for that row.

  Every other line authorizes nothing: `- [MEANING]`, `- [RETURN]`, an
  unmatched tag, a row tagged two ways, a Done-when part and every other
  brief class. On a held rung only CLARITY re-attests (SR-228, unchanged).
  The bound covers verdicts that the kit's adjudicator routes write and
  `record_outcome` records accepted. A committed verdict edited after its
  outcome was recorded is outside it (PROCESS.md §6; WI-912's bound). The
  rule binds landings through the merge slot. The coordinator's squash
  landing runs no approval-act reader until WI-808 lands (the residue in
  `## Trust`, Ruling).
- **S4.** `single`. The row has a Trust section. It touches two script
  families: the merge readers (`kitlib/sitting.py` under
  `acceptance_record.py`) and the act assembler (`adjudicate_act.py`). It
  crosses two seams (IF-287, IF-296) and promises behaviour over an input
  space (verdict row lines).
- **S5, architectural delta,** within scope:
  - No new state.
  - The merge's authorizing domain narrows: an amendment MEANING row
    authorizes only with its mark.
  - The merge's output gains an input it did not read, the mark, which is
    already in the verdict.
  - The bless condition moves to one home that both readers use.

  No component or boundary changes, and no refactor row is owed. **Found,
  not fixed:** the held-rung policy has two homes. The derivation reads
  `intake.adjudication_action`, while the floor states CLARITY-only in
  `acceptance_record.held_reattest_refusal`. That is for the coordinator to
  file or leave. This row does not need it.
- **S6.** Two soft edges; nothing third-party.
  - `~WI-929`: it edits `kitlib/sitting.py` (the reader and IF-287's
    contract paragraph) and amends LLR-310. It is first in the queue, so
    this row follows it and avoids a cross-lane edit of one row and one
    paragraph.
  - `~WI-942`: the lone-retirement row filed beside this one. Both amend
    LLR-278 and TC-278 and the same recipes paragraph, and WI-942 carries
    the deadline.

  Later rows, not edges:
  - WI-851 retires LLR-278's held clause.
  - WI-809 builds the loop's act turn on `adjudicate_act`.
  - WI-801 carries `coordinator_adjudicate.py act` into `ask`.
  - WI-902's reshape re-judges or retires its acts 113 to 117, which plain
    MEANING verdicts back (Context).
- **B1.** The probe and the lanes-in-flight reading are evidence. The
  hand-landing gap is WI-808's, stated as residue, not hidden work.
- **B2.** No split is minted on a work branch. WI-942 is filed on
  trunk beside this one.
- **B3.** The merge reads the decision the sitting recorded in its own
  commit (the mark on the verdict) and re-derives nothing. The derivation
  reads the same record through the same reader.
- **B4.** No Done-when item needs an owner act or a credential. The
  amended rows sit on rungs this repository's dial releases. WI-912's own
  act turn re-attested LLR-310 (act 126) and approved LLR-338 and TC-368
  (act 127).

## Calls ruled at filing

- **The hand-landing gap** (owner, docs/decisions/coordinator-2026-10-17.toml#D-009):
  WI-808 owns it, and no hook-step row is filed. It is stated once, as
  residue in `## Trust`, Ruling.
- **No grandfathering** (owner, docs/decisions/coordinator-2026-10-17.toml#D-010):
  an unmarked MEANING ruling authorizes no act, whenever it was sat. Lanes
  in flight re-sit: WI-902 by its reshape, WI-798 by recipes §3 item 5.

## Critique dispositions

Round 1 (Codex Sol, medium, 2026-10-17): APPROVE, no findings.
