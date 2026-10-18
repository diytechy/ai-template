# WI-912 implementation plan: the sitting ends at its verdict; the act is a later turn

Spec: `docs/work/active/wi-912/WI-912-verdict-act-split.md` (the spec of record
is `docs/plans/2026-10-11-review-churn/README.md` §16, revisions 31, 32 and 36;
where this plan and a ruling differ, the ruling governs). Read for this plan:
the spec in full; plan §16; `coordinator_adjudicate.py`; `adjudicate_brief.py`
(the first-approval, amendment and aftermath arms, `governing_templates`,
`record_outcome`); `kitlib/sitting.py` (`accepted`, `accepted_at`,
`judged_rows`, `uncovered_refusal`, `unaccepted_refusal`); `kitlib/verdict.py`
(`ROW_RULINGS`, `row_rulings`); `intake.adjudication_action`;
`session_service.AdjudicationRequest` / `adjudication_keep`;
`agent_brief.loop_provenance_note`; the three sitting templates; SR-231,
SR-146, SR-232 and SR-209; LLR-306, LLR-167 and LLR-310; IF-283/284/285 and
their neighbours; the TCs below. WI-913, the plan gate, landed at
`b803dd019`; WI-911 landed at `247dc36c4`. Both soft edges are met.

## The architectural-delta answer

Yes, and within scope. The WI adds:

- **A state:** a lane holding an accepted verdict whose act is not yet taken.
  Today the judgement and the act share one turn, so that state is never
  observed between turns.
