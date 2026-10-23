+++
id = "WI-850"
title = "A spine row is approved only after the rows it hangs from are"
workstream = "process"
sr_refs = ["SR-178"]
specref = ""
needs = ["WI-892"]
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "single"
+++

## Deliverable

Landed by headless leg 15 of loop session `20261021T045653Z-213020`, squashed from lane `wi-850`.

- **SR-224's chain, first in its own act.** SR-224 was re-sat twice (a perspective record, and one `shall` governing both the shipped descriptions' floor and the named failure) and approved at sitting 003, act seq 154, so LLR-281 and TC-291 no longer stand approved under a Drafted parent.
- **The rule.** `kitlib.spine` holds the parent-first rule (`parent_first_findings`, `parent_first_line`) and the one approval predicate (`claims_approval`, Approved or Founded in any letter case), which `acceptance_record` and `adjudicate_act` now bind. Its edges are an SR's SN parents, an LLR's SR parents and a TC's SR and LLR parents; IF, B, DA, undeclared and `-000` references are not judged.
- **The standing finding.** `trace.py`'s integrity sweep reports each standing case as a `parent-first:` integrity finding naming the child, the parent and both statuses with its remedy, so `--strict-integrity` and `registry-integrity` fail on it; the WI-129 LLR-status advisory is retired.
- **The commit refusal.** `acceptance_record`'s commit judgement (IF-308) refuses a staged tree or lane commit that moves a status into such a case, prefixed `the index:` or `commit <sha10>:`, reading every registry carrier through WI-963's two-tree reader (`_tier_reads`, carried here as its own commit), refusing what it cannot read on the commit side and counting every status as moved when a comparison side cannot be read. It runs as `check.py`'s `parent-first` step at pre-commit and as the third lane-commit rider at the merge slot.
- **Rows and text.** SR-245 (the standing finding) and SR-246 (commit admission), labelled derived, with LLR-357, LLR-358, TC-396, TC-397 and IF-308, approved in one combined sitting (006), act seq 155; the spine-authoring skill names the check as the parent-first rule's enforcer; a RESYNC entry names the two remedies for an adopter's standing case.

## Context

Re-homed 2026-10-10 (D-015): the shared lane-commit walk this row rides
moved from WI-828 (closed partial) to WI-892, which landed the same day.
OI-113 was ruled (d), won't fix, on 2026-10-14, and WI-893 was cancelled: no
hook walks a hand merge, and the merge slot is the sanctioned landing path.

Filed by hand on 2026-10-07 from the WI-841 retrospective (proposal §7.2,
row P3), carrying the owner's ruling 4 of 2026-10-07
(`docs/log.d/2026-10-07-wi841-retro-owner-rulings.md`): a child is approved
only after its parent. The owner expected the check to exist. It does not:
LLR-281 and TC-291 have been Approved under SR-224, which is still `Drafted`,
since WI-615 (2026-09-28), and neither `trace.py --strict-integrity` nor a plain
`trace.py` run mentions it.

SR-224 sits on a released rung here (the dial is `DevStg-Boundary`), so an
adjudication sitting can settle its chain before the check lands.

## Trust

