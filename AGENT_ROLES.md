# Agent roles & the coordinator loop — the dynamic layer

**Author:** Claude (Opus 4.8 / Fable 5), design note from a working session ·
**Date:** 2026-07-09 (last updated 2026-07-09) · **Branch:** `MultiRepoSupport` (not pushed) ·
**Status:** **RATIFIED (iterations 2–3, owner rulings 2026-07-09) — design settled,
nothing built.** The four open questions are answered (R1–R5) plus provider diversity
(R6); what remains is build sequencing (§ "Remaining open"). The floated 24-hour
coordinator self-reboot is **dropped** (owner-confirmed 2026-07-09 — R3's
by-construction resolution: every session is already a fresh context).

## Provenance

Split out of [`AXES_AND_WORKSTREAMS.md`](AXES_AND_WORKSTREAMS.md) (iteration 6, was its
"Operating the model" section). That note is the **static structure** — the registries
and how they relate (WHAT / WHY / HOW / WHEN; ratified at its iteration 9). **This**
note is the **dynamic layer** — *who does what, in what order, and how feedback flows*.
They are deliberately separate concerns; keeping them in one note conflated structure
with process.

A lot of this **already exists** in the kit and is *situated against it*, not
reinvented:

- [`agent_loop.py`](project-trajectory/scripts/agent_loop.py) — the unattended
  **coordinator** (headless resume, typed outcomes, parallel tracks). Stdlib Python —
  it holds a stall counter and a session number, **no LLM state**; sessions write
  `run-state`/`run-phase`, the loop only dispatches and reads evidence.
- `docs/run-phase` — the model-tier key (`PLAN | BUILD | …`), already mapped per-phase
  by `--model-map`.
- `docs/run-state` — the coordinator contract (`RUNNING | DONE | BLOCKED | NEEDS-HUMAN`).
- `docs/gate-policy` — `attended | single-ratify | autonomous`; the `autonomous` level
  already names "an independent fresh-context LLM reviewer's recorded verdict."
- The **integrator** role ([`tracks-README.template.md`](project-trajectory/tracks-README.template.md))
  — "a sync session, human or an agent leg run without `--track`"; the only writer of
  the root dispatcher; lands registry changes proposed by lanes.

---

## The pipeline

**coordinator → planner → implementer → reviewer(s) → coordinator**, looping through
the roadmap:

1. **Coordinator** runs the roadmap. It ingests feedback (harness results, reviewer
   findings, human input); when a gap is identified, a **work item** is created naming
   the affected component(s) + the gap (the iter-6/9 WI definition).
2. A **planner** builds the detailed plan, **updates the component (CMP) definition +
   knowledge pack**, researches if needed, and writes back into the WI what it added.
3. An **implementer** performs the work and confirms completion.
4. **Reviewer(s)** verify. Running the TCs is **not** the reviewer's value — `check.py`
   is mechanized, deterministic, and free; the harness pass is the reviewer's *entry
   ticket*. The reviewer's budget goes to **judgment on top of green**: method, risks,
   corner cases — and **scrutiny of the prose as well as the code** (TC wording, SR/LLR
   text, doc claims). *Review the claim, not just the code.* Empirical basis:
   [`THREAD_52_REVIEW.md`](THREAD_52_REVIEW.md) found eight verified findings (one
   HIGH) on a fully green branch.
5. The coordinator ingests the feedback, adjusts the roadmap, and dispatches the next
   session(s).

**The boxes may fuse; the seams may not.** Roles are *phases a session may occupy*,
not mandatory process boxes — a small WI legitimately fuses plan+build in one session.
Exactly **two independence seams are mandatory**:

1. **Reviewer ≠ implementer** — fresh context, no shared transcript, verdict recorded.
2. **Integrator = single writer** of the roadmap (`work-items.csv`) and the root
   dispatcher — no lane, planner, or reviewer ever writes those.

## Each role writes exactly one home (the tie to the static model)

| Role | Writes (its one home) | Existing kit anchor |
|---|---|---|
| **Coordinator (loop)** | session dispatch + typed outcomes (no judgment) | `agent_loop.py` |
| **Integrator (judgment)** | the **roadmap DAG** + root `status.md` (creates / reprioritises WIs from feedback) | tracks-README integrator |
| **Planner** | the **CMP definition + knowledge pack**; updates the WI with what it added | PLAN phase |
| **Implementer** | the **code** | BUILD phase |
| **Reviewer(s)** | **review evidence** — recorded verdict + findings | the gate / TCs |

## Rulings (iteration 2, owner 2026-07-09)

### R1 — Review policy: configurable count, split charters, prose in scope

