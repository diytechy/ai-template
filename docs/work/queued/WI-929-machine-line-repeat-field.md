+++
id = "WI-929"
title = "The shared machine-line reader stops refusing a repeated field; the review verdict line's exact-form check already refuses one"
workstream = "process"
sr_refs = ["SR-232"]
specref = "docs/decisions/coordinator-2026-10-15.toml"
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "none"
needs = ["~WI-912"]
+++

## Context

The owner ruled (coordinator-2026-10-15 D-011) that WI-852's
duplicated-count verdict fix is discarded: agents are trusted to write a
verdict line, and the whole-grammar check superseded the fix. The audit of
guards built on contrived findings
(`docs/plans/2026-10-11-review-churn/audit-contrived-guards-2026-10-15.md`)
grades it CONTRIVED: no model writes a verdict line that names its count
twice.

The original rationale, read before drafting: WI-852's second full-lane
review found that `VERDICT: APPROVE findings=7 findings=0` was filed,
because the shared token reader keeps the last copy of a field. The builder
added a local repeated-field check at the filing boundary. One round later
the dispute sitting replaced that boundary's token checks with one
whole-line match (the review line must be exactly
`VERDICT: <APPROVE|CHANGES-REQUESTED> findings=<digits>`), and WI-870 then
moved the repeated-field refusal into the shared per-line reader "for every
consumer (adjudication verdicts included)" and removed the local copy.

So WI-852's own code is already gone. What survives is the shared reader's
repeated-field refusal in `kitlib/sitting.py`: `_machine_line` returns the
repeated fields, `_incomplete` refuses on them, `_machine_lines` threads
them. Its consumers are the review verdict line (`review_line`, read by the
filing boundary and the merge gate) and every adjudication sitting line
(`_one_line`, `line_refusal`).

The supersession claim was checked in process, on trunk:
- On the review line it holds. `review_line` refuses unless the stripped
  line equals the canonical line rebuilt from its parsed tokens, and a line
  with two `findings=` tokens never equals one with one. With the
  repeated-field check disabled, `findings=7 findings=0` and `findings=0
  findings=0` are still refused, as "not exactly" the canonical form.
- On adjudication lines it does not. They have no exact-form check, so with
  the repeated-field check gone, `VERDICT: MEANING rows=2 rows=0` reads as
  `rows=0`.

This row deletes the mechanism. On review rounds nothing changes but the
wording of the refusal. On adjudication lines, a line that repeats a
declared field reads its last copy, which only an adjudicator model writing
the same field twice on one line would reach. That is the class D-011 and
the audit call contrived, and it is stated residue (Deliverable 4). This
partly reverses WI-870's Done-when, which made the shared reader refuse a
repeated field for every consumer and which the audit did not grade. The
owner ruled that reversal at filing (coordinator-2026-10-15 D-017).

## Deliverables

1. **Delete the repeated-field refusal from the shared per-line reader**
   (`project-trajectory/scripts/kitlib/sitting.py`). `_machine_line` returns
   `(label, values)` again. `_incomplete` loses its `repeated` argument and
   branch. `_machine_lines` stops threading it. `review_line` is unchanged
   in behaviour: its exact-form comparison is the only thing that refuses a
   repeated count. No replacement check is added.
2. **Contract and docstring text.** The IF-287 contract sentence "every
   machine line naming a declared field twice is refused (WI-870)" is
   deleted. `review_line`'s docstring drops "and named once" and says the
   exact-form comparison refuses anything else on the line.
   `docs/interface-reference.md` is regenerated.
3. **Tests.**
   - `tests/test_adjudicate_brief.py`,
     `test_an_unusable_verdict_is_refused_and_says_which_way`: the
     `successors=7 successors=0` case and its comment are **deleted**.
   - `tests/test_review_brief.py`,
     `test_a_filed_coordinator_review_appears_in_the_rollup`: the
     `findings=7 findings=0` case is **kept**, its expected reason changed
     from "more than once" to "is not exactly", and its comment no longer
     names the shared reader's refusal.
   - `tests/test_score_reviews.py`,
     `test_the_gate_reads_a_malformed_verdict_line_as_no_verdict`: the
     `findings=7 findings=0` case is **kept** unchanged. It pins the
     outcome (no verdict), which the exact-form check still gives.