Done-when's commit refusal and standing finding give two cells of the four
spine registries authority over a commit and over a lane's landing: each
row's `status`, and its parent references (`sn_refs` on an SR, `sr_refs` on
an LLR, `verifies` on a TC; `SN-Refs`, `SR-Refs` and `Verifies` as the
readers name them). The carriers are `docs/requirements/stakeholder-needs.toml`
(its `need` tier), `docs/requirements/system-requirements.toml`,
`docs/requirements/low-level-requirements.toml` and
`docs/test/test-cases.toml`, with their legacy forms (`.md` needs, `.csv`
rows), which the same readers resolve. They are hand-edited files on disk, so
the guard is owed under
[PROCESS.md §3, "When a guard is owed"](../../../../project-trajectory/PROCESS.md#3-traceability--anti-duplication).

- **Producer:**
  - *Authoring:* rows are written `Drafted`, as file edits, by Terra's
    authoring turns, by builder and coordinator sessions and by the owner.
    `retire.py` deletes a row and writes its record; `migrate_carrier.py`
    rewrites a whole registry once, at a carrier cutover; `bootstrap.py`
    scaffolds the `-000` example rows.
  - *The approval act:* the act turn (an adjudicator turn whose brief
    `adjudicate_act.py` composes, run through `coordinator_adjudicate.py
    act`) or the owner edits `status` cells to `Approved` or `Founded` by
    hand, then runs `intake.py snapshot`. That writes only the copy and the
    ledger under `docs/archive/last_approved/` (`baseline_snapshot.py`),
    never a live status cell: the scripted flip is retired (OI-45).
  - *A demotion:* a hand edit of `status` back to `Drafted`. It writes no
    copy, since a de-approval is not an act.
  - Failed-write shapes:
    - *A malformed file:* a TOML decode error, an explicit empty string, an
      unquoted dotted table header, or one stem under both carriers.
    - *A malformed cell:* a row with no `status`, or a word outside
      `Drafted`, `Approved` and `Founded`; the integrity floor's missing-cell
      and closed-vocabulary findings already name both. A stray non-UTF-8
      byte is decoded with replacement by every reader.
    - *A partial act:* some of an act's flips saved and not others, a child
      flipped without its parent, or a parent demoted under approved
      children. The last two are what this row refuses; a flip without its
      copy, or the reverse, is the snapshot mirror's finding
      (`acceptance_record.staged_snapshot_findings`).
    - *A truncated file* (a writer killed mid-write): a decode error in
      nearly every case, so a malformed file.
    - *An unstaged edit:* on disk but not in the index. The commit judgement
      reads the index; the standing finding reads the disk.

- **Consumers** (grep over `project-trajectory/scripts` and
  `project-trajectory/hooks`):
  - *The rule's one home:* a pure function in
    `project-trajectory/scripts/kitlib/spine.py`, beside `is_approved`,
    `is_founded`, `refs` and `missing_cell_findings`. Given the four tiers'
    rows, it returns one entry per approved child (`Approved` or `Founded`)
    citing a parent row that exists and is not approved, naming the child,
    the parent and both statuses. Its edges are an SR's `SN-Refs` to SNs, an
    LLR's `SR-Refs` to SRs, and a TC's `Verifies` to SRs and LLRs. Its
    approval test is the pair `acceptance_record._claims_approval` names
    today: the pair moves into `kitlib.spine` with the rule and
    `_claims_approval` binds it, so the rule and the approval-act readers
    agree on what counts as approved. Not `coherence.py`, whose only caller
    is `trace.analyze` by its own statement, and not `spine_rules.py`, whose
    callers are the stage derivation's.
  - *The commit judgement's one home:*
    `project-trajectory/scripts/acceptance_record.py`, beside
    `APPROVAL_ACT_CSVS`, `_commit_parents` and the two-tree readers: one
    function judging a tree (the index, or a commit) against its parents. It
    calls the rule on the tree and keeps each entry whose child or parent
    status moved against a parent. It has a staged form (the index against
    HEAD, and against MERGE_HEAD during a merge) and a per-commit rider
    form.
  - *Callers that only call:*
    - `project-trajectory/scripts/trace.py` `integrity_sweep`: the standing
      finding, in `findings.integrity`, so `--strict-integrity` and
      `--strict` exit 1 on it. `check.py`'s `registry-integrity` step runs it
      at pre-commit, at every bar, in CI and in the merge slot's bar
      (`integrate._run_bar`); `traceability` runs `--strict`.
    - `project-trajectory/scripts/text_then_act.py`: the rider joins
      `LANE_COMMIT_RIDERS`; `lane_commit_walk` is unchanged.
    - `project-trajectory/scripts/integrate.py`: `_text_then_act_refusal`,
      through `_each_lane_commit`, already walks every rider at the merge
      slot. The rider's lines carry their own remedy, as the adoption
      record's do, so the slot's code does not change.
    - `project-trajectory/scripts/check.py`: one new step, a mode in
      `_text_then_act_mode`'s shape at `STAGE_NEEDS`, named in
      `BUILTIN_STEP_NAMES` and kept out of `_TRUNK_FRESHNESS_STEPS`, calling
      the staged form.
    - `project-trajectory/hooks/pre-commit`: the step joins the batched
      `--run-steps` list.
    - `project-trajectory/scripts/trace.py` `llr_status_advisories` (WI-129)
      retires in the same change. Each case it warns of, an unapproved LLR
      whose every citing TC is `Approved`, is now an integrity finding on the
      TC-to-LLR edge.
  - *Readers checked and unchanged:* `spine_carrier.py`, which supplies the
    reads and the contract below; `spine_rules.py` and `derive_stage.py`,
    where a `Drafted` parent already holds its rung open; `census.py`, whose
    `gap_census` reads orphans and status findings, so the new finding mints
    no gap row; `adjudicate_act.py` and `coordinator_adjudicate.py`, whose act
    commit meets the refusal at the hook and the slot; `plan_gate.py`, which
    walks lane commits with its own judge.

- **Ruling** (drafted for the owner to confirm or overrule):
  - *What the commit judgement binds to:* one commit's tree and its parents'
    trees. At pre-commit that is the index against HEAD (and MERGE_HEAD); at
    the slot, each lane commit against its own parents. Never the working
    tree, and no history past the parents. It reads the status cells and the
    parent references only: a parent whose approved text has drifted from
    its copy still reads approved here, and that drift stays the
    re-attestation's. A row's status moved when it differs from a parent's,
    an absent row counting as a value; in a merge, from any parent's, so a
    violation a merge assembles from two sides is the merge's own. A commit
    whose name list (read `--no-renames`) touches no carrier of the four
    registries moved no status and is not read further. A squash landing is
    judged like any commit: the rule asks what the tree leaves, not who wrote
    it, so it needs no squash path.
  - *The standing finding* reads through `spine_carrier.load` and
    `load_needs` under their existing contract (IF-102): an absent registry
    is no rows; one that exists and does not parse, carries an explicit
    empty string or an unquoted dotted id, or exists under both carriers,
    raises SystemExit naming the file. `--strict-integrity` then exits 1 and
    `registry-integrity` fails. This is fail-closed already and needs no new
    code.
  - *The rule:* a row with no status, or with a word outside the vocabulary,
    is not approved, so an approved child under it is a finding (and the
    cell has its own integrity finding). A parent id no row declares is not
    judged: the orphan rules' `references unknown` finding (`coherence.py`)
    owns it, as IF-141 already says of unresolved parentage. A cited id
    outside the four tiers (an IF, B or DA row) is not a parent.
  - *The commit judgement* reads each registry at a tree through
    `kitlib.git.git_show` (None when the tree does not list the path; it
    raises `UnreadableBlob` when the tree lists it and git cannot read it)
    and `spine_carrier.tier_rows_from_text` (None, never `{}`, for TOML that
    does not parse). It does not read through
    `acceptance_record._spine_rows_at`, which takes both failures for an
    absent registry.
    - Absent on the commit side: no rows, and its edges are the orphan
      rules'. Absent on a parent side (the commit adds the registry): every
      row in it counts as moved.
    - Listed but unreadable, or not parsing, on the commit side: a refusal
      line naming the registry and the tree, since whether the commit leaves
      an approved row under an unapproved parent is unknown.
    - The same on a parent side: every status on the commit side counts as
      moved, so the commit's tree is judged in full. A commit that repairs a
      broken registry is judged on its own rows, and is never refused for
      its parent's state.
    - A diff git cannot produce: a refusal line, never a skip, as text then
      act rules. A commit or parent git cannot read: `_commit_parents`'
      line. A range the slot cannot list: `_each_lane_commit`'s refusal.
    - No HEAD yet (the first commit): nothing is judged, as text then act
      rules; the standing finding reads that tree. Off git or outside a work
      tree: there is no commit to judge, as for every staged step.
  - *The step* exits 1 printing the refusal, else 0. A crashed step exits
    nonzero, which the step runner reads as FAIL, never SKIP; the slot's bar
    refuses a SKIP.

- **The bound**
  ([PROCESS.md §6, "Review threat model"](../../../../project-trajectory/PROCESS.md#6-review-depth-triage-efficiency)):
  the promise reaches what supported workflows and the kit's own routes
  write into the four registries, a hand edit of an authored row included,
  since rows are authored by hand; hand-edited kit-written state (the
  approval record under `docs/archive/last_approved/`, a generated view), a
  hand-chosen name alias (`sr-224` cited for `SR-224`) and a sub-second
  timing window (a writer killed mid-write, a file rewritten between a
  reader's two reads of it) lie outside it.

- **The parent set, and the one reader** (coordinator-2026-10-22 D-002, for
  the owner to confirm or overrule): a TC's parents are the SRs and LLRs its
  `verifies` cites. An IF row it cites carries no approval status (an
  interface is approved through the sitting of the row it serves; OI-112's
  ruling, review-churn plan revision 35), so it is no parent: counting IF
  rows would make 114 approved TCs here standing findings, demotion their
  only remedy. The standing finding stays an integrity finding, as Done-when
  states, and Done-when's first act clears the only standing case here
  (LLR-281 and TC-291 under SR-224). The commit judgement's two-tree read
  keeps "cannot be read" and "does not parse" apart; WI-963's held lane adds
  that reader (`acceptance_record._tier_reads`), so whichever row lands
  first carries it as its own behaviour-preserving commit and the other
  rebases onto it. The plan settles the rest of the draft's open points (the
  in-lane skill line on a parent "approved for its current text", which this
  check reads by status only; retiring `trace.llr_status_advisories`).

## Done-when

- First, in its own act: SR-224's chain is settled. Either SR-224 is
  adjudicated for first approval, or LLR-281 and TC-291 return to `Drafted`.
- A commit that leaves an approved row (`Approved` or `Founded`) under a parent
  that is not approved is refused, where the commit moved either row's status.
  An SR waits for every SN it cites, an LLR for every SR, and a TC for every
  SR and LLR it verifies. It is refused at pre-commit and on each lane commit through
  the shared lane-commit walk (WI-892).
- `trace.py --strict-integrity` reports any standing case as an integrity
  finding, naming the child, the parent and both statuses.
- `spine-authoring`'s parent-first rule (WI-848) names this check as its
  enforcer.
- Its rows (SR-178's chain, or a labelled derived SR if no approved row demands
  the rule) are authored as one change set and judged in one combined sitting.
- Tests: each tier pair; `Founded` counts as approved; demoting a parent under
  an approved child is refused; the standing finding.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit. An adopter with an approved
  child under an unapproved parent sees the new integrity finding at upgrade,
  and the entry names the two remedies.

## Critique dispositions

Scope critique (Codex, 2026-10-22; CHANGES-REQUESTED, findings=3):

- **MAJOR, S2 (Done-when gives on-disk registry cells gate authority with no
  Trust section): adopted.** `## Trust` now names the carriers and each
  producer route with its failed-write shapes, the consumers by path with
  "The rule's one home: a pure function in
  `project-trajectory/scripts/kitlib/spine.py`" and "The commit judgement's
  one home: `project-trajectory/scripts/acceptance_record.py`", and a ruling
  per consumer, among them "Listed but unreadable, or not parsing, on the
  commit side: a refusal line naming the registry and the tree" and "A diff
  git cannot produce: a refusal line, never a skip".
- **MAJOR, S4 (no `planmode` while the row changes trace enforcement and
  commit and lane admission): adopted.** The frontmatter carries
  `planmode = "single"`.
- **MINOR, S3 (no explicit supported-workflow bound): adopted.** `## Trust`
  ends with the bound: "the promise reaches what supported workflows and the
  kit's own routes write into the four registries, a hand edit of an
  authored row included, since rows are authored by hand; hand-edited
  kit-written state (...), a hand-chosen name alias (...) and a sub-second
  timing window (...) lie outside it."