- **`docs/review-policy`** — a one-line declared file in the existing policy idiom
  (`gate-policy` / `push-policy`; read by `read_declared`): reviewer count
  **`0 | 1 | 2`, default `1`**.
- **Floors above the dial:** a gate advance under `gate-policy: autonomous` always
  requires ≥1 fresh-context recorded verdict (already the gate-policy's own rule); a
  WI touching the spine/registries recommends `2`.
- **Two reviewers split *charters*, never duplicate coverage** (correlated models
  double-agree; independent charters catch uncorrelated misses — the owner has seen a
  double review expose items a single one missed): reviewer A = **method / risk /
  corner cases** (adversarial correctness); reviewer B = **process / trace / prose**
  (SSOT, traceability, TC text, SR/LLR wording, doc honesty).
- **Independence** = fresh context, no shared transcript with the implementer; input =
  the diff + the WI + the TCs; output = a **recorded verdict** (review doc / `log.md`).
- **Direct fix vs new WI** — decided by the WI's own definition (*affects + gap*): a
  finding **within** the current WI's declared affects-and-gap goes back to the
  implementer as a retry; anything else is **filed as a finding** and only the
  integrator turns it into a WI (the THREAD_52_REVIEW pattern: file, triage, never fix
  inline).

### R2 — Integrator mechanics: a distinguished session, not a loop sub-mode

- **No `agent_loop` sub-mode.** The loop stays dumb. The role vocabulary joins the
  phase vocabulary: **`run-phase ∈ {PLAN, BUILD, REVIEW, INTEGRATE}`** — the existing
  per-phase model map already keys tiers; sessions already set the phase.
- **Prompt selection: zero-code convention first** — the previous session sets
  `run-phase` and writes "Next action: review WI-x / integrate" in `status.md`; the
  next session picks up its role from the resume surface. A per-phase `--prompt-map`
  is added only if role-drift shows up in practice.
- **Who integrates is a function of `gate-policy`** (the seam the kit already has):
  `attended` → the human (they already ratify gates and triage reviews);
  `single-ratify` / `autonomous` → an `INTEGRATE`-phase agent session on the **root
  lane** (no `--track`), verdicts recorded in root `status.md` + `log.md`.
- **How an integrator session starts** (there is no daemon — every session starts the
  same way): under `attended`, the human works in the repo or boots
  `agent_loop --interactive`; otherwise a **root-lane loop** (`agent_loop.py` without
  `--track`) dispatches it like any session — on a cadence/cron, or after track lanes
  end (`run-state` DONE/BLOCKED). The per-worktree lock prevents overlap.

### R3 — Context is bounded by construction; the real risk is the resume surface

The owner's concern — "even the coordinator's context window will fill" — is resolved
by the existing architecture, not by a timer: the coordinator is **stdlib Python with
no LLM state**, and every LLM actor is a **bounded fresh session** that inherits state
from files (`status.md`, `log.md`, the registries), never from a conversation. The
"reboot" happens **between every session**; a 100-session run accumulates zero LLM
context. The floated 24-hour self-reboot is therefore unnecessary — **dropped
(owner-confirmed 2026-07-09)**.

The **real** analogue of the concern is `status.md` growth: every session inherits the
resume surface, so a bloated status file is the file-world version of a full context
window. Guard cheaply:

- The **integrator's charter includes pruning root `status.md` to one screen**
  (evidence belongs in `log.md` / iteration logs, which are append-only elsewhere).
- Optionally a **preflight size warning** when a lane's `status.md` exceeds a
  threshold (stdlib, warn-only) — a build call, see "Remaining open".
- Per-track surfaces already exist: each lane has its own `status.md`, so a track
  session never inherits another track's surface.

### R4 — Feedback → roadmap: file anywhere, write in one place

- **Anyone may *file* a finding** (no authority needed — it's evidence, the reviewer's
  one home; a failing TC is filed by the harness report).
- **Only the integrator writes the roadmap** — WI rows created/reprioritised in
  `work-items.csv`, the same single-writer discipline tracks-README imposes on the
  root dispatcher. WI creation is a *roadmap* change, not a gate act: it needs the
  integrator role, not gate authority.
- **Two escalations do hit gate authority:** (a) a finding that invalidates a
  previously attested claim (F1 is the live example — it impugns the ratified G3
  spine) surfaces to the gate authority, human under `attended`, never silently
  absorbed as a WI; (b) a WI whose gap requires new/changed SRs goes through the
  normal registry-change + re-attestation path.
- Full path: failing TC / reviewer finding / human input → **filed** as evidence →
  integrator **triages** → same affects-and-gap? implementer retry : **new WI row**
  (or escalation) → planner picks it up. Every arrow lands in exactly one role's home.

### R5 — Composition with parallel tracks: pipeline per lane, one shared integrator

- Each lane already has its own `run-state` / `run-phase` / `status.md` and its own
  coordinator loop (own lock, own worktree): **plan → build → review cycles entirely
  within a lane**, including that lane's reviewer sessions.
- The **integrator is repo-singular by construction** (runs without `--track`, sole
  writer of root `status.md` and the registries); `work-items.csv` is repo-singular,
  so **the roadmap DAG is automatically the shared apex** where cross-track feedback
  converges.
- A WI's **workstream** category *suggests* which lane runs it (workstream = grouping,
  track = execution lane — the ratified AXES distinction doing real work); the
  per-track **ID blocks** keep lane drafts from minting colliding ids on the way to
  the integrator.

