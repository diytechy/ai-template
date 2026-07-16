# Open items — owner decision briefs

The **single owner-review surface**: one section per pending decision, with the
context needed to rule — what's being decided, blast radius, options with
pros/cons, and the driver's recommendation. [status.md](status.md) carries only
the one-line form of each; the DAG rows live in
[work-items.csv](requirements/work-items.csv). **A section lives here only
while the decision is pending** — the ruling appends to [log.md](log.md)'s
Decisions log and the section is deleted. (Format:
[specs/open-items-surface.md](specs/open-items-surface.md).)

_The 2026-07-13 sitting ruled OI-1/OI-2/OI-5/OI-6; the 2026-07-14 ratification
sitting ratified OI-8 (the `[v3]-[g2]` batch) and OI-9 (the research-knowledge
spec). The 2026-07-14 phase-v3 g2-close sitting ruled OI-11 (containment arrow —
accept), OI-12 (the 042/048/052 critique disposition — accept: U5 + 3 TC-HARDEN
ratified, one final WI-144 build round, T2 → WI-159) and OI-13 (the WI-147 pause
`run-state` deviation — ratified + documented) — all in the log's Decisions.
OI-3 (corrected against git), OI-4, and OI-7 remain open._

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
- **Blast radius:** durability of ~10 commits of ratification + phase work
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

- **Decision:** phase-close 2× adversarial review instead of per-slice
  (owner-raised 2026-07-12; spec: [specs/WI-123.md](specs/WI-123.md)).
- **Blast radius:** the unattended loop's defect-catch latency — per-slice
  reviews are the escalation sensor the medium-BUILD relax leans on.
- **Options:** adopt phase-close cadence now · keep per-slice · wait for
  evidence.
- **Recommendation (recorded):** rule only after ≥ 2 phases of medium-BUILD
  evidence.
