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
  [handoff-2026-09-26-coordinator.md](handoff-2026-09-26-coordinator.md), then
  [handoff-2026-09-26.md](handoff-2026-09-26.md)'s
  read order. The redesign's remaining threads keep their context in
  [handoff-2026-09-06.md](handoff-2026-09-06.md). Recheck Git and the generated
  frontier before choosing work; earlier handoffs and sitting checklists are
  historical context.
- **Assumption tier — the build is under way:** the phase-6 chains are
  approved down to test cases
  ([spine map](plans/2026-09-25-assumption-tier-spine-map.md)), the needs by
  the owner's stand-in, and the build proceeds test-first, one builder
  worktree per item in the generated frontier's order, each handed the
  [builder brief](plans/2026-09-26-assumption-tier-builder-brief.md). The C1
  sitting commit and the reversal sweep follow it. The full unfiltered suite is
  owed before any phase close. The owner owes re-attestations and the
  reserved rulings (the handoff's list). The depth-0 mockup in
  `docs/plans/mockups/` still renders the old `kit` value.
- **Sister plan — one plan still owed:** every question in the
  [notes on spine, sessions and tests](plans/2026-09-23-owner-notes-spine-sessions-and-tests.md)
  §5 is ruled except S11, whose direction (one trunk commit per work item)
  needs its own plan before any ruling; design S9's reviewer-commit check with
  it. S7's session service proceeds and writes S8's adopted OTel schema; S6 is
  designed with the assumption tier before its C3; S14's flag-axis count
  proceeds, its duplicate-detection research first.
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

- **In stage:** **DevStg-Tests** (stage 6 of 8, test-case definition in work) (per-phase `1=DevStg-Impl;3=DevStg-Impl;4=DevStg-Impl;5=DevStg-Tests;6=DevStg-Impl`, derived current **phase=6**) — the rung this repo is IN, derived over its settled spine. [`derive_stage.py`](../project-trajectory/scripts/derive_stage.py) derives it, recorded in [`docs/stage`](stage).
- **Spine:** **SN=31 SR=112 LLR=239 TC=234** (17 drafts) · 187 seams · 4 components.
- **Open items** _(pending rows of [requirements/open-items.toml](requirements/open-items.toml); each item's blast radius, options and recommendation render in [open-items.html](open-items.html), the generated owner surface):_
  - **OI-82** — WI-572 moved the first-approval act to the adjudicator and filtered the minted population by the human-approval dial at both adjudication ends (intake's mint and adjudicate_brief's composition, through agent_common.human_approves_spine). The plan's §2a table row 'Surfaces to the owner' says rows on a RELEASED rung no longer surface to the owner - but trace.py --approve modified still renders every Drafted chain, held or released, and calls human_approves_spine nowhere. Should the owner's approval brief narrow to the rungs the dial still HOLDS (so a sitting shows only what the owner actually owes a signature on), or keep rendering every Drafted chain (so the owner retains sight of what adjudicators are approving on their behalf)? WI-572 deliberately did not decide this: it changes what the owner sees at a sitting, which is the owner's call and not a side effect of moving who acts.
  - **OI-86** — The phase-6 act (cbb6649f) approved SN-041..SN-044 on the owner's held rung by a Fable STAND-IN, not the owner; the need tier has no drift detector, so nothing else surfaces this. Three acts, D6/D20 first: keep or revert SN-042's narrowed acceptance, sign the two new needs SN-043/SN-044, and accept SN-041's first sentence being left to a later assumption row.
  - **OI-87** — SR-217 dates a test case's approval per test case, so a test case approved earlier and attached to a requirement AFTER its implementation landed inherits its earlier date and passes. Amend SR-217 (with LLR-257, TC-250) so a requirement's test case counts from the first commit where it reads approved AND names the requirement or one of its design rows? Rule with OI-86's SN-042 act.
  - **OI-88** — SR-212's interface-form gate runs at DevStg-Arch, because interfaces exist only from the Arch rung; the assumption-tier plan (AT §11) says its Boundary half 'also runs per reached boundary IF'. Confirm the deviation (the check waits for interfaces), or ask for a Boundary-rung arm?
  - **OI-89** — SR-187 (a crossing names its system of interest: operation or delivery) is derived from SN-043, not from a need that asks for two systems; SN-037 speaks of one system. Keep it as a derived requirement argued in its rationale, or state the two-frame orientation as an owner need (a design constraint)?
  - **OI-90** — SR-198 marks an observation test case by its Automated cell alone (No), which admits manual and demonstration cases to lifetimes, declared inputs and checkpoint re-judging: a wider class than the inspection, critique and attestation the S6 ruling had in mind. Confirm the Automated-cell marker, or narrow the class?
  - **OI-91** — Approved SR-178 says a recorded artifact whose text moved from its acceptance copy is reported, 'stakeholder needs included'; the need tier has no drift detector (OI-85 deferred it). Fund the detector (add the need tier to the snapshot comparison and the re-attestation brief) or amend SR-178 to exclude needs?
  - **OI-92** — The per-commit smoke tier is budgeted at 60 s (measured 27 s on a 24-core box) and runs 188 s quiet and up to 957 s loaded on this 4-core, 8-thread box, so every commit records the seconds FAIL rather than re-stamping it. Keep recording, re-tier to fit this box, or make the budget name the machine it is measured on?
  - **OI-93** — Approved TC-215 puts an out-of-vocabulary stakeholder status in the always-on integrity class and approved LLR-216 puts it in the frame class, so the build (WI-628) reports it twice. Amend one: keep the integrity report (a schema fact, like every other status vocabulary) and drop LLR-216's status clause?
  - **OI-94** — Approved SR-211 reports every boundary interface that names no bridging assumption and records no coincidence, with no 'until adopted' clause, so this repository gains 43 advisories and an adopter that never uses the tier gets one per boundary interface forever; the requirement side (SR-193/SR-194) stays silent until a real assumption row exists. Keep it ungated, or amend SR-211 to the same vacuity?
- **Ready frontier** _(dependency-ready WIs in build order — generated from the scheduler; a closed WI drops out automatically, so this list is never stale and never names a `done` id):_
  - **WI-582** `P4` — The WI-552 residual sweep: the schedule-trace seam's test case, the validate docstring, t…
  - **WI-643** `P3` — The C1 sitting commit: write the redrawn frame, the stakeholder rows and the needs' cells…
  - **WI-626** `P2` — Make the shared-spec warning compare section anchors, so distinct sections of one plan ar…
  - **WI-602** — spot-check the clean close of WI-580
  - **WI-604** — adjudicate: LLR-210, TC-208
  - **WI-581** `P6` — Lane-close hygiene: quarantine spares monotone and record paths, integrate.lock declared
  - **WI-570** `P5` — The typed open-item brief: an adjudicator-minted OI carries blast radius, options and a r…
  - **WI-634** `P5` — Build the assumption gate's boundary, release and architecture steps (SR-205, SR-206, SR-…
  - **WI-638** `P5` — Build checkpoint re-judging of observation tests at merge and release (SR-215)
  - **WI-608** `P4` — Stop a later session rewriting an earlier review round's verdict file: reproduce first, t…
  - **WI-633** `P4` — Build the assumption approval brief, the stage's tier reading and the per-need view (SR-2…
  - **WI-620** `P3` — One session service for every model call (act, keep, record), writing the adopted OTel us…
  - _(+19 more ready — see the dashboard)_
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