### R6 — Provider diversity: neutral at every seam but one (verified in code)

Verified against `agent_loop.py` + the launchers (2026-07-09):

- **The invocation is a provider-neutral command template** — `AGENT_CMD` is any CLI
  with `{model}`/`{prompt}` placeholders, substituted per token, never through a shell.
  Nothing in the loop is Claude-specific; the meta-repo's launcher merely wires
  `claude`. (The loop itself was ported from a pre-Claude PowerShell coordinator.)
- **Outcome detection doesn't trust the provider:** truth = git (HEAD moved =
  COMMITTED) + `docs/run-state` (session-written). The JSON parse is best-effort by
  design — a plain-text CLI degrades cleanly (`ERROR` = nonzero exit without JSON,
  handled explicitly); `is_error`/usage/cost and the rate-limit reset wording are
  Claude Code niceties other CLIs simply won't populate.
- **The committed context is already agent-neutral** — the `AGENTS.md` standard
  (Thread 0) with thin `CLAUDE.md`/`GEMINI.md` stubs; any provider's session inherits
  the same guide.
- **The one gap: a run has ONE command template.** `AGENT_MODEL_MAP` varies only the
  `{model}` token inside it — per-phase *provider* switching isn't native (different
  providers are different binaries).

Two routes, both compatible with R1's dual review:

1. **Today, zero kit change — the dispatcher convention:** point `AGENT_CMD` at a thin
   project wrapper (`scripts/agent-dispatch.*`) that switches CLI on a **namespaced
   model token** (`claude:opus`, `gemini:2.5-pro`). The existing per-phase model map
   then routes providers for free, and `run-phase` keys are free-form so two reviewer
   phases just work: `AGENT_MODEL_MAP="BUILD=claude:opus,REVIEW-A=claude:opus,
   REVIEW-B=gemini:2.5-pro"`. Guardrails substring-matching survives namespaced tokens.
2. **Kit build call — `AGENT_CMD_MAP`:** a per-phase command-template map alongside the
   model map (same `parse_model_map` machinery, ~15 lines) makes provider routing
   first-class without a wrapper. Precedent: `AGENT_CMD_INTERACTIVE` is already a
   second template slot.

**Ruling (owner, 2026-07-09): cross-provider is the *recommended* `review-policy: 2`
configuration.** Two samples of one model have correlated blind spots; a different
model family is the less-correlated second draw — the entire point of paying for a
second review. The dispatcher convention is the now-answer; `AGENT_CMD_MAP` lands with
the review-policy wiring (dual review is its first consumer).

## Remaining open (build calls, not design gates)

1. **`docs/review-policy` build** — wire the declared file + the reviewer dispatch
   (`REVIEW-A`/`REVIEW-B` phases) + **`AGENT_CMD_MAP`** (first-class cross-provider
   routing, R6) into the loop/skills; exact vocabulary confirmed as `0|1|2`.
   Sequenced with the dynamic-layer build, after the AXES schema bundle.
2. **`status.md` size guard** — add the warn-only preflight threshold, or rely on the
   integrator-prunes charter alone? (Cheap either way.)
3. **`--prompt-map`** — deferred until the zero-code role convention shows drift.

## Cross-links

- [`AXES_AND_WORKSTREAMS.md`](AXES_AND_WORKSTREAMS.md) — the static structure this
  operates on (CMPs, the roadmap DAG, knowledge packs; ratified iteration 9).
- [`project-trajectory/scripts/agent_loop.py`](project-trajectory/scripts/agent_loop.py)
  · `docs/run-phase` · `docs/run-state` · `docs/gate-policy` · the integrator role in
  [`tracks-README.template.md`](project-trajectory/tracks-README.template.md).
- [`THREAD_52_REVIEW.md`](THREAD_52_REVIEW.md) — the review lineage these notes descend
  from, and R1's empirical basis (judgment findings on a green branch).
