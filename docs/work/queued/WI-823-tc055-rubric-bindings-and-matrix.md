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

The rubric is a declared input of TC-055, but its open re-judge row (WI-831)
suppresses a second mint while it is open. So WI-831 judges on the corrected
rubric: run it after this row lands.

Landing order (scope critique round 1, 2026-10-10; coordinator decision
D-018 in `docs/decisions/coordinator-2026-10-10.toml`, for the owner to
confirm or overrule): the three deliverables (the rubric's T2/T5 bindings,
the shot matrix with the skill's matrix text, and the judge brief's scope
lines) could land apart, but are kept in ONE lane on purpose. Each changes
what a TC-055 judge is given, and WI-831's re-judge must run on all three
together; landing them apart costs a render-and-judge cycle per landing.
Within the lane the rubric lands first, then the matrix, then the brief.
The judge brief's home is the `render-dashboard-critique` skill (a
this-repo skill, so no RESYNC entry); the shipped rejudge template is not
changed. The whole set lands before WI-831 runs.

## Trust

This row adds no authority and changes no reader's handling of a bad input. It
edits two files the TC-055 judgment depends on; each keeps the contract it
has (`project-trajectory/PROCESS.md` §3, "When a guard is owed").

**1. The rubric** `docs/rubrics/dashboard-usability.md`, a declared input
and the declared `rubric` of TC-055.
- **Producer:** this lane's builder, by a reviewed lane commit; nothing
  writes it at run time. A failed edit (tool error, timeout, a partial or
  truncated file) is a defect in the lane's diff, caught by the lane's
  review before landing; it is never written outside a commit.
- **Consumers and rulings** (all unchanged):
  - `project-trajectory/scripts/rejudge.py`, through
    `record_observation.inputs_digest`: the file is digested as declared;
    an absent file digests as `(absent)`, so a deletion or a malformed edit
    still moves the digest and makes the case due. Digesting judges
    nothing: a due case is a re-judge owed, never a pass.
  - The TC-055 judges (the `render-dashboard-critique` skill and recipes §8,
    `.claude/skills/coordinator-cycle/references/recipes.md`): a judge
    given an absent, unreadable or malformed rubric records no verdict; the
    re-judge stays open until the rubric is repaired, or the case goes to
    the owner. No verdict is recorded against a rubric it did not read.
  - `docs/requirements/low-level-requirements.toml` (LLR-055) and
    `docs/test/test-cases.toml` (TC-055) name it as text; they read nothing
    at run time.
- **Binds to:** the rubric's bytes at the commit the observation record
  is judged at (its inputs digest).

**2. The shot runner** `scripts/dashboard-shots/shoot.mjs`, the render
recipe that fixes which widths, themes and tabs a judge sees.
- **Producer:** this lane's builder, by a reviewed lane commit. At run
  time it writes PNGs to the gitignored `scripts/dashboard-shots/shots/`;
  a failed run (Playwright error, timeout, non-zero exit) or a tab the
  page renders but `TABS` omits is an incomplete matrix, which the runner
  already reports by name.
- **Consumers and rulings:**
  - `project-trajectory/scripts/check_trajectory.py`
    (`_render_surface_paths`, `_RENDER_RECIPE_REL`): the runner is an
    optional member of the watched render surface; an edit to it after the
    latest critique stales the perceptual stamp (unchanged). Its absence
    removes it from the watched surface by design (a downstream scaffold
    has no runner); this row does not delete it.
  - The `render-dashboard-critique` skill, recipes §8 and
    `scripts/dashboard-shots/README.md`: the operator stops on a failed run
    or an incomplete matrix and repairs or escalates; a judgment is never
    made on a smaller matrix than the runner declares. This row writes that
    sentence into the skill.
  - `tests/test_changed_selection.py` names the path for impact selection; a
    missing file there fails the test bar, not coverage.
- **Binds to:** the PNG set one run produced at the judged commit.

## Done-when

- The rubric's T2 and T5 entries each name the test-tier row that holds their core
  (LLR-099/TC-102; LLR-105/TC-108) and state what remains for the judge, in the form
  T4 and T8 already use; T2's SR-089 cite is replaced by LLR-099's rule.
- `shoot.mjs` shoots every tab the page renders, the Retired tab included, and the
  render-dashboard-critique skill's matrix description agrees and says a
  judgment is never made on a failed run or an incomplete matrix.
- The judge brief the skill (or the rejudge brief) gives a critique judge includes the
  scope lines of the test-bound rows, so a judge does not re-rule a test-held clause.
- Test bar: the affected modules' tests plus the smoke tier at `-n 2`.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: none (this-repo rubric and tooling), unless the rejudge brief that
  ships changes, which then gets an entry anchored at a trunk commit.
