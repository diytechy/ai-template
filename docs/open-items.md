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
OI-11 (session-038 REVIEW-A disposition), OI-12 (the 042 dashboard
critique disposition), and OI-13 (the WI-147 pause `run-state` deviation)
remain open._

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
- **Update (2026-07-14) — fresh re-critique ran + build round 2 landed.** The
  independent re-critique fired ([reviews/048-CRITIQUE.md](reviews/048-CRITIQUE.md),
  provider-heterogeneous; **CHANGES-REQUESTED, 5 findings + 2 TC-HARDEN**). It
  confirmed the round-1 fixes (A2/A3/A4/U1/U4/T3/T4 all pass) and raised **new**
  build items, now shipped in **build round 2** (verified; full trajectory suite
  75 passed, smoke 593):
  - **[BLOCKER] A1** — leaf drill blocks carried click/focus detail handlers but
    no `tabindex`, so keyboard readers couldn't open any WI/module detail. Every
    `.block` is now `tabindex="0"` (containers keep their `role="button"`).
  - **[MAJOR] T1** — "find the next work" cost three descents; the landing hero
    now names the active WI (id + title) in a `.sub.nowat` line — zero tab switches.
  - **[MINOR] U3** — the knowledge `.kedge` hardcoded `#94a3b8`, diverging from the
    drill `.wire` in light mode; it now shares the `--muted` stroke token at 1.5px.
  - **046-REVIEW-A [MAJOR]** (a separate REVIEW-A round, its finding folded in
    here) — the `<=3-tier` flat `dag_svg` fallback showed the bare WI id; it now
    glyph-prefixes the `.wid` label like the drill (A3's "every status" floor for
    small registries). Regression tests added for all four.
  - **Deferred / owner-gated (unchanged):** **[MINOR T2]** Knowledge-tab density
    (the `.knode`/`knowarrow` re-spec — its own focused pass); the **U5** anchor
    (048 refines it to "no cross-vocabulary colour collision" — a phase hex reused
    by the status/tier/kind vocab in one view) + phase-hue de-collision, and the
    **TC-HARDEN** cases (the tabindex-has-handler and palette-disjoint assertions).
  - **After the next fresh re-critique confirms round 2, WI-144's buildable work
    is complete** — only the owner ratification of U5 + TC-HARDEN at the phase-g2
    close remains for the slice to close and the spine to rejoin G3.
- **Update (2026-07-14) — round-3 re-critique ran; critique budget now EXHAUSTED.**
  The fresh re-critique fired ([reviews/052-CRITIQUE.md](reviews/052-CRITIQUE.md),
  provider-heterogeneous, no implementer notes; **CHANGES-REQUESTED, 8 findings + 3
  TC-HARDEN**), preceded by a 050-REVIEW-A (NO-COMMIT, 1 MINOR — status.md verbosity,
  acted on) and a 051 CRITIQUE ERROR (no verdict — did not count). This is the
  **3rd** CHANGES-REQUESTED critique on the SR-052/053/054 scope (042/048/052), so
  per `AGENT_CRITIQUE_MAX=3` the loop's budget is spent and `single-ratify`'s
  `failure_action` **pauses WI-144 and surfaces the block for the batched
  ratification** (it does not auto-page; run-state is driver-set to NEEDS-HUMAN
  because no non-dependent WI is safely auto-startable). The 052 findings split the
  same two ways, with one honesty correction:
  - **Newly-buildable, rubric-MEETING (round-1's A4 scan was too narrow — it
    covered SVG node text-on-fill only, missing the HTML surfaces below, so A4 is
    **not** actually satisfied):**
    - **[MAJOR] A4 queued detail badge** — `.detail .badge` hard-codes `color:#fff`
      on the `queued` slate `#94a3b8` = **2.56:1** (.68rem, normal text) vs the
      ratified 4.5:1 floor. Fix: dark ink `#0f172a` (the `#dag .wi.queued text`
      already uses it). ~1-line emitter/CSS fix.
    - **[MINOR] A4 focus ring** — the amber `#f59e0b` 2.5px focus stroke (the sole
      focus cue; native outlines suppressed) measures **2.05:1** on white vs the
      3:1 graphical-boundary floor. Fix: darker ring (`#b45309` ≈ 3.2:1).
    - **[MAJOR] T4 `.blab` overflow** — drill main labels are emitted untruncated
      while `.bsub` truncates with `…`; long ids (`system-requirements.csv` 41ch in
      a 172px block) overrun the block + arrowheads. Fix: apply `.bsub`'s
      width-fit truncation to `.blab` (full text already in `<title>`).
    - **[MINOR] U4 / U3 / U1** — When-container click→detail parity, converge the
      two legend idioms, collapse the 21 near-duplicate HTML font sizes (polish).
  - **Owner-gated (recurring — proposed at 042/048/052):** **U5** "one concept per
    colour" (U2 palette collision — green/amber phase-accents render directly above
    a status legend declaring green=done/amber=active) + phase-hue de-collision;
    **[MAJOR] T2** Knowledge tab opens as 249 nodes flat (the `.knode`/`knowarrow`
    re-spec, its own pass); the **3 × TC-HARDEN** (contrast, label-fit,
    palette-bijection — route via change-intake, PROCESS §5).
