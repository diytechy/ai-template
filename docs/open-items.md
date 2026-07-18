# Open items — owner decision briefs

The **single owner-review surface**: one section per pending decision, with the
context needed to rule — what's being decided, blast radius, options with
pros/cons, and the driver's recommendation. [status.md](status.md) carries only
the one-line form of each; the DAG rows live in
[work-items.csv](requirements/work-items.csv). **A section lives here only
while the decision is pending** — the ruling appends to [log.md](log.md)'s
Decisions log and the section is deleted. (Format:
[specs/open-items-surface.md](specs/open-items-surface.md).)

_Ruled items are recorded in [log.md](log.md)'s Decisions log (and the sitting's
GATE audit entry) and their sections deleted per the pending-only rule above — so
ruled history is **not** restated here. The sections below are the currently open
decisions._

---

## OI-3 — `main` integration decision

- **One-line:** the routine push is done (owner, 2026-07-17 — branch in sync);
  the remaining question is whether/when to integrate `derived-gate-model`
  into `main`, a deliberate sitting of its own.
- **Decision:** whether/when to integrate `derived-gate-model` into `main`
  (the push half of the original brief was executed by the owner 2026-07-17 —
  log Decisions; this section keeps the stable id, narrowed to the residue).
- **Git-checked facts (2026-07-17; re-verify at read time — an open-item claim
  about git state must come from git, not memory):**
  - `derived-gate-model` tracks `origin/derived-gate-model`, **in sync** at
    the WI-207 close — verify: `git fetch --prune && git branch -vv`;
  - `main` is several hundred commits behind this branch
    (`git rev-list --count main..derived-gate-model`) — the whole
    derived-gate/self-adoption era lives only on this branch.
- **Blast radius:** whatever consumes `main` (fresh clones, any default-branch
  automation) sees a kit hundreds of commits stale until integrated; the
  integration itself is a large fast-forward-or-merge best done at a
  deliberate cut point (e.g. after the M1/M2 migration lands).
- **Options:** integrate at the next stable cut (post-WI-209) · integrate now ·
  keep `derived-gate-model` the de-facto mainline and re-point tooling.
- **Recommendation:** integrate at the next stable cut — after WI-208/WI-209
  land and bake briefly, merge to `main` in one reviewed sitting.

## OI-4 — WI-097: LICENSE decision

- **One-line:** rule WI-097 (LICENSE + public/private intent) — no rec; needs
  the owner's public/private intent first.
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

- **One-line:** rule WI-123 (review cadence) — rec: wait for ≥ 2 phases of
  medium-BUILD evidence before switching from per-slice review.
- **Decision:** phase-close 2× adversarial review instead of per-slice
  (owner-raised 2026-07-12; spec: [specs/WI-123.md](specs/WI-123.md)).
- **Blast radius:** the unattended loop's defect-catch latency — per-slice
  reviews are the escalation sensor the medium-BUILD relax leans on.
- **Options:** adopt phase-close cadence now · keep per-slice · wait for
  evidence.
- **Recommendation (recorded):** rule only after ≥ 2 phases of medium-BUILD
  evidence.
