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
budget + index); their records live in the log's Decisions. OI-3 was corrected
against git and stays open, with OI-4 and OI-7._

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

## OI-8 — Ratify the `[v3]-[g2]` dashboard-ux batch (single-ratify's one human sitting)

- **Decision:** bless the v3 requirement work now decomposed to G2 — the single
  human ratification `single-ratify` defers to one sitting at the phase's g2
  close (`docs/gate-policy`; the derived-gate model §6). This is that close.
- **What's on the table (the g2 GATE entry in [log.md](log.md) 2026-07-14 has
  the full consistency sweep):**
  - **SR-052…056's LLR+TC** (LLR-053…057 / TC-053…057, all `Planned`) —
    including the three `Verification=Critique` rows SR-052/053/054, each
    non-LLR-exempt per SR-047 so each owns an LLR + TC beside its rubric;
  - the three intent-derived rubrics
    `docs/rubrics/dashboard-{accessibility,uniformity,usability}.md` (the
    concretized soft criteria: WCAG 2.1 AA contrast, the one-tab-switch task
    list, the `MAX_TIER_COL` bound, the loop-stage 1:1 map);
  - the **SR-051 rev** (LLR-052/TC-052 `Verified→Planned`) — interface-wired
    Simulink render + descend-a-layer/breadcrumb, holding v2 at G2 until WI-141
    rebuilds it.
- **Blast radius:** unblocks the v3 dev slices (WI-141→144, series G2→G3). No
  code shipped yet — this ratifies the *design*, not an implementation.
- **Options:** ratify the batch (agent may record it under `single-ratify`, or
  you sign off) · request changes to a specific SR/LLR/TC/rubric · hold.
- **Recommendation:** ratify — the LLM-gate consistency sweep is recorded in the
  g2 GATE entry, the mechanized floor is green (trace `--strict` orphans=0,
  derived gate G2, full suite 719 passed), and the Critique rubrics are authored
  from SR intent, not the TCs. After ratification, `docs/next-wi` → **WI-141**
  and the loop resumes autonomously.