- **Recurrence insight (the reason the budget tripped):** the contrast TC-HARDEN
  has been proposed **three rounds running** because manual A4 fixing keeps missing
  a surface (round 1 fixed SVG fills; round 3 found the badge + focus ring still
  fail). The durable fix is the **mechanized** contrast/label-fit/palette tests, not
  another hand pass — so the strong recommendation at the sitting is to **ratify the
  3 TC-HARDEN cases first**, then land ONE final build round that fixes every
  contrast/label surface at once with a test proving it (and tunes the badge/fill
  inks together with the U5 palette ruling, since the critic notes they couple).
  This ends the whack-a-mole the budget exists to stop.
- **Recommendation (at the phase-g2 sitting):** ratify the U5 anchor + the 3
  TC-HARDEN, authorize the residual buildable A4/T4 fixes as one final owner-directed
  build round (paired with the U5 palette ruling), and defer T2 to its own
  `.knode`/`knowarrow` pass. Alternatives: rule a specific palette family for U5 ·
  hold the whole slice for a live design sitting.

## OI-13 — WI-147: pause leaves `run-state` untouched vs. the spec's `ask:` line

- **Decision:** whether to **ratify the documented WI-147 deviation** (amend the
  spec so a `docs/pause` stop leaves `run-state` untouched) or **direct a code
  fix** (persist `NEEDS-HUMAN` + `ask: docs/pause` on pause, and clear it on
  resume). Surfaced by the orphaned **062-REVIEW-A** (session-062 REVIEW-A on
  WI-147, NO-COMMIT, 1 MAJOR + 1 MINOR, CHANGES-REQUESTED;
  [reviews/062-REVIEW-A.md](reviews/062-REVIEW-A.md)) — reconciled from the working
  tree, its live MAJOR routed here rather than buried.
- **The divergence (verified against code + tests + deliverable + the WI-147 log
  entry):** the WI-147 spec
  ([specs/owner-intake-2026-07-14.md](specs/owner-intake-2026-07-14.md)
  #pause-blackout) says the coordinator "stops the loop with a clear banner
  **(and the run-state `ask:` line naming `docs/pause`)**." The shipped code
  (`agent_loop.py` `pause_reason` docstring + the top-of-loop pause branch, exit
  8) **deliberately leaves `run-state` untouched** and honors the phrase as the
  **banner detail** instead; `test_pause_delete_resumes` and the WI-147 deliverable
  both lock in "run-state untouched." The builder **documented this as an explicit
  deviation** (log.md WI-147 session entry: persisting `NEEDS-HUMAN` "would force a
  two-act resume and contradict 'deleting it resumes'"). The reviewer disputed it
  and asked for "an explicit spec amendment before closing WI-147" — but WI-147's
  row is already `done` with **no owner ruling**, so the amendment the deviation
  needs is still outstanding.
- **Blast radius:** narrow and self-contained (one coordinator control, absent by
  default downstream). The tension is purely which signal carries "paused": today
  it is the **exit code (8) + banner**; the spec wanted it **also in `run-state`**.
- **Options:**
  - **(a) Ratify the deviation (amend the spec).** Bless the shipped
    file-is-the-contract design; strike/soften the spec parenthetical to "the
    banner names `docs/pause` + the resume act." No code/test change; keeps the
    single-act delete-to-resume.
  - **(b) Direct the code fix.** Persist `NEEDS-HUMAN` + `ask: docs/pause` on
    pause and clear it on resume (a two-act resume, or a launcher special-case
    that treats `run-state=NEEDS-HUMAN` + `ask:docs/pause` + file-absent as
    resumable). Reopens WI-147 for a corrective slice + test updates.
- **Recommendation: (a) ratify the deviation.** The rationale is already recorded
  and sound: a graceful pause is an operator "I'll be back," semantically distinct
  from a `NEEDS-HUMAN` decision-block — and setting `NEEDS-HUMAN` here would
  collide with the loop's own `trajectory --strict` rule that rejects a stale
  `NEEDS-HUMAN` park while work is actionable. Code, tests, and deliverable already
  cohere. **Honest downside:** an external monitor reading only `run-state` sees
  `RUNNING` while the loop is paused — mitigated (not eliminated) by the
  `EXIT_PAUSED=8` exit code + the stop banner. If the owner weights the
  observable-state concern higher, option (b) is the fix. (The MINOR finding —
  session-062's `status.md:95` forward-only nit — is **superseded**: that
  queued-backlog line was rewritten away in the interim; the residual "shipped"
  mentions in status.md are load-bearing queue-boundary context, not
  history-narration, so no action.)
