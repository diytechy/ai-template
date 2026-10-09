+++
id = "WI-860"
title = "A review's scope excludes defects that need a compromised host"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 8
+++

## Deliverable

PROCESS.md §6 gains the bold-lead paragraph "Review threat model", the one home of the owner's 2026-10-08 ruling: a review hunts defects in a normal working environment (content agents write into the repository, supported configurations, regressions of supported behavior); a finding whose reproduction needs the host itself compromised or contrived is out of scope, dismissed in one recorded line by whoever rules the finding, in the response to the review verdict (and in the delegated-decisions record too, when the run keeps one), and never answered with code. The shipped reviewer brief cites that paragraph and restates none of its examples; `tests/test_prompts.py` pins the paragraph's ten clauses, the citation in each finding-judging brief (`FINDING_JUDGING_BRIEFS`, the reviewer brief today) and the absence of the examples from every shipped prompt. Rows: SR-233, LLR-311 and TC-332 approved (verdict 004, after three returns answered in the lane, verdicts 001-003). Codex 6.1 Sol: the fresh full-lane review SOUND (`379ed914`, at medium; `docs/reviews/wi-860-review-threat-model/sol-review-full.md`). Decisions: `docs/decisions/wi-860.toml` (D-001).

## Context

Filed by hand by the coordinator on 2026-10-08 from the owner's ruling
([log.d/2026-10-08-owner-ruling-review-threat-model.md](../../../log.d/2026-10-08-owner-ruling-review-threat-model.md)).
WI-846's lane drew six Codex Sol rounds; the later ones chased reproductions
that need a fake runner binary or a cwd-dependent shim. The kit already says
"the threat model is bugs and fail-open, not malice" for forge mode
(PROCESS_OPTIONS.md), but no rule bounds what a code review may demand, so a
reviewer can keep finding contrived cases and a coordinator keeps building
against them.

## Done-when

- PROCESS.md §6 states the review threat model in one paragraph, its one
  home: in scope are defects in a normal working environment, content agents
  write into the repository (the gates exist to check it), supported
  configurations and regressions of supported behaviour; out of scope is any
  finding whose reproduction needs the host itself compromised or contrived
  (a fake or hostile binary, a shim whose output depends on cwd, the
  environment or PATH changed by another process mid-call, a tampered OS or
  tool), which is dismissed in one recorded line and never answered with
  code.
- The kit's reviewer template and every adjudication brief template that
  judges a finding link to that paragraph rather than restating it; the
  byte-budget skill's rows are re-stamped.
- The spine carries the obligation (Terra authors it; an independent
  adjudicator judges it in the lane).
- Review bar: A (one cross-family REVIEW-A).

## Adjudication follow-ups, answered in this lane

The first-approval sitting (`docs/reviews/wi-860-review-threat-model/001-ADJUDICATE-784e047.md`) returned SR-233, LLR-311 and TC-332 with one drafted follow-up. Under the owner's ruling of 2026-10-06 (a return is answered in the lane, not minted), it is answered here:

- SR-233 drops the coincident claim SN-006 does not carry, and its acceptance criteria name the ruling party and the lane's delegated-decisions record and bind every delivered brief that judges a review finding, not only the reviewer brief.
- LLR-311 names the home by its real form, the §6 bold-lead paragraph "Review threat model", and follows SR-233's widened scope.
- The pinning test asserts the definition's content (the in-scope classes, the exclusion, the one-recorded-line dismissal, "never answered with code") and the absence of all four boundary examples from every shipped prompt (`5c170072`); TC-332's Method, Expected and Evidence state exactly that.

The re-sit judges all three again for first approval.

The first-approval re-sit (`002-ADJUDICATE-7f72102.md`) accepted those answers and returned all three rows on one clause: the dismissal had no record home that always exists, since the delegated-decisions record is dial-gated and ships off. Answered the same way: §6 now says the dismissal is recorded in one line by whoever rules the finding, in the response to the review verdict, and in the delegated-decisions record too when the run keeps one; the test pins both clauses and asserts every brief in its enumerated finding-judging set (the reviewer brief today) cites §6 (`0928481f`). SR-233, LLR-311 and TC-332 state exactly that. The next re-sit judges all three for first approval.

The second re-sit (`003-ADJUDICATE-ba1dc19.md`) judged SR-233 and LLR-311 blessable as written and returned all three rows on one clause: the test did not assert the delegated-decisions half of the recording clause, so deleting it from §6 left the test green. Answered the same way: the test now asserts `delegated-decisions record too, when the run keeps one` and fails when that clause is removed (`f43007a7`), and TC-332's Method and Expected name it. SR-233 and LLR-311 are unchanged. The next re-sit judges all three for first approval.
