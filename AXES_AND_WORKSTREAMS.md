# Axes & Workstreams — how to organize *what* / *how* / *when* without duplication

**Author:** Claude (Opus 4.8), design note from a working session ·
**Date:** 2026-07-08 · **Branch:** `MultiRepoSupport` (not pushed) ·
**Status:** **OPEN — a ruling-in-progress. Expect iteration.** Nothing here is
built; no registry or script has been touched.

## Provenance

This came out of reviewing the recent **"how"-emphasis** work — the trajectory /
work-items layer (Thread 52) — and the risks [`THREAD_52_REVIEW.md`](THREAD_52_REVIEW.md)
flagged. The owner's concern, in their words:

> The updates to emphasize the *how* may be conflating **how** and **when**. Future
> iteration will force development on a "track" that was already structured to fix a
> particular issue, and I don't want agents or humans relearning what an older track
> already outlined. Iterating just means something needs tuning, or a new approach
> needs exploring. Are these really *tracks*, or *domains*? How do I keep the **what**
> (SN→SR→LLR), the **how** (mainly tracks), and the **when** (schedule) aligned and
> connected without duplication?

This is a **triage / design input, not a plan** (the same posture as the review).
It **folds in `THREAD_52_REVIEW.md` F3** (the work-items schema question) and
**touches F1** (tracing the layer's own code). It exists so the next session
inherits the framing instead of re-deriving it.

> How to read: §1 names the conflation with evidence. §2 is the core reframe (four
> axes). §3 is why today's model fails the iteration case. §4 is the proposed shape.
> §5 is the naming ruling. §6 is cautions + staging. §7 is the provisional decision.
> §8 is the open questions the next iteration must close.

---

## 1. The conflation: "track" names two unrelated things

The word **track** currently means two things that have nothing to do with each
other:

**(a) An execution lane.** In [`tracks-README.template.md`](project-trajectory/tracks-README.template.md)
and the "Parallel tracks" layer of [`PROCESS_OPTIONS.md`](project-trajectory/PROCESS_OPTIONS.md)
(§ "Parallel tracks (multi-lane operation)"), a track is a *worktree +
`llm/<track>` branch + `docs/tracks/<track>/` lane*. It is purely a **when / who-
runs-it-in-parallel** device — concurrency control so two drivers never thrash one
blackboard. Transient, chosen by invocation, never even committed as a pointer.

**(b) A grouping label on a work item.** In
[`docs/requirements/work-items.csv`](docs/requirements/work-items.csv) the `Track`
column holds `docs` / `scripts` / `unattended` / `self-adoption`. Look at what
[`gen_trajectory.py`](project-trajectory/scripts/gen_trajectory.py) actually does
with it: it seeds the DAG cluster order (`key=lambda n: (by_id[n]["track"], n)` in
`_dag_layout`), sets a display label (`TRACK_LABELS`), counts distinct values for a
tile, and prints one detail line. **That's the whole use.** It carries no
dependency semantics and no worktree/branch reality.

So the `work-items.csv` "Track" **is not a track**. It is a **functional grouping**
— what the owner is reaching for when they say *domain*. And the prose already
encodes the conflation: `PROCESS_OPTIONS.md` calls it *"a **track** — a lane of
related work (`scripts`, `docs`, a subsystem)"*, borrowing the parallel-lane
metaphor for something that has nothing to do with lanes.

**Renaming here is not bikeshedding — the shared word is the root cause of the
conflation.**

---

## 2. The reframe: there are four axes, not three

The owner's *what / how / when* frame is right, but **"how" is hiding two different
things**, and one of the four axes is already modeled and easy to forget:

| Axis | The question it answers | Where it lives today | State |
|---|---|---|---|
| **WHAT** — truth | What must be true? | the `SN→SR→LLR→TC` spine | ✅ solid |
| **HOW-physical** — assembly / where | What parts/modules make it, and where do they live? | `LLR.Module`; off-spine `MOD` (multi-repo delegation), `ASSET`, `PART` (procurement) | ◐ modeled but scattered |
| **HOW-functional** — decomposition | How do we carve the *problem* into durable workstreams? | a flat `Track` string on the work item | ❌ **under-modeled** |
| **WHEN** — schedule | In what order, and who runs it in parallel? | WI `Predecessors` + `Status` DAG; the parallel-execution *tracks* (worktree/branch/lane) | ✅ modeled |

Two observations fall straight out of the table:

- **Three of the four axes already have homes.** The physical/where axis is real —
  `LLR.Module` names the code module; `MOD-###` delegates SRs to whole repos in the
  multi-repo rung; `ASSET`/`PART` cover un-diffable assets and procurement. It is
  scattered rather than a single clean hierarchy, but it exists and is genuinely
  *distinct* from functional decomposition (one functional workstream can span
  modules; one module can serve several workstreams).
- **The only missing home is HOW-functional** — and it is being **faked by a
  throwaway column that is misnamed after the WHEN axis.** That is the entire
  problem in one sentence.

---

## 3. Why the flat `Track` fails the iteration scenario

The owner's real worry: *iteration returns to a problem that was already
structured, and I don't want to relearn what the older structure already worked
out.* Today's model **cannot** support that, because `Track` is a flat cosmetic
label on a work item, and work items go `queued → active → done` and then freeze.
When a problem is re-opened:

- **Tuning it** → a new WI, perhaps tagged with the same `Track=scripts` string.
  Nothing links the new attempt to the prior one's structure or rationale.
- **A new approach entirely** → new WIs, possibly *new or rewritten SRs/LLRs*. The
  through-line to "the same problem" is lost, because the only durable nodes (SN,
  SR) may themselves change under the new approach.

So the durable thing the owner keeps returning to — *"the particular issue"* — has
**no entity**. It is smeared across an SN that is too coarse, a `Track` string that
is only a colour, and a pile of `done` WIs that would need archaeology. That
archaeology *is* the "relearn it every time" tax.

Note the durable anchor must survive an SR/LLR rewrite (a "new approach entirely"
can change the requirements). The only things that survive that today are the SN
(usually too coarse) and — nothing else. That "nothing else" is the gap.

---

## 4. Proposed shape: reference-not-restate, with a durable *Workstream* entity

The kit already knows how to relate axes without duplication: **each axis is its
own source of truth; connections are id-references; the dashboard is a generated
*view* that joins them** — the `trace.py` / "a view, never a source of truth"
idiom. The fix is to apply that *same* pattern to the missing axis instead of
smuggling it into a WHEN column.

Concretely, promote the functional decomposition to a first-class, durable entity —
provisionally a **Workstream**:

- **Its own off-spine registry**, e.g. `workstreams.csv`:
  `WS-ID, Title, Parent, Serves (SN/SR refs), Status, Rationale/Log-link`.
  - `Parent` gives the **hierarchy** the owner asked for ("functional breakdowns
    are a hierarchy").
  - `Serves` points **up** to the SN/SR it currently serves — a **soft, updatable**
    link (not a hard `trace.py` edge), so a new approach that rewrites the SRs
    re-points the workstream *without losing its identity*.
  - `Rationale/Log-link` is the one thing SN→SR→LLR structurally lack: an
    accumulating home for *what was already tried* — the surface that ends the
    relearn tax.
- **WIs point at it.** Rename the WI `Track` column → `Workstream`; value `WS-003`.
  Now many WIs across time roll up to one durable node.
- **The view clusters by it.** [`gen_trajectory.py`](project-trajectory/scripts/gen_trajectory.py)
  already clusters the DAG by `Track`; it clusters by `Workstream` instead, and can
  additionally render the roll-up tree.

**The anti-duplication guardrail (this is the answer to "without duplication").** A
Workstream must **never restate** SR/LLR text — only *reference* it (keys), plus the
rationale. If you catch yourself copying requirement prose into it, that is the
smell. The axes stay aligned because they are **joined by ids, not by paraphrase**,
and nothing is a source of truth for more than one axis.

This also resolves the owner's observation that a WI is "allocated to a track *and*
to a functional breakdown": those were **always two different allocations** —
`WI → execution-lane` (transient, operational, keeps the name *track*) and
`WI → workstream` (durable, functional, the renamed thing). Today they are
collapsed into one flat string; splitting them is the fix.

---

## 5. Naming ruling (provisional)

Semantics matter *here* precisely because "track" is already taken by the parallel-
execution layer. Ranking:

- **Workstream** — preferred. Says "a durable line of effort on a problem," which is
  exactly the iteration anchor. No collision.
- **Domain** — acceptable (the word the owner reached for), but it leans "area of
  the system," risking confusion with `MOD` / modules (the physical axis).
- **Track** — **retire it from the WI layer.** Leave "track" to mean *only* the
  parallel-execution lane.

---

## 6. Cautions & staging

- **Do not invent a fourth hierarchy that duplicates SR/LLR.** `SN→SR→LLR` is
  *already* a decomposition. A Workstream is only justified when it is genuinely
  orthogonal — a durable line of *effort* that cross-cuts requirements and survives
  their rewrites. If, in practice, workstreams map 1:1 to SNs, **do not build the
  registry** — a `Workstream` column that just references an SN is enough. Reach for
  the registry only when a workstream provably spans multiple SRs *and* outlives
  them.
- **This is downstream-migrating.** A new registry + a renamed WI column is
  inherited by every adopter. That is exactly the class of change
  [`THREAD_52_REVIEW.md`](THREAD_52_REVIEW.md) **F3** says to *decide before adoption
  spreads* — and F3's "hard-vs-soft predecessor edges" question is the same schema
  conversation. **Settle both in one ruling.**
- **It intersects F1.** F1 wants `SR-037/038` to trace the trajectory layer's own
  code and raises a G3 re-attestation question. If the WI schema is changing anyway,
  **sequence F1 first** so the ratified spine is not re-attested twice.
- **Staging (recommended):**
  - **Now (cheap, non-migrating):** rename `Track → Workstream`, and write the
    four-axis distinction into `PROCESS_OPTIONS.md` as a companion to F3. Documents
    the model and ends the word-collision without forcing anyone to migrate data.
  - **Later (gated on real need):** promote to `workstreams.csv` with `Parent` +
    the rationale link — only when a repo (or this one's own next iteration)
    actually needs the durable, hierarchical node. Do not build the hierarchy
    speculatively (YAGNI; the kit's "smallest change that works").

---

## 7. Provisional decision

Adopt the organizing principle: **four axes, each its own source of truth, joined
by id-references, surfaced by generated views — never by restating one axis inside
another.** Three axes already follow it. The fix is to stop letting the *functional*
axis freeload on the *execution-lane* word and the WHEN column, and give it its own
durable, hierarchical home so iteration **rejoins** prior structure instead of
relearning it.

Two moves, staged as in §6:

1. **Now:** `Track → Workstream` rename + the four-axis section in
   `PROCESS_OPTIONS.md` (as the F3 companion ruling).
2. **When a repo needs the durable node:** the `workstreams.csv` registry with
   `Parent` + rationale link.

**Status: provisional — not ratified, not built.** The owner has said this will
iterate.

---

## 8. Open questions for the next iteration

1. **Workstream vs SN — is it really a separate axis, or a coarser roll-up over
   SNs?** If workstreams reliably map 1:1 to stakeholder needs, the registry is
   redundant (see §6). Test this against 3–4 real "re-opened problem" cases before
   committing to a new registry.
2. **Where does the rationale actually live?** A `Rationale` cell, a link into
   `docs/log.md` / the thread notes, or a per-workstream note file? Whatever it is,
   it must stay single-sourced (no paraphrasing the threads).
3. **Hard-vs-soft edges (F3).** Does `work-items.csv` also need a
   hard-predecessor (blocks) vs soft-ordering (reads-well) distinction? Same schema
   ruling; decide together.
4. **How does a Workstream relate to the physical axis (`MOD` / `LLR.Module`)?**
   Confirm they stay orthogonal (a workstream may span modules) and that the view
   does not imply otherwise.
5. **Granularity (F3).** Independent of the schema: is the 37-WI / 4-group cut the
   right one, or should some groups split/merge once they are Workstreams?
6. **Migration ergonomics.** If `workstreams.csv` ships, what does `bootstrap.py`
   scaffold, and does `downstream-resync` need a step? (Downstream-migrating —
   §6.)

---

## Cross-links

- [`THREAD_52_REVIEW.md`](THREAD_52_REVIEW.md) — the review that surfaced this;
  **F3** (schema/edge-semantics) and **F1** (trace the layer's own code) are the
  two findings this note is coupled to.
- [`docs/requirements/work-items.csv`](docs/requirements/work-items.csv) — the
  `Track` column this note proposes renaming.
- [`project-trajectory/scripts/gen_trajectory.py`](project-trajectory/scripts/gen_trajectory.py)
  · [`project-trajectory/scripts/check_trajectory.py`](project-trajectory/scripts/check_trajectory.py)
  — the view + validator that would follow the rename.
- [`project-trajectory/PROCESS_OPTIONS.md`](project-trajectory/PROCESS_OPTIONS.md)
  — "Trajectory / work-items layer" (the `Track` prose) and "Parallel tracks" (the
  *other*, execution-lane meaning of "track").
- [`project-trajectory/tracks-README.template.md`](project-trajectory/tracks-README.template.md)
  — the execution-lane "track" that keeps its name.
