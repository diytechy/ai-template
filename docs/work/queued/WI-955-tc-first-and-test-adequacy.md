+++
id = "WI-955"
title = "Test cases come first in a lane, and reviewers judge each new test's strength and each new file's duplication"
workstream = "process"
sr_refs = ["SR-146"]
specref = "docs/plans/2026-10-11-review-churn/README.md#13-review-only-a-green-tip-review-test-cases-in-stages"
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "none"
needs = []
+++

## Context

Review-churn item 13, the text half of the queue's row P1. The owner ruled
item 13 as a whole (plan, revision 35) and confirmed TC-first in lanes
(revision 17).

**TC rows come after the code today.** The coordinator builds round 1, then
dispatches Terra to author the change set (`coordinator-cycle` SKILL §3,
"Intent", steps 1 and 2). Recipes §1 adds that a single plan placing the
spine turn at the checkpoint owes no intent turn (wi-918 D-002). That is the
reverse of PROCESS.md §7's test-first order. The ruled split: a TC **row**
is written with its LLR, before the build; test **code** is the build's
first deliverable, failing (plan item 13, "TC-first in lanes").

**Nobody checks test strength or duplication.** The reviewer template maps
each Done-when item to a test and checks a regression test's pre-fix
failure. It asks nothing about whether a test would catch a wrong
implementation, and nothing about duplication. Neither do the builder's
briefs (`kit-builder.md`, `worker.template.md`). Plan item 11, F-call 2:
"Duplication in intent can't be mechanized, so this is text, not a gate".

**Without P8.** The strict expected-failure marks are named here as the way
a test commit lands red. The commit check that enforces them, the test-file
tags and the scoped set are P8, a separate row. Until P8, the lane's tests
are the ones the coordinator names (`review_brief.py review --tests`).

**Anchor.** SN-007 (approved): the kit holds itself to its own standard.
SR-146 covers the reviewer template as a shipped, catalogued prompt. No row
text changes: this row moves procedure and prompt text only.

## Deliverables

1. **TC-first in the coordinator cycle** (`.claude/skills/coordinator-cycle/SKILL.md`
   §3 and its recipes; the `project-trajectory/skills/` copy stays
   byte-identical).
   - "Intent" reorders: Terra authors the change set, TC rows included,
     before build round 1 (after the plan pass record, for a `single` row).
   - Build round 1's first deliverable is the tests, committed alone before
     the code, each under one evidence class from item 13's typed-evidence
     contract (plan item 13, "typed evidence", revision 16):
     - **new or corrected executable behaviour:** marked as a strict
       expected assertion failure (Python: `@pytest.mark.xfail(strict=True, raises=(AssertionError, pytest.fail.Exception))`),
       the marks removed in the code commit. A red must reach the test's own
       assertion, not an import error (revision 17); a stub is the
       builder's choice;
     - **characterization of already-correct behaviour:** unmarked, with a
       stated adequacy witness (what wrong implementation it would catch);
     - **Inspection, Analysis or Attest TCs:** their declared method's
       independently checkable evidence, as the TC row states it.
     A test that fits none of the three is named in the lane's decisions
     record with its disposition before the code commit.
   - The recipe line "owes no intent turn" (wi-918 D-002) is replaced.
   - Lanes claimed before this lands keep their order, recorded as a
     decision.
2. **The same order in the shipped `spine-authoring` skill**,
   `references/in-lane.md` (both copies byte-identical): TC rows are
   authored with their LLRs before the build; row text is still reconciled
   and judged against settled code at the checkpoint, as now.
3. **The reviewer's test-adequacy questions** in
   `project-trajectory/prompts/reviewer.template.md`, beside the Done-when
   mapping. For each test the diff adds or changes:
   - does it drive the interface the requirement names, not handler source?
   - would it fail on a plausible wrong implementation?
   - is each Done-when item covered?
   The fourth question in the plan ("does a test name the IF it drives,
   where variant F requires it") waits for item 11's lane, which creates
   that rule.
4. **The duplication question.** In the reviewer template: of each new file
   and function, does it repeat, exactly or in intent, something that
   already exists (PROCESS.md §3, linked)? In `.claude/agents/kit-builder.md`
   and `prompts/worker.template.md`: search before minting a file or
   function, and name the nearest existing home considered.
5. **Records.** `prompts/CATALOG.md` regenerated. One RESYNC entry for the
   shipped template, worker brief and skill reference, anchored at the
   landing's parent.

## Done-when

- The coordinator-cycle skill's §3 places Terra's change-set turn, TC rows
  included, before build round 1, and names the test commit as round 1's
  first deliverable under the three evidence classes of Deliverable 1 (the
  strict mark and its removal for new or corrected behaviour, the adequacy
  witness for characterization, the declared method's evidence for
  Inspection, Analysis or Attest), with the recorded disposition for a test
  that fits none. No text in the skill or its recipes keeps "after the
  first build" or the wi-918 D-002 exemption.
- `in-lane.md` states the order; both `spine-authoring` copies and both
  `coordinator-cycle` copies are byte-identical.
- A test pins each of the three adequacy questions and the duplication
  question in the reviewer template (`tests/test_agent_loop_review.py`'s
  substring pattern), and a rendered `review_brief.py review` brief carries
  them.
- Both builder briefs, `.claude/agents/kit-builder.md` and
  `prompts/worker.template.md`, tell the builder to search before
  creating a file or function and to name the nearest existing home it
  considered; a test pins the sentence in each.
- `prompts/CATALOG.md` is fresh; the RESYNC entry check passes.
- On the landing tip, the commit bar is green, `check_trajectory.py
  --strict` and `trace.py --strict` clean.

## Scope answers

- **S1.** One deliverable set, text only. Lands first of P1's four rows
  (WI-955 to WI-958): no dependency, and every later P1 lane then runs
  TC-first.
- **S2.** None. No file gains authority.
- **S3.** The one input space is a new test's evidence class, closed by
  Deliverable 1's three classes; a test outside them is dispositioned
  by name in the lane's decisions record, never left to default.
- **S4.** `none`: text and pinning tests only, no code path.
- **S5.** No delta. The reviewer template's slots are unchanged.
- **S6.** None. B2 (WI-914) landed on 2026-10-16.
- **B1.** Deliverable 4's builder half is not in the queue text; it is
  listed because it is the producer side of the reviewer's question and no
  other row owns it. The critique kept it and asked for its Done-when item.
- **B4.** No owner act.

## Critique dispositions

Scope critique round 1 (Codex Sol, medium, 2026-10-20; CHANGES-REQUESTED,
findings=2):

- **MAJOR, S3 (the blanket strict-mark rule): adopted.** Deliverable 1 now
  reads "each under one evidence class from item 13's typed-evidence
  contract", naming the three classes, and the Done-when's first item names
  them; S3 states the closed set and the named disposition for a test
  outside it.
- **MINOR, B1 (the kit-builder half had no Done-when item): adopted.** The
  Done-when item now reads "Both builder briefs, `.claude/agents/kit-builder.md`
  and `prompts/worker.template.md`, tell the builder to search before
  creating a file or function and to name the nearest existing home it
  considered".
