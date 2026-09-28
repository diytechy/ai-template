<!--
Contracts: IF-163 — the interface seam this file declares (process.md §8; row of
record in requirements/interfaces.toml).

Contract IF-163: the forward-only blackboard's HAND-AUTHORED bytes — everything
    outside the GENERATED STATUS marker pair — read as data by the kit's checks
    and by a resuming session; the block between the markers is its writer's
    own row. Markdown with `##` sections: `## Current State` is the section a
    stopping coordinator excerpts into its exit banner (the generated block
    rides inside that excerpt as the writer's bytes). Only what must happen
    NEXT belongs here — what already happened lives in log.md — so a work-item
    id recorded closed must not appear in the hand-authored prose, and a claim
    naming one there is refused; inside the generated block that rule stands
    down, because the generated frontier legitimately names queued ids.
-->

# Meta-Repo Status — Blackboard

The **working surface** for developing the kit itself. **Forward-only**, held to
the declared S-1 budget (`docs/status-lint`; raised 2026-08-31 to carry the
supervisor prompt at the owner's request). Backward-looking homes:
[log.md](log.md) (sessions, verdicts, **Decisions**), [open-items.html](open-items.html)
(the generated **Open items** owner surface), [docs/work/](work/) (the WI registry —
status = directory; terminal rows under [archive/work/](archive/work/)),
[archive/](archive/README.md), and the folder map [docs/README.md](README.md).

- **RESUME HERE:** start with the coordinator's
  [handoff-2026-09-27-wave4-coordinator.md](handoff-2026-09-27-wave4-coordinator.md).
  The queue is consolidated (50 open to 13) and seven groups have landed. Its
  first jobs: re-measure the smoke tier quietly, then ONE spine-acts batch
  (one adjudicator, one act) over every row the landed groups amended or
  drafted, which the handoff lists. Then the consolidation machinery item and
  the remaining groups, one builder each. File new work into an open group's
  Context before minting a row. The redesign's remaining threads keep their
  context in [handoff-2026-09-06.md](handoff-2026-09-06.md). Recheck Git and
  the generated frontier before choosing work; earlier handoffs are
  historical context.
- **Assumption tier — the build has landed:** the C1 sitting (the redrawn
  frame, the stakeholders, the dial at DevStg-Boundary), checkpoint
  re-judging of observation tests, and the assumption gate's four steps
  (behind `[checks] assumption_gate = false`), with SR-212's Boundary arm per
  OI-88 (c). Their amended rows await the spine-acts batch. C2's content is
  next in its group, C3 (evidence) and C4 (activation) after it. The full
  unfiltered suite is owed before any phase close.
- **Sister plan — one plan still owed:** every question in the
  [notes on spine, sessions and tests](plans/2026-09-23-owner-notes-spine-sessions-and-tests.md)
  §5 is ruled except S11, whose direction (one trunk commit per work item)
  needs its own plan before any ruling; design S9's reviewer-commit check with
  it. S7's session service proceeds and writes S8's adopted OTel schema; S6 is
  designed with the assumption tier before its C3; S14's flag-axis count has
  landed, and its duplicate-detection research is still owed.
- **Next implementation:** resolve the existing SR-161 per-decomposition
  perspective-record gap and complete TC-211's normal sample. Follow the
  existing artifact adjudication route for the Drafted amendments; passing an
  Inspection does not approve its requirement. Keep the scope proportional to
  the missing obligation.
- **Control launch:** retain the tracked `docs/work/pause` while preparing
  route-complete spending bounds, including in-flight drain, against the
  [settled control ruling](ai-template-redesign-2026-09-05-codex/CONTROL-DECISION.md#owner-ruling-2026-09-06).
  Revalidate the [preflight](ai-template-redesign-2026-09-05-codex/CONTROL-PREFLIGHT.md)
  at the proposed frozen launch commit, then obtain the ruling's owner-reviewed
  pause deletion. Replacement packages follow the control's evidence decision.
- **Standing owner acts the loop will not make:** merge-to-main + push for
  `dualplan-routing-fix`, `guardrails-fable-method`, `ConcurrencyTrainRewrite`
  and this branch (`push = "human"`). `wi416-parked-handback-contract` is still
  single-copy — delete only after deciding it is not wanted. The held wi508
  branch is on origin; the queued wi508-partial-close row is the only
  sanctioned act on it (`OI-71`).
- **Standing constraints:** the depth-0 frame is **LOCKED and APPROVED** (4
  entities · 4 crossings · 3 relationships, watermark-held); owner-owed, not
  re-raised: `OI-49` (b)'s exception reads
  ([plans/2026-08-22-interface-exception-dossier.md](plans/2026-08-22-interface-exception-dossier.md)),
  `OI-61` (c) deferred, and the wording round's two banked findings
  ([reviews/2026-08-24-draft-wording-round/RESUME.md](reviews/2026-08-24-draft-wording-round/RESUME.md)).
- **Unfiled follow-ups** (topics, no ids): the stage-ladder program's deferred
  codex round; the SN-036 coverage record (re-derive — basis reads
  `uncovered=0`); the archived [2026-08-01 handoff §6](archive/history/handoff-2026-08-01.md)
  findings; the [spine-restructure-2026-08-08.md](spine-restructure-2026-08-08.md)
  residues (§7 items 2/4/5 need a destination); PROCESS.md §4's stale
  "ordinal `0`–`4`" approval dial; **owner intake 2026-09-22:** the self-test
  suite should fail fast when its dev toolchain is missing, and name the run
  menu's setup action as the fix. Today a missing pytest-xdist dies on
  `unrecognized arguments: -n`. This depends on the root launchers SN-034/SN-035
  require, which do not exist yet, and needs stepping through as a requirement
  before it is built.
- **Conventions:** [specs/README.md](specs/README.md) · [rubrics/README.md](rubrics/README.md) · partial closes [handbacks/](handbacks/README.md).

## Current State

<!-- BEGIN GENERATED STATUS -->
_GENERATED by `python project-trajectory/scripts/gen_trajectory.py --status` — do not hand-edit; cite the spine registries + `docs/stage`, not this rendering (the forward-only intent below is hand-authored)._

- **In stage:** **DevStg-LLReqs** (stage 5 of 8, LLR definition in work) (per-phase `1=DevStg-Impl;3=DevStg-Impl;4=DevStg-Impl;5=DevStg-LLReqs;6=DevStg-Impl`, derived current **phase=6**) — the rung this repo is IN, derived over its settled spine. [`derive_stage.py`](../project-trajectory/scripts/derive_stage.py) derives it, recorded in [`docs/stage`](stage).
- **Spine:** **SN=31 SR=114 LLR=254 TC=254** (47 drafts) · 201 seams · 4 components.
- **Ready frontier** _(dependency-ready WIs in build order — generated from the scheduler; a closed WI drops out automatically, so this list is never stale and never names a `done` id):_
  - **WI-682** — adjudicate: LLR-210, TC-208
  - **WI-683** — adjudicate: LLR-264, LLR-265, SR-220, TC-260, TC-261
  - **WI-684** — re-judge TC-036: no result recorded [sha256:2f2f30dfba87] at merge 77fb093
  - **WI-688** — re-judge TC-211: no result recorded [sha256:aa064ee9542c] at merge 77fb093
  - **WI-690** — adjudicate: LLR-203, LLR-233
  - **WI-691** — adjudicate: LLR-205, LLR-206, LLR-262, LLR-274, LLR-275, LLR-276, TC-201, TC-203, TC-204,…
  - **WI-692** — spot-check the clean close of WI-616
  - **WI-693** — adjudicate: LLR-158, LLR-173, LLR-245, SR-178, TC-167, TC-240
  - **WI-694** — adjudicate: LLR-271, LLR-272, LLR-273, LLR-277, LLR-278, TC-269, TC-270, TC-271, TC-272,…
  - **WI-695** — adjudicate: SR-006, SR-007, SR-009, SR-011, SR-015, SR-022, SR-024, SR-026, SR-027, SR-02…
  - **WI-696** — adjudicate: SR-220, TC-279
  - **WI-697** — re-judge TC-279: no result recorded [sha256:cf0861ee8f1d] at merge bcf1e9a
  - _(+6 more ready — see the dashboard)_
<!-- END GENERATED STATUS -->

- **Bar (per commit)** and the **standing rules** (claim refusal on prose ids,
  never sanction a check to green a step, line-ending hygiene, claiming through
  the integrator): the `session-protocol` skill §2–§3. Run
  `check_trajectory.py --strict` unfiltered before claiming anything done;
  route a critique dispatch by PROVIDER, probing first.
- **Process (kit source):** [PROCESS.md](../project-trajectory/PROCESS.md) ·
  [PROCESS_OPTIONS.md](../project-trajectory/PROCESS_OPTIONS.md) · working rules
  [CLAUDE.md](../CLAUDE.md) + the `session-protocol` skill · lock items
  [repo-lock.md](repo-lock.md) · external (not this repo's work): guardrails
  content in `TheColliny/FableClaudeMDForOpus`.

## Scope

- **Goal:** keep the kit **maintainable and trustworthy** — the `PROJECT-VISION:`
  tag opening [README.md](../README.md) is canonical.
- **Supported platforms:** Windows + POSIX; kit scripts stdlib-only, Python 3.11+.
- **Non-goals (self-application boundary):** no product **launch** — the kit's
  "product" is `project-trajectory/` + `tests/`; an actions-menu launcher is in
  scope, a `run.*` product launcher is not. No scaffolded `docs/process.md` (the
  masters live in `project-trajectory/`).
