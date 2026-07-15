# 085-DESIGN-CHECK — top-tier shared-failure page after the WI-165 review round (round 33)

The autonomous page-the-human path (PROCESS_OPTIONS.md "Unattended operation",
failure semantics): review round 33 (session 084, REVIEW-A of WI-165, built
session 083) came back **CHANGES-REQUESTED at the strong tier**, `escalate`
returned **page-human**, and `docs/gate-policy: autonomous` routed the loop to a
fresh **design-check session** — a different provider at the strong tier — to
rule grind-through vs. genuine redesign. This session (Claude Fable, strong; the
implementer was gpt-5.6-sol / OPENAI) is that ruling.

## What fired, exactly (traced, not assumed)

- Scoreboard round 33: `verdict=CHANGES-REQUESTED tier=strong tripwire=0
  contradiction=0` ([scoreboard.txt](scoreboard.txt)) — so neither the tripwire
  page nor the twice-contradiction page can have fired.
- The remaining page condition is `page_top_tier_fails` (default **2**,
  `agent_route.escalate`): strong-tier CHANGES-REQUESTED rounds in this
  coordinator run. Round **31** (session 080, REVIEW-A of WI-166:
  CHANGES-REQUESTED findings=3, tier=strong) and round **33** (session 084,
  REVIEW-A of WI-165: CHANGES-REQUESTED findings=2, tier=strong) reach the
  threshold. The page reason is the shared-failure hypothesis: "the spec is
  wrong, not the model".

## Ruling: **GRIND-THROUGH** (no redesign)

The shared-failure hypothesis is refuted by tracing the two fails to their
findings — they are **independent implementation defects in unrelated
deliverables**, each with a mechanical, reviewer-specified fix; neither indicts
a spec or a design:

1. **Round 31 / WI-166** ([080-REVIEW-A](080-REVIEW-A.md), BLOCKER): the build
   copied the meta-repo dogfood shim verbatim, so the scaffolded
   `dev-setup.template.cmd` passes `-Install` to a template ps1 that declares
   only `-Check/-Baseline/-Full` — a silent no-op on the consented install path.
   The spec ("double-click reports then offers install") was right; the copy
   missed the interface difference. Fix: a switch swap + the shape test that
   pinned the wrong token. **Verified still live in the tree** (template cmd
   lines 7/14/31/33 still say `-Install`; the ps1 `param()` block has no such
   switch).
2. **Round 33 / WI-165** ([084-REVIEW-A](084-REVIEW-A.md), MAJOR): the loop
   box + return-arrow CSS uses bare `.loop` selectors while the markup carries
   `class="loop"` on **both** the wrapper div and the inner `<ol class="pflow
   loop">` (`gen_trajectory.py` 2584-2585), so each loop renders as a nested
   double pill with two arrowheads. The reviewer states the layout design is
   "sound in isolation"; the defect is selector scoping (lines 2729/2733 and the
   ≤760px twins 2754/2759 — verified still live). Fix: scope the four rules to
   the wrapper (`div.loop`), plus the MINOR TC-056 tautology.

Two different WIs, two different failure modes (an interface-parity miss and a
CSS cascade miss), two mechanical fixes: no common spec defect, no design to
re-enter PROCESS.md §5 for. The artifacts stand as designed; they need their
**rework rounds**, which brings us to the real gap.

## The real gap the trace exposed: orphaned CHANGES-REQUESTED remediation

On CHANGES-REQUESTED the coordinator resets `run-phase` to BUILD — but the next
BUILD session takes its scope from `docs/next-wi`, which the *reviewed build
itself* had already advanced to the next backlog item. Net effect, observed in
this run: **080's BLOCKER was never reworked** (no commit after `57b199b`
touches `dev-setup.template.cmd` or `test_onboard_devsetup.py`; WI-166 sits
`done` in the registry with a defective deliverable; sessions 081/083 built
WI-162/WI-165 instead), and 084's findings were headed the same way (`next-wi`
already pointed at WI-167). This is the second occurrence of the dangling-round
failure — the 2026-07-14 remediation sitting (WI-139/WI-140) cleared three
rounds orphaned the same way.

Remediation, this sitting (the WI-139/WI-140 idiom — new registry rows, filed
ahead of new backlog):

- **WI-168** (`BuildTier=medium`, deliberate pin below the strong phase
  default — the fix is reviewer-specified and off-spine, matching WI-167's
  precedent): rework 080-REVIEW-A findings 1-3 (`-Install` → `-Baseline` in the
  template cmd + prompt/comment wording, flip the shape-test token, fix the
  bootstrap docstring inventory).
- **WI-169** (`BuildTier=strong` — WI-165's declared route was strong because
  its TC-056/SR-055 verification is spine-touching; a rework of the same scope
  inherits it, never a downgrade): rework 084-REVIEW-A findings (scope the four
  box/arrow rules to `div.loop`, then de-tautologize or soften the TC-056
  degree assertion).
- **WI-170** (`BuildTier=medium`): close the mechanism gap itself — carry a
  CHANGES-REQUESTED round's findings into the next BUILD scope (e.g. the
  coordinator writing a rework pointer that outranks `docs/next-wi`, or
  prepending the rework to it) so remediation no longer depends on a driver
  noticing dangling verdicts. Twice-dangling is a pattern, not luck.

Order: **WI-168 → WI-169 → WI-167 → WI-170**, then the greenlit
research-knowledge campaign (WI-152…157 + WI-164) — product-surface BLOCKER
first, the meta-dashboard MAJOR second, then the previously queued backlog.
No batch: WI-169 is spine-touching and each remediation deserves its own
review round.

RULING: GRIND-THROUGH — resume BUILD on WI-168 (then WI-169 → WI-167 → WI-170);
redesign not indicated.
