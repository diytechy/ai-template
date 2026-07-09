# Agent roles & the coordinator loop — the dynamic layer

**Author:** Claude (Opus 4.8), design note from a working session ·
**Date:** 2026-07-09 · **Branch:** `MultiRepoSupport` (not pushed) ·
**Status:** **OPEN — a ruling-in-progress. Expect more passes before implementation.**
Nothing here is built.

## Provenance

Split out of [`AXES_AND_WORKSTREAMS.md`](AXES_AND_WORKSTREAMS.md) (iteration 6, was its
"Operating the model" section). That note is the **static structure** — the registries
and how they relate (WHAT / WHY / HOW / WHEN). **This** note is the **dynamic layer** —
*who does what, in what order, and how feedback flows*. They are deliberately separate
concerns; keeping them in one note conflated structure with process.

A lot of this **already exists** in the kit and should be *situated against it*, not
reinvented:

- [`agent_loop.py`](project-trajectory/scripts/agent_loop.py) — the unattended
  **coordinator** (headless resume, typed outcomes, parallel tracks).
- `docs/run-phase` — the model-tier key (`PLAN | BUILD | …`).
- `docs/run-state` — the coordinator contract (`RUNNING | DONE | BLOCKED | NEEDS-HUMAN`).
- The **integrator** role ([`tracks-README.template.md`](project-trajectory/tracks-README.template.md))
  — the only writer of the root dispatcher; lands changes.

This is a **triage / design input, not a plan.**

---

## The pipeline

**coordinator → planner → implementer → reviewer(s) → coordinator**, looping through
the roadmap. Walked through as the owner described it:

1. **Coordinator** is running the roadmap. It ingests feedback (test results, reviewer
   findings, human input), and when a gap is identified it **creates a work item** to
   resolve it (naming the affected swBlock(s)/part(s) + the gap).
2. It dispatches that WI to a **planner**, which builds the detailed plan, **updates the
   module (swBlock) definition + knowledge pack**, does research if needed, and **writes
   back into the WI** the specifics it added to the module definition.
3. The planner hands off to an **implementer**, which performs the implementation and
   confirms completion back to the coordinator.
4. The coordinator sets off **one or two reviewers**, which **execute the test cases**
   and generate feedback.
5. The coordinator ingests that feedback, **makes adjustments** if needed, and **kicks
   off the next agent(s)** to continue through the roadmap.

## Each role writes exactly one home (the tie to the static model)

This is what keeps the dynamic layer aligned with the static structure — no role
restates another's home:

| Role | Writes (its one home) | Existing kit anchor |
|---|---|---|
| **Coordinator** | the **roadmap DAG** (creates / reprioritises WIs from feedback) | `agent_loop.py` + integrator |
| **Planner** | the **swBlock definition + knowledge pack**; updates the WI with what it added | PLAN phase |
| **Implementer** | the **code** | BUILD phase |
| **Reviewer(s)** | **test evidence** — executes the TCs → feedback | the gate / TCs |

## Break the coordinator along the loop-vs-judgment seam

The coordinator is doing two different jobs, and they should be split:

- **The mechanical loop** — dispatch an agent, collect its typed outcome, advance —
  stays **dumb and deterministic**. That is `agent_loop.py` as-is.
- **Roadmap maintenance** — deciding *what WIs to create / reprioritise* from test /
  reviewer / human feedback — is **judgment**, and belongs to a distinct step. The kit
  already has a name for it: the **integrator** (the only writer of the dispatcher).

So the "breakup" is **not new machinery** — it is *naming the seam that already exists*:
**loop = orchestration, integrator = roadmap judgment.** Don't put judgment inside the
loop.

## Open questions

1. **Reviewer count / independence** — one reviewer or two, and do they run the same TCs
   or split coverage? What makes a reviewer's feedback *land* as a new WI vs. a direct
   fix.
2. **Where the loop/integrator split lives mechanically** — a distinct `agent_loop`
   sub-mode, a separate integrator leg, or a human step under `attended` authority.
3. **Feedback → roadmap** — the exact path from a failing TC / reviewer finding to a new
   or reprioritised WI (who writes it, under which gate authority).
4. **Relationship to parallel tracks** — how the pipeline composes with the existing
   per-track lanes (one pipeline per track? a shared coordinator across tracks?).

## Cross-links

- [`AXES_AND_WORKSTREAMS.md`](AXES_AND_WORKSTREAMS.md) — the static structure this
  operates on (swBlocks, parts, the roadmap DAG, knowledge packs).
- [`project-trajectory/scripts/agent_loop.py`](project-trajectory/scripts/agent_loop.py)
  · `docs/run-phase` · `docs/run-state` · the integrator role in
  [`tracks-README.template.md`](project-trajectory/tracks-README.template.md).
- [`THREAD_52_REVIEW.md`](THREAD_52_REVIEW.md) — the review lineage these notes descend
  from.