4. **Spine rows** (Terra authors; judged at the lane's checkpoint sitting):
   - **LLR-310** (Approved), **amended**: "a bare, split, bad-label,
     field-missing or declared-field-repeated line invalidates" becomes "a
     bare, split, bad-label or field-missing line invalidates"; "with
     findings named once" is deleted, since the canonical form already has
     exactly one count.
   - **TC-327** (Approved), **amended**: Method drops "including a machine
     line that names a declared field more than once"; Expected drops
     "refusing a line that repeats a declared field". Its test list is
     unchanged.
   - **TC-083** (Approved), **unchanged**: "a repeated findings field"
     still produces no verdict, now through the exact-form check.
   - **LLR-313**, **TC-333**, **SR-232**, **SR-235**: **unchanged**. None
     names the repeated-field refusal.
   - Residue, in the row's RESYNC entry and LLR-310's rationale if the
     sitting wants it there: an adjudication machine line that repeats a
     declared field reads its last copy.
5. **`RESYNC_PACK.md` entry**, anchored at a trunk commit: a shipped
   script changes. It says the review verdict line still refuses a repeated
   count (as not the exact form), and an adjudication line that repeats a
   field now reads its last copy. Nothing migrates and no adopter setting
   changes.

## Done-when

- `kitlib/sitting.py` holds no repeated-field branch: `_machine_line`
  returns two values and `_incomplete` takes no repeated-fields argument.
  Fails before the change (both carry it).
- The `successors=7 successors=0` case is gone from
  `test_an_unusable_verdict_is_refused_and_says_which_way`, and
  `test_a_filed_coordinator_review_appears_in_the_rollup` expects "is not
  exactly" for `findings=7 findings=0`. The second fails before the change
  (the reason there is "more than once").
- `test_the_gate_reads_a_malformed_verdict_line_as_no_verdict` passes
  unchanged. It passes before the change too, and that is the point: it
  shows the review line loses nothing.
- LLR-310 and TC-327 carry the amended text, judged at the lane's
  checkpoint sitting; TC-083 is unchanged.
- The IF-287 sentence is gone and `docs/interface-reference.md` is
  regenerated.
- `RESYNC_PACK.md` carries the entry.
- The commit bar is green on the lane tip (smoke tier and budget enforce);
  `check_trajectory.py --strict` exits 0.

## Scope answers

- **S1, independently landable deliverables.** One. The deletion, its tests,
  its contract text and its spine amendments land together; none stands
  alone. WI-852's other removal, the rollup branch-name refusal, touches
  different code (`review_brief.file_review`), a different SR chain (SR-235:
  LLR-313, TC-333) and waits on a different lane (WI-911), so it is its own
  row, filed beside this one. Their one shared surface is one test function
  in `tests/test_review_brief.py`, where this row changes one expected
  string and the other deletes a loop a few lines below: a trivial rebase.
  Either may land first.
- **S2, authority over a hold, an act or a gate.** No new authority. The
  reader already decides whether a review round counts at the merge gate and
  whether an adjudication verdict is accepted; this row narrows what it
  refuses, it gives no file new authority. No `## Trust` section.
- **S3, closed coverage.** The promise is over machine lines, an unbounded
  grammar, and it stays a construction: the review line is one exact form
  (deny everything else), and each adjudication line is its declared
  keyword, label and fields. The bound: lines written by the kit's reviewer
  and adjudicator routes. A line repeating a declared field is outside it,
  stated as residue.
- **S4, planning need: `none`.** The row only removes code, tests and
  text and adds no code path, which S4 exempts from the plan step (owner,
  2026-10-16, docs/decisions/coordinator-2026-10-16.toml#D-005). Round 1's `single` finding
  stands below as history.
- **S5, architectural delta.** None added: no state, no domain value, no
  new input, no new boundary. The reader's tuple loses an element.
- **S6, dependencies.** `needs = ["~WI-912"]`, soft: WI-912's verdict/act
  split reaches `kitlib/sitting.py` and SR-232's reader, so this row
  follows it to avoid a cross-lane edit of LLR-310 and the same module. No
  new third-party package, tool or service.
- **B1.** No deliverable hides in the Context; the residue line is
  Deliverable 4.
- **B2.** No split is minted on a work branch; the sibling row is filed on
  trunk.
- **B3.** No consumer re-derives a past decision.
- **B4.** No owner act or credential in the Done-when. The adjudication
  half was ruled at filing (D-017).

## Calls ruled at filing

- **The adjudication half** (coordinator-2026-10-15 D-017, as
  recommended): the repeated-field refusal is deleted for every consumer,
  adjudication lines included, partly reversing WI-870's Done-when. Review
  verdict lines lose nothing, since their exact-form comparison still
  refuses a repeated field; an adjudication line that repeats a field reads
  its last copy, which only a model writing a field twice reaches. The
  alternatives, cancelling this row or keeping the refusal for adjudication
  lines only, were not taken.

## Critique dispositions

Round 1 (Codex Sol, medium, 2026-10-16; CHANGES-REQUESTED, one finding):

- **S4, MAJOR: adopted.** The row was filed `planmode = "none"`, yet it
  promises behaviour over machine-line inputs. The front matter now reads
  `planmode = "single"`, and the S4 answer reads "The row promises
  behaviour over an input space (machine lines: exact-form review lines,
  adjudication lines, a repeated declared field), which the ruled S4
  criteria make `single`. The lane's plan passes the single-plan gate
  before its first build."
