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
records in the log's Decisions. OI-3 (corrected against git), OI-4, OI-7,
OI-11 (session-038 REVIEW-A disposition), and OI-12 (the 042 dashboard
critique disposition) remain open._

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
- **Update (2026-07-14):** the fresh **042 CRITIQUE** has now run and did **not**
  re-raise the containment-arrow legibility (it flagged contrast, a dead panel,
  status-by-hue, and palette collisions — not the `cedge` arrow). The folded
  question is therefore answered in the affirmative — the arrow reads acceptably
  to an independent critic — so OI-11 can close with recommendation (a) at the
  next sitting; it is subsumed by **OI-12** below.

## OI-12 — 042 CRITIQUE disposition (dashboard vs SR-052/053/054 rubrics)

- **Decision:** how to disposition the **042 CRITIQUE** (fresh,
  provider-heterogeneous — Claude Fable 5; [reviews/042-CRITIQUE.md](reviews/042-CRITIQUE.md)),
  which returned **CHANGES-REQUESTED with 7 findings** + 3 TC-HARDEN proposals
  against the regenerated `PROJECT_STATE.html` judged by the three ratified
  rubrics. This is SR-047's critique loop firing for the **first time** on the
  `dashboard-ux` campaign-closing slice (WI-144).
- **The findings split two ways:**
  - **Build work that meets ALREADY-RATIFIED rubrics** (no rubric change; do it
    in WI-144's build round, provisional per the OI-8 "amendments arrive as
    future WIs" note):
    - **[BLOCKER] U4/T3/A1** — the When-tab detail aside is *dead*: its JS targets
      `#dag .wi`, but the drill emitter renders `.block` nodes (zero `.wi`), so
      the panel never populates and keyboard users have no path to WI detail.
      Rewire the drill blocks (single-click + focus) to `renderDetail(...)`.
    - **[BLOCKER] A4** — SVG label text is below the rubric's own declared 4.5:1
      floor on most node fills (e.g. `#fff` on done-green `#059669` = 3.77; amber
      = 3.19; sub-labels drop to 2.72–3.95 via the opacity discount). Darken the
      fills / drop the sub-label opacity discount. **Fixing this MEETS the
      ratified `dashboard-accessibility.md` floor — it is not an amendment.**
    - **[MAJOR] A3** — status is encoded by hue alone on drill blocks; add a
      redundant visible glyph/word (matches the phase swatch+label pattern).
    - **[MAJOR] T2** — the Knowledge tab renders all 249 nodes flat on open; apply
      the same start-collapsed `>3` grouping the When/How drills already use.
    - **[MAJOR] U3** — the How-SW drill ships no legend and no detail aside though
      its sibling When drill has both; emit the shared `.legend` + a `#sw-detail`.
    - **[MINOR] U1** — unify the three per-emitter node-label sizes (9/10/11px)
      into one shared CSS rule.
  - **Owner-gated (a rubric amendment + change-intake — ratify at phase-g2
    close):**
    - **[MAJOR] U2 → new anchor U5 "one color, one meaning"** — the same hue
      carries different meanings across tabs (`#059669` = done = phase-v3 = Test
      Case; `#d97706` = active = phase v2+v3 = Process Guide; `#0891b2` = SR =
      unphased = an sw tier). Proposes giving **phases their own hue family**
      distinct from the status vocabulary and de-colliding the per-tab type
      palettes, and **adding U5 to `docs/rubrics/dashboard-uniformity.md`**. This
      is a genuine design taxonomy call (and it couples with the A4 fill choices),
      so it wants the owner's ruling before the palette-touching build.
    - **3 × [TC-HARDEN]** (route via change-intake, PROCESS §5): (1) a TC that
      parses every emitted `<text>`/effective-fill pair and asserts WCAG ≥ 4.5
      (≥ 3.0 for ≥18.66px-bold) — mechanizes A4; (2) a TC asserting every
      `querySelectorAll` selector in emitted scripts matches ≥ 1 element (would
      have caught the dead `#dag .wi` wiring); (3) a TC asserting every multi-fill
      SVG panel also emits a legend naming each fill.
- **Blast radius:** the dashboard's readability/accessibility (the kit's own
  dogfooded trajectory surface, and the template downstream repos inherit). The
  build fixes are self-contained in `gen_trajectory.py`; the U5 amendment changes
  a ratified rubric + the palette taxonomy; the 3 TC-HARDEN cases add tests that
  would prevent regressions of exactly these classes.
- **Options:** (a) accept the split as above — build the rubric-meeting fixes in
  WI-144 (to the critique's proposed dispositions, provisional), ratify U5 + the
  3 TC-HARDEN at the g2 close · (b) request changes to a specific disposition
  (e.g. a different phase-hue family, or dark-text-on-light-tint instead of
  darker fills) · (c) hold the whole slice for a live design sitting.
- **Recommendation:** (a). The build fixes make the dashboard meet rubrics it
  already fails; the U5 anchor + TC-HARDEN are strict improvements that fit the
  OI-8 "iterate the graphic breakdowns via future amendments" note. WI-144 stays
  open and re-critiques **fresh** after the build round (never self-adjudicated).
  The one point that benefits from an early owner steer is the **phase-hue
  family** (U5) — if the owner has a palette preference, ruling it before the
  build avoids tuning fills twice.
- **Update (2026-07-14) — build round 1 landed** (log.md; commit `WI-144: …round
  1`). **Five of the six** rubric-meeting fixes shipped and are verified: A4
  (contrast, 0/8 fills fail a WCAG scan), U4 (dead When panel rewired), A3 (status
  glyph), U3 (How-SW legend + `#sw-detail`), U1 (shared type scale). A4 darkened
  fills within-hue, so it does **not** foreclose the U5 taxonomy call. **Still
  pending build:** [MAJOR T2] Knowledge-tab density — deferred one round (a
  faithful grouping is a `.knode`/`knowarrow` re-spec that wants its own focused
  pass). **Still owner-gated (unchanged by this round):** the **U5** anchor +
  phase-hue de-collision, and the **3 TC-HARDEN** cases — ratify at the phase-g2
  close. Next in the loop: a **fresh re-critique** of the rebuilt dashboard (it
  will re-surface T2 and judge the five landed fixes).
