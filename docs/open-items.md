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
  from SR intent, not the TCs. After ratification: mark **WI-145** (the
  sitting's registry row) done, flip `docs/run-state` to RUNNING —
  `docs/next-wi` already points at **WI-141** — and the loop resumes
  autonomously.

### The batch as a tree (owner-requested view, added 2026-07-14)

_The SN→SR→LLR/TC hierarchy of everything this sitting ratifies. Registry
prose quoted as of 2026-07-14 — the registries stay canonical; this section
dies with the ruling. (Mechanizing this view for every future ratification is
**WI-146**.)_

- **SN-024** — subjective/perceptual acceptance is adjudicated by an
  independent critical eye against a written rubric, never by the authoring
  session — and **SN-023** — one dashboard shows progress *and how the parts
  connect*:
  - **SR-052 Dashboard accessibility** (`Critique`, v3, Planned) — operable
    and readable without a pointer or full color perception: every
    interactive element keyboard-reachable with an accessible name; no
    information encoded by color alone; readable text contrast.
    - LLR-053 — `gen_trajectory.py build_html/_svg_node/_nav`: focusable
      elements/tabindex + key handlers, title/aria names, color+shape/text
      cues, contrast ≥ the rubric's WCAG 2.1 AA threshold.
    - TC-053 (Critique) — fresh cross-family CRITIQUE session judges the
      generated dashboard against `docs/rubrics/dashboard-accessibility.md`;
      APPROVE citing anchors A1–A4.
  - **SR-053 Dashboard UI uniformity** (`Critique`, v3, Planned) — one system
    across tabs/views: one type scale + spacing rhythm, one status/phase/type
    color vocabulary, uniform node/edge/legend/detail styling across the SVG
    emitters, one interaction idiom per structure.
    - LLR-054 — shared style constants/helpers so emitters cannot drift.
    - TC-054 (Critique) — rubric `dashboard-uniformity.md`, anchors U1–U4.
  - **SR-054 Dashboard usability** (`Critique`, v3, Planned) — core reading
    tasks with low friction: project state / next work / how parts connect
    each within **one tab switch**; legible default density (start-collapsed
    per the >3 rule); detail without losing context; no clipped/overlapping
    labels at default zoom.
    - LLR-055 — landing view surfaces or one-click links each task; the task
      list lives in `docs/rubrics/dashboard-usability.md`.
    - TC-055 (Critique) — rubric anchors T1–T4.
- **SN-010** — docs stay navigable and honest — and **SN-021** — a generated
  artifact that drifts from its source is a red, not silent rot:
  - **SR-055 Ingest and human-decision process loops** (`Test`, v3, Planned)
    — the Process tab renders the two circular working loops: (A) intake →
    triage-to-WI → resume loop → build/review → merge; (B) open-items
    population (incl. the gate-ratification table) → human ruling → log
    Decisions → merge — the LLM_Agent entry node rendered once, shared by
    both; every stage links its canonical home; data-less repos render
    byte-identically.
    - LLR-056 — `process_panel/_loop_panel` extends SR-050's tab.
    - TC-056 (Integration) — both panels, stage list 1:1 to nodes, links
      resolve, deterministic, `--check` trips.
  - **SR-056 Decomposition render polish** (`Test`, v3, Planned) —
    right-sized tier columns within a declared bound; one explicit horizontal
    parent→child arrow per containment edge; hover highlight persists on the
    last-hovered item (no flash-on-exit).
    - LLR-057 — `MAX_TIER_COL` per-tier width cap; stateful highlight keyed
      to last-hovered node id.
    - TC-057 (Integration) — one arrow per edge, width ≤ the declared bound,
      persistent-highlight contract, deterministic.
  - **SR-051 rev Tiered drill-down views** (`Test`, **v2**,
    Verified→**Planned** — the owner-sanctioned reopen) — the When/How-SW
    hierarchies render **interface-wired** (IF-### seams attach to block
    input/output ports at every tier, cross-container seams aggregate to the
    boundary — Simulink-style) and **double-click descends a layer** with a
    breadcrumb return (keyboard alternative required); tiering thresholds and
    edge aggregation unchanged; supersedes the Q3 in-place-expand ruling.
    - LLR-052 — `when_view/_wi_phases/sw_containment/_descend`; rebuilt by
      dev slice WI-141; v2 stays G2 until it re-verifies.
    - TC-052 (Integration) — ports/aggregation, descend + breadcrumb +
      keyboard path, byte-determinism, `--check` trips.

## OI-9 — Ratify the research-track + knowledge-layer design spec (WI-138)

- **Decision:** bless the design in
  [specs/research-knowledge.md](specs/research-knowledge.md) (owner-intake
  items 5+6) so its §8 implementation WIs get filed — the WI-088
  spec-then-implement pattern. Four sub-decisions are listed in the spec's §6
  with recommendations: the `docs/knowledge/` home, the medium-tier default
  for research WIs, the warn-first ref check in `trace.py`, and deferring the
  OKF pack export.
- **Blast radius:** adds an opt-in kit layer (a scaffolded
  `docs/knowledge/README.md`, a warn-first `trace.py` check, one
  `PROCESS_OPTIONS.md` section) — never gating, nothing downstream must
  migrate. No spine rows change; the design deliberately reuses the existing
  CMP `Knowledge`/`DetailDoc` hooks and the WI/BuildTier machinery.
- **Revised 2026-07-14 per your feedback** (the intake:
  [specs/owner-intake-2026-07-14.md](specs/owner-intake-2026-07-14.md)) —
  what changed in the spec before you rule:
  - **§3b tier model:** research runs as a **strong-tier coordinator** that
    spawns lower-tier (quick/medium) directed gatherer subagents — your
    ruling, superseding the draft's medium default; still zero coordinator
    changes (the fan-out is the CLI's own, governed by `docs/subagent-gate`).
  - **§3a coupling:** knowledge packs present ⇒ the component layer is
    expected — a warn-first check arms the existing module→component join
    (WI-073) from knowledge presence, closing the "each implementation module
    ties back to a component" conditional you raised.
  - **§4.4:** meta-repo packs confirmed ON (the dogfood is required).
  - **§4.5/§6.5–6/§8.6–7:** the kit now also **provisions** packs downstream
    (intake item 8) — a domain-tagged library + opt-in scaffold, plus the
    skills domains filter; import scope from the ClaudeGuardChecks staging
    library is your §6.5/§6.6 call at this sitting.
  - **§9 seed:** the first end-to-end research WI = the prompt→image
    investigation (intake item 5).
- **Options:** ratify as revised · ratify with changed §6 calls · request
  changes · hold.
- **Recommendation:** ratify — the design builds on the already-resolved
  Thread-52 knowledge home rather than inventing a parallel surface, and every
  addition is warn-first/opt-in. Fits the same sitting as OI-8.
