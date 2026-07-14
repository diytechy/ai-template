# Open items — owner decision briefs

The **single owner-review surface**: one section per pending decision, with the
context needed to rule — what's being decided, blast radius, options with
pros/cons, and the driver's recommendation. [status.md](status.md) carries only
the one-line form of each; the DAG rows live in
[work-items.csv](requirements/work-items.csv). **A section lives here only
while the decision is pending** — the ruling appends to [log.md](log.md)'s
Decisions log and the section is deleted. (Format:
[specs/open-items-surface.md](specs/open-items-surface.md).)

_The 2026-07-13 sitting ruled OI-1 (G3 re-attestation — ratified), OI-2
(single-ratify enablement — accepted), OI-5 (WI-098 — thin) and OI-6 (WI-103 —
budget + index). The 2026-07-14 sitting ratified OI-8 (the `[v3]-[g2]`
dashboard-ux batch) and OI-9 (the research-knowledge design spec, as revised) —
records in the log's Decisions. OI-3 (corrected against git), OI-4, OI-7, and
OI-11 (session-038 REVIEW-A disposition) remain open._

---

## OI-3 — Push / sync decision

- **Decision:** whether to push the pending local commits on
  `derived-gate-model` (and, separately and later, whether/when to integrate
  the branch into `main`).
- **Git-checked facts (2026-07-13; re-verify at read time — an open-item claim
  about git state must come from git, not memory):**
  - remote `origin` exists (`github.com:diytechy/ai-template`);
  - `derived-gate-model` tracks `origin/derived-gate-model`, **ahead 9** at
    check (10 with the ratification commit that lands this brief) —
    verify: `git fetch --prune && git branch -vv`;
  - `MultiRepoSupport` is **in sync** with its remote;
  - `main` is 340 commits behind this branch
    (`git rev-list --count main..derived-gate-model`) — the eventual
    integration question, **not** part of the routine push.
  - _(The earlier "local-only, ~48 commits" claim was stale and wrong —
    corrected at the 2026-07-13 sitting.)_
- **Blast radius:** durability of ~10 commits of ratification + campaign work
  (one disk holds them until pushed). The branch is already public-remote
  tracked, so pushing adds no new exposure.
- **Options:** authorize the push (`push-policy` = `human`: you push, or
  explicitly authorize the agent once) · hold.
- **Recommendation:** push — the branch is already tracked upstream; the
  unpushed commits are pure durability risk. The `main` integration is a
  separate, later sitting.

## OI-4 — WI-097: LICENSE decision

- **Decision:** which license, and whether the kit is headed public (the
  deep-review-b H3 finding; WI row: [work-items.csv](requirements/work-items.csv)).
- **Blast radius:** the legal terms of every downstream adoption — the kit's
  whole model is copy-in, so the license travels with every scaffold.
- **Options:** **MIT** (max adoption, simplest copy-in story) · **Apache-2.0**
  (adds an explicit patent grant; slightly heavier notice obligations) · **stay
  private / no license** (default all-rights-reserved; blocks outside use).
- **Recommendation:** none recorded — this needs the owner's public/private
  intent first.

## OI-7 — WI-123: review-cadence dial

- **Decision:** campaign-close 2× adversarial review instead of per-slice
  (owner-raised 2026-07-12; spec: [specs/WI-123.md](specs/WI-123.md)).
- **Blast radius:** the unattended loop's defect-catch latency — per-slice
  reviews are the escalation sensor the medium-BUILD relax leans on.
- **Options:** adopt campaign-close cadence now · keep per-slice · wait for
  evidence.
- **Recommendation (recorded):** rule only after ≥ 2 campaigns of medium-BUILD
  evidence.

## OI-11 — Review-038 finding against WI-143 / SR-056 (containment arrow)

- **Decision:** disposition the session-038 REVIEW-A **[MAJOR]** finding — the
  `cedge` containment arrow is emitted once per descendable block as a short
  shaft inside the parent (terminating at no child), which the reviewer reads as
  violating SR-056's "one horizontal parent-to-child arrow per containment edge."
- **Finding verified against the code:** the drill view is a **layer-swap** model
  (`gen_trajectory.py` §"SR-051 rev": a container carries `data-descend` → a
  *child layer id*; descending replaces the layer). A parent and its children are
  never co-rendered in one SVG, so the reviewer's proposed fix (an arrow ending
  "at the corresponding child"; a fixture with "multiple children" in one layer)
  is architecturally inapplicable — it presupposes a co-rendered tree, not the
  ratified drill/descend render. In the drill model each container has exactly
  one containment edge visible in its layer ("descend into my decomposition"),
  and the code emits exactly one arrow for it — satisfying SR-056's Done-when
  ("Each containment edge renders exactly one parent-to-child arrow").
- **Blast radius:** none to correctness — a spec-interpretation call. The residual
  is whether a 9px arrow into empty space *reads* as a containment cue, which
  SR-056 explicitly routes to the SR-052/053/054 Critique rows ("the Critique
  rows judge the residual look-and-feel").
- **Options:** (a) accept the interpretation — no WI-143 correctness fix; fold
  the arrow-legibility question into WI-144's critique scope · (b) treat it as a
  bug and redesign the decomposition render to co-render parent + children (a new
  SR; large blast radius — reverses the ratified drill/layer-swap model).
- **Recommendation:** (a). WI-143 keeps its Verified status (the OI-10 precedent:
  a REVIEW-A finding does not un-Verify a ratified slice); the arrow's legibility
  is judged by WI-144's SR-052/053/054 Critique rows, which are next in the loop.
