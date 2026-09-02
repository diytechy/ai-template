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

- **RESUME HERE — THE FRONTIER IS PAUSED (tracked `docs/work/pause`,
  re-armed by owner direction at the 2026-09-01 evening session's end;
  decision 56).** That session merged four rows (the construction-first
  reviewer clause, the approval-brief renderer defects, the wi508
  partial-close conversion and its disposition adjudication) and left one
  new successor queued behind a pending open item; its account is the log's
  2026-09-01 supervised-evening entry, and one reviewed deletion of the pause
  file resumes the generated frontier below. All three codex rows in
  `docs/agents.toml` now pin reasoning effort to medium (owner directive).
  **For the owner's review:** delegated decisions 47–56 in
  [decisions-for-review-2026-08-31.md](decisions-for-review-2026-08-31.md)
  (52–56 are the evening session's: the hand merge + drawn rounds that
  landed the wi508 conversion, its record corrections, the adjudication's
  rework and by-hand close, the loop stopped on a C6 cycle, the re-arm);
  **`OI-78`** — the off-spine approval baseline absorbed by the wi508
  handback merge (132 rows now read as approved unseen): STAND or
  REVIEW-THEN-STAND, the brief on the successor row's spec, recommendation
  REVIEW-THEN-STAND; `OI-77` (the intake regex DOTALL ruling) — both cards
  now carry their full brief (hand-filled at the owner's direction; the
  automated mint had written only the question, and the owner-prioritized
  row that makes a thin card unrepresentable heads the generated frontier
  below); the six MEANING rows awaiting the owner's signature on the
  `trace.py --approve modified` re-attestation brief; the origin ref
  `wi508-architectural-remap-HELD-for-owner-verdict` to rename or delete now
  its range is in trunk history; `OI-72`'s "four Drafted rows" wording (two
  were Approved when it was written); `check_trajectory --strict` carries one
  KNOWN queued ERROR (the schedule→trace seam; its row is queued, and it does
  not red the non-strict bar); nine unfiled kit findings listed in the
  evening log entry (a lane cut before a trunk snapshot move cannot refresh;
  the thin `open_item` mint; the C6 re-adjudication cycle; the audit flagging
  intake's own OI mint); and the standing 2026-08-31 items below.
  Hand-authored prose here names no queued id (the claim-refusal rule); a
  fresh reader starts at [handoff-2026-08-31.md](handoff-2026-08-31.md) —
  **read its banner: the 2026-09-01 runs superseded parts of it** — and the
  log.
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
  "ordinal `0`–`4`" approval dial.
- **Conventions:** [specs/README.md](specs/README.md) · [rubrics/README.md](rubrics/README.md) · partial closes [handbacks/](handbacks/README.md).

## Current State

<!-- BEGIN GENERATED STATUS -->
_GENERATED by `python project-trajectory/scripts/gen_trajectory.py --status` — do not hand-edit; cite the spine registries + `docs/stage`, not this rendering (the forward-only intent below is hand-authored)._

- **In stage:** **DevStg-LLReqs** (stage 5 of 8, LLR definition in work) (per-phase `1=DevStg-Impl;3=DevStg-Impl;4=DevStg-Impl;5=DevStg-LLReqs`, derived current **phase=5**) — the rung this repo is IN, derived over its settled spine. [`derive_stage.py`](../project-trajectory/scripts/derive_stage.py) derives it, recorded in [`docs/stage`](stage).
- **Spine:** **SN=27 SR=76 LLR=188 TC=187** (9 drafts) · 162 seams · 4 components.
- **Open items** _(pending rows of [requirements/open-items.toml](requirements/open-items.toml); each item's blast radius, options and recommendation render in [open-items.html](open-items.html), the generated owner surface):_
  - **OI-78** — Does trunk's docs/archive/last_approved/ baseline for interfaces.toml, external.toml, and components.toml STAND as-is at the wi508 branch's 2026-08-30 bytes — which absorbed interfaces.toml's 132 changed / 30 added / 3 removed rows (OI-64, OI-65, OI-67, WI-522, WI-528, WI-530, WI-531, WI-533, WI-534, WI-553), components.toml's 1 changed row (WI-520) and one external.toml comment correction — and is resealed at the successor's approval commit, or does the owner REVIEW that diff first (git diff 6d3d9db4 551d1b2c -- docs/archive/last_approved/docs/requirements/) and amend any rejected row LIVE, which returns it to the re-attestation brief, before the reseal? (A byte-level restore of the old snapshot is unavailable: the mirror invariant reds a snapshot that is not a copy of live at its writing commit.)
- **Ready frontier** _(dependency-ready WIs in build order — generated from the scheduler; a closed WI drops out automatically, so this list is never stale and never names a `done` id):_
  - **WI-570** `P5` — The typed open-item brief: an adjudicator-minted OI carries blast radius, options and a r…
  - **WI-571** `P5` — The snapshot copies only what the act authorises: copy_live scoped to the flipped registr…
  - **WI-557** `P3` — The delegated-decisions record: per-run TOML file, close-time obligation under the decisi…
  - **WI-560** `P3` — One freshness definition for verdicts, and the approval brief's two staleness traps (OI-7…
  - **WI-561** `P3` — The quarantine spares what is monotone or record: the id watermark, docs/reviews, docs/lo…
  - **WI-562** `P3` — Unload residue and scratch: integrate.lock declared, the worker told where scratch belong…
  - **WI-565** `P3` — Rule and apply the intake._SPEC_NEEDS_RE no-DOTALL residual, and clear the two cosmetic W…
  - **WI-551** `P2` — Re-land the adjudicator session-retention layer from its preserved patch, inert at dial 0…
  - **WI-536** `P2` — Agent-brief and scope: the knowledge-pack review's six byte-paid edits and two kit findin…
  - **WI-539** `P2` — Ship the complexity sensor: MAPPING row, template step, the opt-in layer, the deep-module…
  - **WI-545** `P2` — The decomposition debt owner (cont.): three wide modules, check_trajectory's remaining fu…
  - **WI-556** `P2` — Spine-authoring doctrine: the children-coverage rule stated as trust-based prose (OI-72 r…
  - _(+3 more ready — see the dashboard)_
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
