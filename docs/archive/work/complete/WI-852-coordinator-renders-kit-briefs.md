+++
id = "WI-852"
title = "The coordinator renders its review and critique briefs from the kit's templates"
workstream = "process"
sr_refs = ["SR-146", "SR-154"]
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 5
needs = ["WI-860"]
+++

## Deliverable

A new `review_brief.py` renders, and never launches. `review` strictly fills the shipped reviewer template with one round's facts: the work item and its spec, a NARROW range (naming the findings file it answers) or a FULL-LANE range, the tests the reviewer runs, its scratch area and an optional review rubric; `critique` fills the critique template over a spec with a named rubric. An unfilled slot, a missing spec or an unreadable or empty named input refuses before anything is written. `file` writes a reviewer's verdict as the lane's next round file only when it is bound to the reviewed full commit and carries exactly one line whose keyword in any case is `VERDICT`, in exactly the form `VERDICT: <APPROVE|CHANGES-REQUESTED> findings=<digits>` with a matching count, for a lane the round reader reads back as its scope and whose directory is not the rollup generator's own in any letter case; the rollup directory's one declaration moves into `kitlib.verdict` (D-006). The reviewer template gains `{round_facts}` and `{head}`; the loop's brief fills them so it reads the same range as before. The repo's `kit-change-review` and `scope-critique` rubrics are added. Rows: SR-146 re-attested; SR-235, LLR-313, TC-333 approved (verdict 003); LLR-313 and TC-333 re-blessed at 004 and 007; IF-288 and IF-289 Drafted; SR-154 back at its anchor (D-003). The dispute sitting 006 ruled the third review's two findings FIX. Codex 6.1 Sol: the fresh full-lane review SOUND (`90c2f740`, at medium; `docs/reviews/wi-852-coordinator-renders-kit-briefs/sol-review-full.md`). Decisions: `docs/decisions/wi-852.toml` (D-001 to D-007).

## Context

Filed by hand on 2026-10-07 from the WI-841 retrospective (proposal §4(a),
§6 and §7.4; rows P5 and P8, folded together by the queue reconciliation §8.1).

The coordinator hand-writes each Sol brief from untracked templates in
`C:/Projects/ai-template.wt/coordinator-tools/`, not from the kit's
`prompts/reviewer.template.md`. That template asks the reviewer to name the
failure classes a change admits and hunt those first, and to say for a
guard-adding remedy why the defect cannot be made unrepresentable. The hand
brief asks for neither, so WI-841's findings arrived as instances and were
fixed as instances. The coordinator's `sol-review-*.md` files also use their
own format, so the generated verdict rollup sees no coordinator-era lane.

Render only: WI-801 owns launching (`ask.py`), so no coordinator launch script
enters the repository.

Knowledge packs (CMP-008), read before building: `docs/knowledge/agent-routing.md`,
`docs/knowledge/effort-tiering.md`, `docs/knowledge/prompt-image-token-efficiency.md`.

## Done-when

- The coordinator's narrow-round review, its full-lane review and the scope
  critique (ruling 2) are rendered through `prompts.py` from
  `prompts/reviewer.template.md` and `prompts/critique.template.md`, with the
  lane's facts as fill values. No brief is hand-composed.
- The scope critique carries ruling 2's two questions (each independently
  landable deliverable, and whether a file gains authority over a hold, an act
  or a gate) and a scope rubric under `docs/rubrics/` as its rubric input.
- A coordinator review is written as a kit round file
  (`docs/reviews/<scope>/NNN-REVIEW-A-<sha>.md`), so the verdict gate and
  `gen_verdict_rollup.py` read it.
- The coordinator-tools brief templates retire. What they carried that the kit
  templates lack (the scratch-root and basetemp rules, the regenerated-views
  note) moves into the fill values or the kit templates.
- WI-847's narrow-round render is this render.
- Tests:
  - a rendered review brief carries the failure-class and unrepresentable
    clauses;
  - an unfilled slot refuses;
  - a coordinator round file appears in the rollup.
- Its rows (SR-146's and SR-154's chains) are authored as one change set and
  judged in one combined sitting.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit if a shipped template
  changes.

## Adjudication follow-ups, answered in this lane

The first sitting (`docs/reviews/wi-852-coordinator-renders-kit-briefs/001-ADJUDICATE-d75fdc2.md`) blessed SR-146's amendment, did not bless SR-154's, and returned LLR-313 and TC-333 with one drafted follow-up. Under the owner's ruling of 2026-10-06 (a return is answered in the lane, not minted), it is answered here:

- SR-154's Requirement now states the attended recording obligation itself (an attended launcher's independent review verdict is recorded in the round-record form, or refused without a record), so its acceptance accepts its own requirement; the clause stays in SR-154, whose subject is review, not in SR-146, whose subject is prompts.
- Tests drive LLR-313's unverified clauses and IF-289's success code on a real git repository (`a10c0472`): a root not on a branch, a revision that is not a commit and a base that is not an ancestor each refuse through the command line; an empty test list, an empty or missing named input and a missing spec on the critique render refuse; a review render and a filing each exit 0 and write only the requested file. TC-333's Method, Expected and Evidence name them.
- The adjudicator's observation was confirmed: no reader treats a narrow round's `-narrow` tag as more than a name suffix, so the module docstring no longer claims otherwise.

The re-sit judges SR-146 (blessed, not yet anchored) and SR-154 for re-attestation, and LLR-313, IF-288, IF-289 and TC-333 for first approval, in one sitting.

The re-sit (`002-ADJUDICATE-24e989d.md`) blessed SR-146 again and returned SR-154, LLR-313 and TC-333: the widened SR-154 trigger bound the attended path to the unattended route's registry, consent and cross-family obligations. Answered by one decision per row (decisions D-003): SR-154 is restored byte-for-byte to its anchor; a new SR-235 states only the attended record-or-refuse obligation; LLR-313's parents are SR-146 and SR-235, TC-333 verifies SR-235 in place of SR-154, and the code's `Implements:` tags follow (render half SR-146, filing half SR-235). The next sitting judges SR-146 for re-attestation and SR-235, LLR-313 and TC-333 for first approval.
