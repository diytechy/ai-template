+++
id = "WI-823"
title = "TC-055's rubric binds T2 and T5 to their test rows, and the shot matrix covers every rendered tab"
workstream = "process"
sr_refs = ["SR-054"]
specref = "docs/reviews/wi-796-re-judge-tc-055-declared-trig/002-ADJUDICATE-5fb0fc7.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand by the wave-14 coordinator on 2026-10-04 from the independent
adjudication of WI-796's TC-055 re-judge (`docs/reviews/wi-796-re-judge-tc-055-declared-trig/002-ADJUDICATE-5fb0fc7.md`,
follow-ups). Two of six Codex Luna judges returned CHANGES-REQUESTED on findings the
adjudicator refuted, and both refutations trace to gaps in what the judges were
given:

- the rubric (`docs/rubrics/dashboard-usability.md`) keeps T2 and T5 live but, unlike
  T4 and T8, does not say which part a test already holds (T2's start-collapse core is
  LLR-099/TC-102; T5's ring-contrast core is LLR-105/TC-108), so a judge re-ruled a
  test-bound clause from source; T2 still cites SR-089, demoted in `0d5a9432`;
- `scripts/dashboard-shots/shoot.mjs` does not list the rendered Retired tab, so no
  judge sees it;
- the judges' prompt does not carry LLR-099's and LLR-105's scope lines.

The rubric is a declared input of TC-055, so this change fires its trigger and the
next merge checkpoint mints the re-judge, judged on the corrected rubric.

## Done-when

- The rubric's T2 and T5 entries each name the test-tier row that holds their core
  (LLR-099/TC-102; LLR-105/TC-108) and state what remains for the judge, in the form
  T4 and T8 already use; T2's SR-089 cite is replaced by LLR-099's rule.
- `shoot.mjs` shoots every tab the page renders, the Retired tab included, and the
  render-dashboard-critique skill's matrix description agrees.
- The judge brief the skill (or the rejudge brief) gives a critique judge includes the
  scope lines of the test-bound rows, so a judge does not re-rule a test-held clause.
- Test bar: the affected modules' tests plus the smoke tier at `-n 2`.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: none (this-repo rubric and tooling), unless the rejudge brief that
  ships changes, which then gets an entry anchored at a trunk commit.
