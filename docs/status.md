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

- **RESUME HERE — THE FRONTIER IS PAUSED (tracked `docs/work/pause`, armed
  2026-09-02) while the owner addresses the DISPATCH failure this run
  exposed, in a session of their own.** The failure: the scheduler claims
  several rows onto one exclusive lane and the worker assignment names them
  all, but the session banner names only the FIRST id, the worker follows the
  banner, and the remaining rows are left silently undone — caught only by
  the integrator refusing a lane whose claimed row has no outcome. The
  affected lane was finished by hand and merged; the loop is stopped and no
  worktree remains. The account is the log's 2026-09-02 close-out addendum.
  Since 2026-09-01 this run merged the construction-first reviewer clause,
  the approval-brief renderer defects, the wi508 partial-close conversion and
  its disposition adjudication, the snapshot copy scope, the adjudicator-only
  approval act, its amendment adjudication and spot-check, and the wi508
  spine reseal with its registry-bound correction. Routing since 2026-09-02:
  both Anthropic tiers pinned to `claude-opus-5` (effort high/strong,
  medium/medium) and all three codex rows at medium effort (owner
  directives). One reviewed deletion of the pause file resumes the generated
  frontier below.
  **For the owner's review:** delegated decisions 47–56 in
  [decisions-for-review-2026-08-31.md](decisions-for-review-2026-08-31.md)
  (52–56 are the evening session's: the hand merge + drawn rounds that
  landed the wi508 conversion, its record corrections, the adjudication's
  rework and by-hand close, the loop stopped on a C6 cycle, the re-arm);
  `OI-77` and `OI-78` are RULED (2026-09-01 evening: (a) and STAND; both
  cards had been hand-filled first because the automated mint writes only
  the question — the owner-prioritized rows that fix the mint's shape and
  the snapshot's copy scope head the generated frontier below); **ruled in
  session and filed (2026-09-01 evening):** the spine approval act — the
  Status flip and its anchoring snapshot — is the adjudicator's alone, on
  the serial trunk side, for whole-chain context and for concurrency; the
  executing row is queued behind the copy-scope row (a lane's merge refused
  on any flip, born-Approved row or snapshot write; a first-approval
  adjudication arm minted at merge; the amendment brief's stale
  "mechanical tool" line replaced) — the log's 2026-09-01 approval-act
  ruling entry is the record; the six MEANING rows awaiting the owner's signature on the
  `trace.py --approve modified` re-attestation brief (they render in
  [open-items.html](open-items.html)'s re-attestation section); the three
  owner-owed acts now filed as pending rows on that same surface —
  `OI-79` (the origin HELD ref), `OI-80` (`OI-72`'s "four Drafted" wording),
  `OI-81` (publication + the single-copy wi416 branch); `check_trajectory --strict` carries one
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
  - **OI-79** — The held wi508 branch was pushed to origin on 2026-08-31 as a backup under a -HELD- suffix OI-70 calls a bypass of the close flow. Its whole 44-commit range (ff29fef8..6ba27110) is now in trunk history via the 979c3e5f handback merge and its record is compiled into the log. Rename it back, delete it, or keep it as a tagged archive? push = "human" puts every answer out of the loop's reach.
  - **OI-80** — OI-72 (ruled 2026-08-31) reads the SR-163 cluster as 'the wi508 branch's four Drafted rows stay honest as-is'. LLR-203 and LLR-204 had been Approved on that branch since 2026-08-30 (580df781); only TC-199/TC-200 were Drafted. The phrase misled the WI-555 spec's arm 4 and the first WI-568 adjudication. Correct the ruled row's wording (a ruled row is the owner's text), or leave it with a pointer?
  - **OI-81** — Standing since 2026-08-31 and never filed: under push = "human" only the owner can merge contract_split (the integrator's trunk), dualplan-routing-fix, guardrails-fable-method and ConcurrencyTrainRewrite to main and push them; and the local branch wi416-parked-handback-contract is single-copy (on no remote) and should be deleted only after deciding it is not wanted. Rule the publication cadence and the wi416 disposal.
  - **OI-82** — WI-572 moved the first-approval act to the adjudicator and filtered the minted population by the human-approval dial at both adjudication ends (intake's mint and adjudicate_brief's composition, through agent_common.human_approves_spine). The plan's §2a table row 'Surfaces to the owner' says rows on a RELEASED rung no longer surface to the owner - but trace.py --approve modified still renders every Drafted chain, held or released, and calls human_approves_spine nowhere. Should the owner's approval brief narrow to the rungs the dial still HOLDS (so a sitting shows only what the owner actually owes a signature on), or keep rendering every Drafted chain (so the owner retains sight of what adjudicators are approving on their behalf)? WI-572 deliberately did not decide this: it changes what the owner sees at a sitting, which is the owner's call and not a side effect of moving who acts.
- **Ready frontier** _(dependency-ready WIs in build order — generated from the scheduler; a closed WI drops out automatically, so this list is never stale and never names a `done` id):_
  - **WI-578** — adjudicate: LLR-158, LLR-203, LLR-204
  - **WI-579** `P9` — The verdict carrier and the adjudication_review dial: gate over logged rounds, tree-bound…
  - **WI-580** `P8` — The worker and reviewer briefs: batch assignment block, one-turn close bar, rows under re…
  - **WI-581** `P6` — Lane-close hygiene: quarantine spares monotone and record paths, integrate.lock declared,…
  - **WI-570** `P5` — The typed open-item brief: an adjudicator-minted OI carries blast radius, options and a r…
  - **WI-557** `P3` — The delegated-decisions record: per-run TOML file, close-time obligation under the decisi…
  - **WI-536** `P2` — Agent-brief and scope: the knowledge-pack review's six byte-paid edits and two kit findin…
  - **WI-539** `P2` — Ship the complexity sensor: MAPPING row, template step, the opt-in layer, the deep-module…
  - **WI-556** `P2` — Spine-authoring doctrine: the children-coverage rule stated as trust-based prose (OI-72 r…
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