- **Values in domains:** `coordinator_adjudicate.py` gains the `act` command
  (IF-283's argument domain), its exits and readings (IF-284, IF-285); the
  shipped prompts gain `ADJUDICATE-ACT` (IF-113's key set); and the amendment
  verdict's row-line grammar gains the bless mark (IF-175's row rulings).
- **An output on a new input:** the act depends on a committed, accepted
  verdict and its binding read at HEAD across sessions, not on the same turn's
  judgement.
- **A new boundary:** the new assembler module `scripts/adjudicate_act.py`
  (CMP-008), whose call surface `coordinator_adjudicate` consumes. That is a
  new intra-component seam, proposed below with IF-115 as its nearest row.

No preparatory refactor is needed. The new module keeps `adjudicate_brief.py`
(932 of the ratchet's 1000 SLOC) shrinking, not growing, and every reader the
assembler needs already exists behind a declared seam (`accepted_at`,
`row_rulings`, `dial_at`, `rows_at`, `format_approves`, `prompts.fill`). Rows
P2 to P8 carry the change: the interface and domain edits as IF-row
amendments plus one proposed row, and the new module as its own LLR.

DELTA: within

## Design decisions this plan fixes

The builder may refine wording, but the following are the plan's reading of
the spec. A critic who disagrees should say so before the build.

1. **The act assembler gets its own module,** `project-trajectory/scripts/adjudicate_act.py`.
   It does not go in `adjudicate_brief.py`. The spec allows either, but the
   assembler reads registries and snapshot copies at a revision and the dial,
   and that is a different concern from composing a judging brief. A separate
   module also keeps `adjudicate_brief.py` well under the ratchet. Its one
   public call is `act_values(root, verdict, wi, rev="HEAD") -> (values, None) | (None, reason)`,
   plus `compose_act(root, verdict, wi)` returning the filled brief or the
   reason, and `owed_acts(root, verdict, rev)` returning the derivation the
   entry point re-runs after the call. It follows rule 2 of
   `adjudicate_brief`'s header: all or nothing, never a partial brief.
2. **The bless mark (Q2)** is a distinct amendment row tag:
   `- [MEANING+BLESS] <row-id> <cell> -> ...`. `kitlib.verdict.ROW_RULINGS["amendment"]`
   gains `"- [MEANING+BLESS]": "MEANING"`, so every existing reader
   (`row_rulings`, `verdict_rulings`, `judged_rows`, `held_reattest_refusal`)
   still reads the row as MEANING. A new reader, `kitlib.verdict.blessed_rows(text)`,
   returns the ids on `[MEANING+BLESS]` lines. A row that is also tagged plain
   `[MEANING]` or `[CLARITY]` reads as not blessed, which is fail-toward-no-act.
   An absent mark reads as not blessed. `- [MEANING]` does not prefix-match
   `- [MEANING+BLESS]`, so `_ruled_row` needs no other change.
3. **The act derivation reads committed state only.** Each verdict and its
   binding are read through `kitlib.sitting.accepted_at(root, "HEAD", verdict)`.
   Each row's committed text is `acceptance_record.rows_at(root, "HEAD", rel, id_col)`
   for the live registry, and for its copy under
   `docs/archive/last_approved/<rel>`. "Copy equals committed text" compares the
   whole parsed row, Status included. That is the only comparison under which a
   flip committed without its copy, where a whole-registry copy carries the row
   `Drafted` with identical text, reads as inconsistent rather than taken. The
   partition, per authorized row, is S3 "Re-runs" verbatim:
   - **first approval** (APPROVE): committed status below Approved means the act
     is owed, whatever the copy holds. Approved with an equal copy means taken.
     Anything else is inconsistent.
   - **re-attest** (CLARITY, or MEANING+BLESS on a released rung): Approved with
     an equal copy means taken, and Approved otherwise means owed. Below
     Approved, or absent, is inconsistent.
   An inconsistent row refuses the whole derivation and names the row.
4. **The dial is read at the act,** through `kitlib.authority.dial_at(root, "HEAD")`
   and `holds_under` / `rung_for`, never from the working file. On a held rung:
   a MEANING row owes no act; a CLARITY row is re-attested with
   `--verdict <verdict path>`, and `--verdict` is passed when any listed
   re-attest row is held; an APPROVE row owes no act, because the owner signs
   it. The last reading follows `first_approval_values`' rule that "a dial the
   owner tightens afterwards must bind the act it has not yet authorised". The
   spec's Trust list does not name a held APPROVE row, so this is flagged for
   the critic. It cannot widen an act: it only withholds one.
5. **What owes no act:** a RETURN row, a MEANING row without the mark, a held
   MEANING row, a held APPROVE row, a `done-when` part, and every brief class
   other than `amendment`, `first-approval` and `combined`. A verdict whose
   derivation lists nothing is refused as "owes no act". That covers a re-run
   after a completed act.
6. **The act brief's `--approves`** is derived from the owed APPROVE rows only,
   as `baseline_snapshot.format_approves({rel: wi})`. A mixed verdict therefore
   never names a registry whose rows were all returned, and the
   `{approves_rows}` drop rule is no longer the session's to apply.
   `{registries}` and `{approves_rows}` leave the first-approval template. The
   act brief carries `{registries}`, together with the per-token rows list as
   evidence of what each token covers.
7. **Order and commits:** the amendment act first, then the first-approval act,
   each in its own reviewed commit with the `WI:` trailer, text before act
   (WI-806). When the derivation finds the amendment act taken and the
   first-approval act owed, only the first-approval act is listed.
8. **Retention:** the act turn builds `session_service.AdjudicationRequest` with
   `brief =` the verdict's bound class (read off its binding), so
   `adjudication_keep` retains the act turn exactly where the `[adjudicator]`
   dial retains the verdict's class, and runs it fresh otherwise.
   `adjudicate_brief.governing_templates` adds the act template's identity
   whenever the retained set holds an actable class (`amendment`,
   `first-approval` or `combined`). An edit to the act brief therefore drains a
   retained session, as an edit to any retained template does. This changes the
   identity once at landing: a retained session drains on its next call. That
   is harmless, and the RESYNC entry states it.
9. **Success after the call** (exit 0) requires all three: (a)
   `session_service.call_succeeded`; (b) `owed_acts` at the new HEAD lists
   nothing owed and nothing inconsistent; (c) nothing under `docs/reviews/`
   changed, read as `git diff --name-only <HEAD before>..HEAD -- docs/reviews`
   plus `git status --porcelain -- docs/reviews`. Otherwise it exits 1 and names
   which condition failed. The act turn never calls `record_outcome`, never
   reserves a path and never writes a binding.
10. **The `act` command's input:** `act --verdict PATH --wi WI-N [--route ID] [--root DIR] [--timeout S]`,
    with `lane_refusal` and `resolve_route` as `adjudicate` has them. These
    refuse with exit 2 before anything launches: a verdict absent at HEAD or
    unreadable, one with no binding or a `pending` or `failed` binding, one that
    is malformed against its binding (all of these are `accepted_at` returning
    None, with the reason refined by reading the binding with `read_requested`);
    one that owes no act; an inconsistent row, named; and a lane with
    uncommitted changes, with the paths named from
    `git status --porcelain --untracked-files=all`. The brief is composed by the
    command (Q1). There is no `--brief-file`.

## Plan

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | The plan gate: this plan passes `plan_coverage.py --item` and its independent critique before any build; WI-913 has landed (b803dd019) and the plan is produced after the claim | D6 | no interface (a process step; intra-module escape) | |
| P2 | The bless mark: `kitlib.verdict` gains the `[MEANING+BLESS]` tag in ROW_RULINGS and the `blessed_rows` reader (Q2); the amendment template's row-line grammar documents the mark | D1; D2; SR-232; TC-331 | IF-175; IF-287 | P1 |
| P3 | The act brief file: `prompts/adjudicate-act.template.md`, the `ADJUDICATE_ACT` key in `prompts.py`, the bootstrap manifest rows for the template and for `scripts/adjudicate_act.py`, the prompts README row and the `docs/declared-absences` line | D1; SR-146; TC-157; TC-192 | IF-113; IF-097; IF-098 | P1 |
| P4 | The act assembler `scripts/adjudicate_act.py`: `owed_acts`, `act_values` and `compose_act`, reading the verdict through `accepted_at`, rows and copies at HEAD, and the dial at HEAD | D1; D2; SR-231; SR-232; SR-146; TC-161 | IF-287; IF-175; IF-195; IF-196; IF-124; IF-113; Proposed: the act assembler's call surface (owner scripts/adjudicate_act, requestor scripts/coordinator_adjudicate); nearest IF-115, which is the judging composer's compose/record_outcome contract for routed judging classes and falls short because the act brief is no judging class, writes no binding and is composed from a committed verdict rather than a row | P2; P3 |
| P5 | The sitting briefs judge only: the three templates and `adjudicate_brief`'s `_RELEASED_AFTERMATH` and `_HELD_ARMS["reattest"]` stop ordering an act; first-approval loses `{registries}` and `{approves_rows}`; `governing_templates` adds the act template for actable retained classes | D1; D2; SR-146; SR-232; TC-161; TC-331 | IF-113; IF-115; IF-124; IF-282 | P3; P4 |
| P6 | The act turn: the `act` command in `coordinator_adjudicate.py`, with its pre-launch refusals, a retained or fresh launch by the verdict's class, and success only when no listed act is left and nothing was written under docs/reviews | D1; D2; SR-231; TC-321 | IF-283; IF-284; IF-285; IF-282; IF-246; IF-065; Proposed: the act assembler's call surface from P4 (nearest IF-115, as P4 states) | P4; P5 |
| P7 | The trailer line: under the loop marker, every prompt either command launches ends with `agent_brief.loop_provenance_note()`; without the marker nothing is added (Q4) | D2; SR-209; TC-242; TC-321 | IF-260; IF-194 | P6 |
| P8 | The change's trace rows: the SR-231 amendment; the LLR-306, LLR-167 and LLR-310 amendments; a new LLR for `adjudicate_act.py`; a new TC; the TC-321 and TC-161 evidence cells; IF-283/284/285 and the other IF edits; the proposed IF row; a runtime flow for the judging and act turns | D3; SR-231; SR-146; SR-232; SR-209; TC-321; TC-161; TC-242; TC-331 | IF-283; IF-284; IF-285; IF-175; IF-287; IF-195; IF-196; IF-124; IF-113; IF-115; IF-260; IF-282 | P2; P4; P5; P6; P7 |
| P9 | The texts: PROCESS_OPTIONS "Who performs the approval act" (the amendment row's act becomes the later act turn) with the byte-budget-guard delta; the coordinator-cycle skill §1, §3, §4 and recipes; the `.claude/skills/` sync | D1; D4 | no interface (prose and a skill copy; intra-module escape) | P6 |
| P10 | The RESYNC_PACK entry: one entry for the shipped files, no forced migration, stating that the loop's route has no act turn yet (Q3) | D5; SR-146 | no interface (a pack entry; intra-module escape) | P6; P7; P9 |
| P11 | This lane's checkpoint in the new shape, run from the lane root: the judging turn (a combined sitting through `adjudicate`), then the act turn (`act`) after the rebase and the unchanged-rows precondition; the coordinator records it as a decision | D3; SR-231; SR-232; TC-321 | IF-283; IF-284; IF-285 | P8; P9; P10 |
| P12 | The landing bar on the landing tip: the smoke tier within 60 s, `check_trajectory.py --strict` clean, `trace.py --strict` with no finding beyond LLR-292's, the prompt catalogue `--check` passing, the full suite once at close | D4; D7; SR-146; SR-209; SR-231; SR-232; TC-157; TC-161; TC-192; TC-242; TC-321; TC-327; TC-331; TC-333 | no interface (a verification step; intra-module escape) | P11 |

No clause is excluded: every D# clause is covered by a row above.

## Steps in detail

Every test named below is written before its code and run red on the
pre-change tree, using the lane's base commit. The red output goes in the lane
report. "Fails before" says why it is red on today's code.

### P1: the plan gate (D6)

The coordinator commits this plan. `plan_coverage.py --item` judges it, and an
independent critic from another model family follows. No build starts before
both pass. WI-913 is on trunk at `b803dd019`, so the "built only after the plan
gate lands" hold is met at the claim's base. Nothing is built in this row.

### P2: the bless mark (Q2; D1, D2)

- `kitlib/verdict.py`: add `"- [MEANING+BLESS]": "MEANING"` to
  `ROW_RULINGS["amendment"]`, and add `blessed_rows(text) -> frozenset`. The new
  reader's docstring carries `Implements: SR-232, LLR-310` and cites
  coordinator-2026-10-14 D-003 (Q2).
- `adjudicate-amendment.template.md`: the row-line grammar gains
  `- [MEANING+BLESS] <row-id> <cell> -> ...`, meaning "a MEANING row whose new
  text you would bless". It is read only on a released rung. On a held rung it
  is a recommendation to the owner, and the act turn never acts on it (P4
  decision 4). That edit is made in P5, together with the rest of the template.
- Tests, in a new `tests/test_adjudicate_act.py` (an in-process module):
  - `test_a_MEANING_BLESS_row_reads_MEANING_and_blessed`. Fails before:
    `blessed_rows` does not exist, and `row_rulings` reads nothing for the tag.
  - `test_an_unmarked_MEANING_row_is_not_blessed`, and
    `test_a_row_tagged_both_ways_is_not_blessed`. Fail before: no reader exists.

### P3: the act brief file (Q1; D1)

- `project-trajectory/prompts/adjudicate-act.template.md`. Its dispatcher block
  names its slots, its rulings (revisions 32 and 36, Q1, owner ruling 6 and
  WI-806) and what is deliberately absent: no judging question and no verdict
  path. Slots, all strict-filled: `{verdict}` (the committed verdict that
  authorizes the act), `{wi}`, `{amendment_act}` and `{approval_act}` (each the
  rendered act or `none owed`, a state the assembler derives and a literal it
  never fills by default; see P4), `{registries}` and `{approves_rows}`.
- The body carries the act instructions in their one home. They move out of the
  three sitting templates and the composer, as follows.
  - The flips: Status `Drafted` to `Approved` for the listed rows only, with
    every other cell byte-exact.
  - The `intake.py snapshot` forms: `--approves "{registries}"` quoted, because
    `;` is a shell command separator; `--reattests ID[,ID...]`; and
    `--verdict {verdict}` where it is listed.
  - The drift refusal: when the snapshot refuses, naming a row not listed, stop,
    leave nothing uncommitted beyond what the refusal left, and report. Never
    widen `--reattests`.
  - The order: the amendment act, then the first-approval act, each in its own
    commit ending `WI: {wi}`.
  - The prohibitions: write nothing under `docs/reviews/`, edit no registry cell
    but `Status`, and approve no row not listed.
- `prompts.py`: `ADJUDICATE_ACT = "ADJUDICATE-ACT"` and its file. The key is not
  added to `adjudicate_brief.BRIEF_PROMPTS`, because that table is the judging
  classes and the `--brief` choices of `adjudicate`.
- `kitlib/bootstrap_manifest.py`: rows for `prompts/adjudicate-act.template.md`
  and `scripts/adjudicate_act.py`, each with its reason comment. Also the
  `prompts/README.md` table row, and the `docs/declared-absences` line in the
  shape of line 134.
- `CATALOG.md` and `docs/cli-reference.md` are generated, trunk-only paths
  (`docs/stack.ini` `[generated]`). They are not committed in the lane. They are
  regenerated at the landing, by the coordinator's landing recipe, and P12
  checks `--check`.
- Tests: the existing TC-157 and TC-192 pins
  (`test_the_catalogue_lists_every_shipped_prompt_with_its_digest` and the
  manifest test) go red until the key, the file and the manifest row agree. Add
  `test_the_act_brief_is_a_shipped_prompt_with_strict_slots` to
  `tests/test_routing_and_prompts.py`: an unfilled slot refuses. It fails before
  because the key does not exist.

### P4: the act assembler (Q1; S3 "Re-runs"; D1, D2)

- `owed_acts(root, verdict, rev)` returns `(acts, None)` or `(None, reason)`.
  `acts` is `{"amendment": {"reattests": [...], "verdict": bool}, "first-approval": {"approves": {rel: [ids]}}}`,
  each part present only when something is owed. It implements decisions 3, 4,
  5 and 7. Its reason names the input it refused: the verdict is absent at
  `rev`; it has no binding; its binding is `pending` or `failed`; it is
  malformed against its binding; it is a class that owes no act; it owes no act;
  or row X is inconsistent, with its status and copy state named.
- `act_values` and `compose_act` fill the P3 template from `owed_acts` at HEAD
  through `prompts.fill`, or return the reason. Neither returns a partial brief.
- The module header names the Trust section's carrier, its consumers and the
  rulings it carries: revisions 31, 32 and 36, Q1 and Q2, owner ruling 6 and
  OI-45 (b).
- Tests, in `tests/test_adjudicate_act.py`, using real git fixtures (the
  `_first_approval_repo` and `_amendment_repo` shapes, re-used through
  `conftest` or copied minimally). Each fails before because the module does not
  exist. Each also pins the behaviour named:
  - `test_each_unaccepted_or_unreadable_verdict_is_refused_naming_why`,
    parametrized over: absent at HEAD; present but uncommitted; no binding;
    `pending`; `failed`; malformed against its binding; a class that owes no
    act (`done-when`, `disposition`). These are the Trust section's refusals at
    the assembler.
  - `test_a_mixed_first_approval_verdict_approves_only_its_approved_rows_registries`:
    APPROVE on an LLR row and RETURN on the only TC row. `--approves` names the
    LLR registry alone.
  - `test_a_MEANING_row_without_the_bless_mark_is_left_unacted`, and
    `test_a_blessed_MEANING_row_on_a_held_rung_is_left_unacted`.
  - `test_a_held_rung_CLARITY_row_is_reattested_naming_its_verdict`. This is the
    successor of TC-161's
    `test_a_held_rung_CLARITY_verdict_is_the_sessions_reattestation`, moved from
    the judging brief to the act.
  - `test_a_combined_verdict_lists_the_amendment_act_before_the_first_approval_act`.
  - `test_a_combined_act_interrupted_between_its_commits_lists_only_the_first_approval_act`:
    the amendment re-attest is committed, and the flip is not.
  - `test_a_flip_committed_without_its_copy_is_refused_naming_the_row`.
  - `test_a_Drafted_row_present_unchanged_in_a_whole_registry_copy_is_owed`.
  - `test_a_reattest_of_a_row_below_Approved_is_refused_naming_the_row`.
  - `test_a_completed_act_owes_none_and_is_refused`.
  - `test_the_rendered_act_commands_survive_a_shell`. This is the successor of
    `test_the_rendered_snapshot_command_survives_a_shell`: one command for a
    two-registry `--approves`.
  - `test_the_act_reads_HEAD_not_the_working_tree`: an uncommitted flip leaves
    the row owed.
- Size: a new module well under 1000 SLOC, with no ratchet row needed. The
  complexity baseline is untouched, because each function stays under its
  budget (`deep-module-design`): the partition is one function per act kind
  over one row reader.

### P5: the sitting briefs judge only (revisions 32 and 36; D1, D2)

- `adjudicate-first-approval.template.md`: delete "If the answer is APPROVE,
  perform the act" steps 1 to 3, the `{registries}` and `{approves_rows}` slots,
  and the "THEN, AND ONLY AFTER ... Stop only after that approval commit is
  recorded" block. In their place, the verdict is the turn's whole output: write
  it, commit it with `WI: {wi}`, and stop. Its act is a later turn taken from
  that committed verdict (cite revision 32). RETURN's `## Dispositions` drafting
  stays, because it belongs to the verdict.
- `adjudicate-amendment.template.md`: the "Take the act in its own reviewed
  commit ..." paragraph and the per-arm "re-attest it" instructions are
  replaced. Each verdict now records what the act needs: CLARITY;
  MEANING+BLESS on a released rung (P2's mark); or MEANING, which means "do not
  bless": draft `## Dispositions`, or on a held rung recommend to the owner. The
  verdict commit is the end of the turn. The held MEANING and held first-draft
  stops for the human-or-delegate stay as they are.
- `adjudicate-combined.template.md`: the "take each act a section owes in its
  own reviewed commit" and "then take each act a section owes" clauses become
  "the sitting ends at its committed verdict; its acts are a later turn".
- `adjudicate_brief.py`:
  - `_RELEASED_AFTERMATH` now tells the judge which mark it owes: CLARITY rows
    are re-anchored by the later act turn, and a MEANING row it would bless is
    marked `[MEANING+BLESS]`.
  - `_HELD_ARMS["reattest"]` now says the CLARITY row is re-attested by the
    later act turn, naming this verdict.
  - Neither arm says "BY YOU" or gives an `intake.py snapshot` command.
  - `first_approval_values` stops returning `registries` and `approves_rows`. It
    keeps its internal per-registry walk, because `_judged_tiers` needs it for
    `{questions}`.
  - `governing_templates` adds `prompts.template_path(ADJUDICATE_ACT)`, or the
    operator's override under that key, when the classes intersect
    `{"amendment", "first-approval", "combined"}` (decision 8).
  - The size ratchet is re-stamped downward in the same commit if the module
    shrinks, which is the ratchet's rule.
- Tests, in `tests/test_adjudicate_brief.py` (TC-161):
  - Delete `test_the_first_approval_brief_cannot_stop_before_its_approved_act`
    (WI-572's pin). Its successor is P6's
    `test_the_act_turn_reports_success_only_when_no_listed_act_is_left` (D1).
  - Add `test_no_judging_brief_orders_an_act`, parametrized over first-approval,
    amendment (released and held) and combined composed briefs. Each composed
    text contains no `intake.py snapshot`, no "BY YOU" and no instruction to flip
    a `Status`, and does say the act is a later turn. Fails before: all three
    compose the act today.
  - Re-point `test_the_MEANING_aftermath_is_DERIVED_from_the_dial_not_left_to_the_judge`
    and `test_the_amendment_brief_reanchors_CLARITY_rows_and_keeps_the_sibling_hold`
    to the new wording. The dial is still derived and the held MEANING row still
    goes to the owner, and neither test asserts an act any longer.
  - Remove the first-approval compose test's `snapshot --approves` assertions;
    `test_the_rendered_snapshot_command_survives_a_shell` moves to P4.
  - Re-point `test_a_mixed_batch_can_tell_which_rows_each_approves_token_covers`
    to the act derivation in P4.
  - Add `test_the_identity_covers_the_act_brief_for_an_actable_retained_class`
    to `tests/test_coordinator_adjudicate.py`, beside
    `test_the_identity_covers_each_class_...`. Fails before: the act template is
    in no identity.
- TC-331 (`test_integrate_admission.py`) is run unchanged. Its pins are what
  prove "the split moves no act out of the branch that carries its binding": the
  merge slot still admits an in-lane act backed by an accepted verdict.

### P6: the act turn (Q1; D1, D2)

- `coordinator_adjudicate.py`:
  - An `act` subparser and an `act(args)` handler, implementing decisions 9 and
    10.
  - Pre-launch, in order: `lane_refusal`, `resolve_route`, the clean-lane check,
    then `adjudicate_act.compose_act` at HEAD (all exit 2, with
    `act: refused: <why>`).
  - The keep: `AdjudicationRequest(brief=<bound class>, ...)` and
    `adjudication_keep`, with the sign-in refusal giving exit 7.
  - The launch, through `session_service.call` with `source_event="coordinator"`.
  - After the call: decision 9's three conditions, printed as
    `act: owed after the call: <list>` or `act: wrote under docs/reviews: <paths>`.
  - The `act` path reserves nothing, binds nothing and calls no
    `record_outcome`.
  - The module header's Contracts IF-283, IF-284 and IF-285 gain the `act`
    command, its exits (0 complete; 1 failed call, act left owed or
    inconsistent, or a write under docs/reviews; 2 pre-launch refusal or
    blackout; 7 sign-in) and its readings. The header's TEMPORARY note says
    WI-801 must carry `act` into `ask`.
- Tests, in a new `tests/test_coordinator_act.py`. It reuses
  `test_coordinator_adjudicate.py`'s lane fixture and stubbed
  `session_service.run_session`, where a stub "adjudicator" runs the brief's
  commands in the lane. Every test fails before because no `act` command exists:
  - `test_the_act_command_refuses_each_trust_input_before_launch`, parametrized:
    the primary checkout, an unclaimed worktree, no repository, a route off the
    enable list, a verdict absent at HEAD, no binding, `pending`, `failed`,
    malformed, owes no act, an inconsistent row (named), and a dirty lane (paths
    named). Each asserts exit 2, that nothing launched, and that no file was
    created or changed.
  - `test_a_retained_and_a_fresh_act_turn_take_the_same_act_from_one_verdict`:
    one verdict, the dial retaining its class and then off. The prompt delivered
    is byte-identical, the keep line differs (resuming or minting, against
    fresh), and both end with the same flips and copies at HEAD and exit 0.
  - `test_a_combined_act_commits_its_amendment_act_before_its_first_approval_act`:
    the commit order is read from `git log`.
  - `test_the_act_turn_reports_success_only_when_no_listed_act_is_left`. This is
    WI-572's pin's successor: a stub that takes the amendment act but skips the
    flip exits 1 and names the owed act.
  - `test_an_act_turn_that_writes_under_docs_reviews_does_not_succeed`: a stub
    that does the whole act and also edits the verdict exits 1.
  - `test_an_act_interrupted_between_flip_and_snapshot_is_refused_dirty_then_rerun_in_full`:
    a stub leaves the flip uncommitted, so the call exits 1 and the next `act`
    exits 2 naming the paths. After `git checkout -- .` (the coordinator's
    discard), `act` lists the whole act and a full stub exits 0.
  - `test_a_combined_act_interrupted_between_commits_reruns_with_only_its_first_approval_act`:
    the second prompt holds no `--reattests`.
  - `test_the_act_turn_writes_no_binding_and_reserves_no_path`.
- `tests/test_coordinator_adjudicate.py` stays in the smoke tier. The new file
  is measured: it joins `tests/conftest.py` `SLOW_MODULES` only if the smoke
  tier would breach 60 s. In that case one in-process pin stays smoke, namely
  the `owed_acts` refusal of an unaccepted verdict, as CLAUDE.md asks of every
  script family.

### P7: the trailer line (Q4; D2)

- `coordinator_adjudicate.py` gets one helper, `_launched(prompt)`, which returns
  `prompt + agent_brief.loop_provenance_note()`. The note is `""` without the
  marker. Both `adjudicate` (after `bind_requested` and `requested_for` read the
  unmodified brief, so the binding is unchanged) and `act` launch its result.
  That is one construction for every prompt the entry point launches (S3, "The
  trailer").
- Tests, in `tests/test_coordinator_act.py`:
  - `test_under_the_loop_marker_every_launched_prompt_ends_with_the_loop_session_line`,
    parametrized over every class in `adjudicate_brief.BRIEF_PROMPTS` plus
    `act`. It sets `kprovenance.LOOP_SESSION_ENV` with monkeypatch, captures the
    prompt the stub received, and asserts it `endswith(agent_brief.loop_provenance_note())`
    and holds the `Loop-Session` trailer. Fails before: the entry point appends
    nothing.
  - `test_without_the_marker_no_prompt_carries_the_line`: the delivered prompt
    equals the composed brief byte for byte, and holds no `Loop-Session`. It
    passes before for `adjudicate`, and is the pair's negative half.

### P8: the trace rows (D3)

Authored on the lane by the spine author at the checkpoint, as the
coordinator-cycle §3 sends it. New ids are drawn from `docs/id-watermark` at
authoring, and the floor briefing covers ids of other open lanes. All new rows
are `Drafted`, and amended Approved rows keep `Approved` with their text changed.

- **SR-231**, amendment (MEANING expected). Today it admits only a fresh
  judgement ("a valid claimed lane exclusively reserves a new verdict path").
  The requirement and acceptance gain the act turn: from a claimed lane, an act
  taken only from a verdict accepted at the lane's HEAD; a refusal before launch
  of each unaccepted, act-less or inconsistent verdict and of a dirty lane;
  success only when no authorized act is left untaken and nothing was written
  to the verdict records. The text is in capability voice: no module, path or
  command names (owner ruling 2026-10-11, "requirements never reference code").
- **SR-146, SR-232, SR-209**: no text change expected. The act brief is one more
  shipped, catalogued prompt (SR-146). The combined sitting's per-kind scope and
  the one reader are unchanged (SR-232). The trailer reaches more prompts under
  an unchanged rule (SR-209). If the spine author's tier questions find an SR
  short, that is an amendment in this lane, sat at the same checkpoint.
- **LLR-306** amendment: the entry point's detail gains the `act` command
  (decisions 8 to 10) and the trailer line (P7). `sr_refs` gains SR-209 for the
  trailer clause, and `code_symbol` gains `act` and `_launched`.
- **LLR-167** amendment: the judging briefs carry no act, and
  `first_approval_values` no longer derives `--approves`.
- **LLR-310** amendment: the amendment row grammar's bless mark and the
  `blessed_rows` reader.
- **New LLR** (SR-231, SR-232): `module = project-trajectory/scripts/adjudicate_act.py`,
  carrying the derivation (decisions 3 to 7) and the all-or-nothing rule.
  `component = CMP-008`.
- **New TC** verifying SR-231, SR-232, the new LLR, LLR-310 and the proposed IF:
  evidence `tests/test_adjudicate_act.py` and `tests/test_coordinator_act.py`,
  with its tier set by P6's measurement.
- **TC-321** gains the P6 and P7 test names, and its `verifies` gains SR-209.
  **TC-161**'s evidence drops WI-572's pin and the moved held-CLARITY test, and
  gains `test_no_judging_brief_orders_an_act`. **TC-242** is unchanged; its
  `Loop-Session` floor is the rule P7's line serves. **TC-331** is unchanged.
- **IF rows:**
  - IF-283, IF-284 and IF-285: data and contract summaries name the `act`
    command, its exits and its readings.
  - The proposed new IF: the `adjudicate_act` call surface, intra-component
    CMP-008, owner `scripts/adjudicate_act`, requestor
    `scripts/coordinator_adjudicate`.
  - Requestor additions of `scripts/adjudicate_act`: IF-287 (`accepted_at`),
    IF-175 (row rulings plus `blessed_rows`, data amended), IF-195 (`dial_at`),
    IF-196 (`rows_at` added to data), IF-124 (`format_approves`, `SNAPSHOT_DIR`)
    and IF-113 (`ADJUDICATE-ACT` added to data).
  - IF-260: requestor `scripts/coordinator_adjudicate` (`loop_provenance_note`).
  - IF-115: notes updated, because the composer no longer derives `--approves`.
  - IF-282: unchanged in shape, but the act turn is a second request from
    `coordinator_adjudicate`, so a note line is added.
- **`docs/runtime-flows.md`**: a new flow, "The coordinator's judging turn and
  act turn (SR-231, SR-232, the new LLR, LLR-306)". The judging turn runs
  reserve, bind, launch, commit the verdict, then `record_outcome` accepted. Any
  time later, rebase, then the coordinator's unchanged-rows check, then `act`
  derives at HEAD, launches retained or fresh, and re-derives, giving exit 0 or
  1. The merge slot's `uncovered_refusal` / `unaccepted_refusal` close the flow.
- `components.derived.toml` is regenerated at landing (it is generated), never
  in the lane.
- **Not a test row:** this row authors spine text. Its checks are
  `check_trajectory.py --strict` and `trace.py --strict` on the lane, run before
  the checkpoint commit (the R-F lesson: run `--strict` before the landing
  commit).

### P9: the texts (D1, D4)

- `PROCESS_OPTIONS.md` "Who performs the approval act", in the division-of-labour
  table's amendment row. "followed by its own re-attestation in the same session"
  becomes "its act is a later adjudicator turn, taken from the committed verdict
  (revision 32); a MEANING row is re-attested there only when its verdict
  blesses it". The "Where" row gains one clause: the verdict may be sat at any
  time, and the act keeps landing order. Cite revisions 31, 32 and 36. Before and
  after, run the `byte-budget-guard` skill and record the delta in the lane
  report (D4).
- The coordinator-cycle skill
  (`project-trajectory/skills/coordinator-cycle/SKILL.md` and
  `references/recipes.md`):
  - §1: replace "the adjudicator commits its verdict and its act".
  - §3: the checkpoint sitting ends at its verdict, and the stash-and-commit act
    steps are replaced by the act turn.
  - §4: the split. Verdicts may be sat at any time, for any lane. Acts keep
    landing order: the act runs only after the lanes ahead have landed and this
    lane has rebased, and lanes that take acts land one at a time. Before the act
    turn, the precondition is that the judged rows are unchanged since the
    verdict judged them. That is checked by comparing the rows at the verdict's
    own commit, before the rebase, with the rebased tip, with a renumbered row
    counting as changed. Any changed row is re-sat (revision 32, text only).
  - The recipes: the `act` command line, the precondition's check (for example
    `git show <verdict-commit>:<registry>` against the tip's rows for the judged
    ids), the discard-leftovers recovery recorded as a decision, and the
    "lanes in flight" rule (S3): a pre-landing verdict whose act is still owed is
    re-sat, since it carries no bless marks.
- Sync: `python project-trajectory/scripts/bootstrap.py --dest . --sync`, then
  confirm that `.claude/skills/coordinator-cycle/` matches the kit source
  (D4; `tests/test_dogfood_sync.py` holds it). The skill is
  `scope: this-repo`, so it gets no RESYNC entry.
- WI-911 landed first and edited the same §4 and recipes. This lane is built on
  that text, so the edit is a rebase-safe amendment of its sentences, not a
  rewrite.

### P10: the RESYNC entry (D5)

One `### The sitting ends at its verdict; its act is a later turn [since <anchor>]`
entry before `## 5. Promotion`, in the shape of the entries around it.

- **What changed:** the three sitting briefs judge only; the act brief; the
  `act` command; the bless mark; and the trailer line under the loop marker.
- **Kit-owned files — overwrite:** `prompts/adjudicate-first-approval.template.md`,
  `prompts/adjudicate-amendment.template.md`, `prompts/adjudicate-combined.template.md`,
  `prompts/adjudicate-act.template.md` (new), `scripts/adjudicate_brief.py`,
  `scripts/adjudicate_act.py` (new), `scripts/coordinator_adjudicate.py`,
  `scripts/prompts.py`, `scripts/kitlib/verdict.py`,
  `scripts/kitlib/bootstrap_manifest.py` and `PROCESS_OPTIONS.md`.
- **What to do:** overwrite them. No registry, setting or record format
  migrates. A retained adjudicator session drains once, on its next call
  (decision 8). A verdict sat before the upgrade whose act is still owed is
  re-sat, since it carries no bless marks.
- **The loop's route (Q3):** it has no act turn yet. Its sittings end at their
  verdict, and the loop's act turn is built in WI-809. The managed loop stays
  paused until WI-809 lands.
- A test-free pin: `tests/test_resync_pack.py`, or the RESYNC check WI-911's
  batch added, must accept the entry. The builder runs it.

### P11: this lane's checkpoint in the new shape (D3)

Run from the lane root, `C:/Projects/ai-template.wt/wi-912`, after P8's rows
are committed:

1. Compose the combined sitting with `compose_lane.py`, which calls
   `adjudicate_brief.compose`. That is the judge-only brief this lane built.
   Run it with `coordinator_adjudicate.py adjudicate --brief combined --wi WI-912 --verdict docs/reviews/wi-912/NNN-ADJUDICATE-<sha7>.md`.
   The sitting judges SR-231's amendment, the LLR amendments and the new
   `Drafted` rows. It ends at its committed verdict, with `record_outcome`
   accepted.
2. Rebase onto current trunk after the lanes ahead land.
3. Run the precondition: the judged rows at the verdict's commit, against the
   rebased tip. Re-sit any that changed.
4. Run `coordinator_adjudicate.py act --verdict <that path> --wi WI-912`. That
   takes the amendment act (SR-231's re-attestation, a MEANING+BLESS row on a
   released rung, and the LLR re-attestations), then the first-approval act,
   each in its own commit.
5. The coordinator records "the lane's checkpoint was sat in the new shape:
   judging turn, then act turn after the rebase" as a decision in
   `docs/decisions/coordinator-<date>.toml`.

A RETURN re-sits only the returned ids. A held row cannot arise here, because
this repo's dial releases SR-231's rung (B3/B4 in the spec).

### P12: the landing bar (D7, D4)

On the landing tip:

- `run.cmd smoke` / `run_menu.py smoke`: green, with the smoke tier within its
  60 s wall. If P6's measurement moved the new module to `SLOW_MODULES`, that
  move is stated with the timing.
- `python project-trajectory/scripts/check_trajectory.py --strict`: clean.
- `python project-trajectory/scripts/trace.py --strict`: no finding beyond
  LLR-292's.
- `python project-trajectory/scripts/gen_prompt_catalog.py --check`: passes
  once the landing regenerates CATALOG.md (D4).
- The full unfiltered suite once at close
  (`python -m pytest -q -n auto`, batched under the tool's 10-minute cap or
  backgrounded).

This step runs every TC verifying the item's SRs:

| TC | Verifies (item SRs) | This WI |
|---|---|---|
| TC-157 | SR-146 | run: the shipped prompts load (P3) |
| TC-161 | SR-146 | amended evidence (P5); run |
| TC-192 | SR-146 | run: the catalogue lists the act brief and its digest (P3) |
| TC-242 | SR-209 | run unchanged: the trailer floor P7's line serves |
| TC-321 | SR-231 | amended evidence and verifies (P6, P7, P8); run |
| TC-327 | SR-232 | run unchanged: Done-when blessing; a `done-when` part owes no act |
| TC-331 | SR-232, SR-146 | run unchanged: the merge slot admits a backed in-lane act (P5) |
| TC-333 | SR-146 | run unchanged: review and critique briefs are untouched |

The output is pasted as produced, never claimed.

## Risks and what the critic should check

- **Decision 4's held APPROVE reading** is the plan's reading, not a spec
  sentence. It fails toward no act.
- **Decision 3's whole-row comparison.** A non-normative cell edited on a judged
  row after its act reads as owed or inconsistent, never as taken. That is
  fail-closed, and the coordinator's unchanged-rows precondition re-sits such a
  row anyway.
- **The act turn trusts no landing order.** That stays the coordinator's
  precondition (Trust, revision 32). The plan adds no check for it, by ruling.
- **WI-801** deletes `coordinator_adjudicate.py` and must carry `act` into `ask`.
  **WI-809** builds the loop's act turn. Neither is an edge here, and the RESYNC
  entry and the module header name both.
