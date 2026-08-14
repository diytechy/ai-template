# R3 and R4 — the context the two open rulings need (2026-08-01)

Written at the owner's request after the first ruling pass: R1 (id minting)
and R2 (evidence cells) are **ruled as recommended**; R3 and R4 needed more
background than the [backlog plan](backlog-plan-2026-08-01.md)'s briefs
carried. This file is that background, self-contained, for someone who has
not lived in this repo's vocabulary. Nothing here executes until ruled —
reply in session, or annotate this file.

---

## R3 — WI-395, and what "blocked" actually is

### The mechanism, in plain terms

- Every work item is one file; the folder it sits in **is** its state:
  `queued/`, `active/`, `deferred/`, `cancelled/`, `complete/`, `draft/`
  under [docs/work/](../../work/).
- **`blocked` is not a folder.** A row is "blocked" when it sits in `queued/`
  and its header carries a `blockref` line naming *why* it is parked (an open
  decision, another work item, or a note).
- The scheduler drops such a row from the ready frontier by checking that the
  `blockref` key **exists**. It never reads the state of the thing the key
  names. That is the whole mechanism.
- So the only release today is a person (or an agent at the owner's
  direction) editing the file: delete the `blockref` line to return it to the
  frontier, or move it to `cancelled/` or `deferred/`.

### Answering the question asked: "a blocked branch has no resolution method?"

Two different things resolve differently, and the distinction is the crux:

- **The branch always resolves.** Since the terminal-outcomes row merged
  (2026-08-01), every lane ends in a merge to trunk, by construction — as a
  completion, as a cancellation, or as a **handback** (partial work merged
  as-is, findable, unable to red anything). No branch dangles. This half of
  the owner's requirement is **built and merged**.
- **The returned work-item row does not resolve.** After a handback, the row
  sits in `queued/` with a `blockref` pointing at its own spec (deliberately —
  so the driver does not claim → hand back → re-claim the same row forever).
  What happens next is nobody's job: no machinery reads the handback reason
  and disposes of the row. It waits, parked, until a human notices. **That
  missing disposition step is the real gap**, and it is what the rest of this
  section is about.

### The complete history of parks: one, and it was a mistake

WI-391 (2026-08-01) is the only park this repo has ever created. The builder
discovered the row's premise was refuted, and returned it to `queued/` with
`blockref = OI-11` — *assuming* that when the owner ruled OI-11 the row would
come back to the frontier. Measured: it would not; nothing reads an open
item's state, so the park was permanent. The correction was to **cancel** the
row instead — which was the right disposition anyway, since its refutation
held under every possible ruling. That mis-assumption is the defect WI-395 files (its spec is in
[docs/work/](../../work/); un-linked here because a row's file moves folder with
every state change): the repo's own exemplar text *promises* the self-release
the mechanism does not provide.

### What will park rows from now on: handbacks

The handback machinery merged with the terminal-outcomes row. Its real
triggers, from the loop's own exit paths (none of them is broken code): a
review escalation past the streak budget (expected to be the most common),
no routable model or provider auth failure, a critique budget exhausted while
still CHANGES-REQUESTED, and a dual-plan page needing a human choice. Worker
*crashes* are a separate path — the lane persists and is re-assigned; a crash
never becomes a park.

### The owner's direction as heard (2026-08-01) — to confirm or correct

Stated in session, paraphrased tightly:

1. A broken item may end cancelled or partial, **but the branch must not
   dangle** — it integrates what it can.
2. The lane hands its reason back **to the dispatcher**, and the
   **dispatcher completes the disposition**: cancel the work item with
   rationale, defer it with rationale, draft related follow-up content, or
   surface an open item where a human ruling is genuinely needed.
3. That repair/disposition process is **loop machinery, not a work item** — a
   work item's job can never be to recover another work item.

Reading against what exists:

- Point 1 is already true and merged (see above).
- Point 2 is the missing piece. Today the handback *carries* the reason back
  (the spec's own Handback section names what remains) but nothing consumes
  it. Under this direction the dispatcher gains a **handback-intake arm**:
  each cycle it reads returned rows and disposes of them — cancel / defer /
  re-queue with drafted follow-up / surface as an open item — so the parked
  state is transient by construction rather than permanent by silence.
- Point 3 places that arm in the dispatcher row's scope (the row that builds
  `dispatch.py`), **not** in a new "recover WI-NNN" work item. Its spec would
  be amended trunk-side at claim time to carry the arm.
- Consequence for WI-395: it **narrows to its honest remainder** — correct
  the two byte-identical exemplar paragraphs that promise auto-release, and
  point them at the dispatcher's disposition arm as the actual mechanism.
  The original build-a-subscription option dissolves: consulting a blocker's
  state cannot serve the self-blocked handback shape at all, and the one
  historical park it *could* have served was better answered by cancellation.

**What executes if the owner confirms:** the direction is recorded in
[log.md](../../log.md)'s Decisions; the dispatcher row's spec gains the intake arm
before it is claimed; WI-395 is executed as the wording fix. If any numbered
point above misstates the intent, correcting the point corrects the plan.

### The arbitration-row variant (owner, 2026-08-01 — under consideration)

The owner is considering that a work item might need to mint a **placeholder
work item as a handback**, to mechanize an arbitration cycle. Analysis
against the machinery as it now stands:

- **Where the mint happens decides everything.** An *in-lane* mint (the
  placeholder created in the branch's own tree as part of handing back) would
  be refused by the just-shipped minting rung, and would reintroduce the
  collision it exists to end — two lanes handing back concurrently would each
  take the same next id. Minted **at intake** — by the dispatcher, on trunk,
  serially, when the handback merge lands — it is the already-ruled
  adjudication pattern (mechanical mint, derived description, no model)
  extended from spine amendments to handback disposition. And the lane loses
  nothing by not minting: the returned spec's own Handback section already
  carries the row id, the reason, and what remains — everything the derived
  placeholder needs.
- **Reconciled with "recovery is loop machinery, never a work item":** the
  *machinery* mints and routes; the minted row is the arbitration **instance**
  made visible, claimable, and dispatchable under the gate-policy dial — the
  same "force in a WI that must be attended to" shape already ruled for the
  adjudication kind. The row's job is the judgement, never the recovery.
- **One new invariant is required: no recursion.** An arbitration row's only
  outcomes are a disposition (then it completes) or an escalation to the
  owner surface. It can never itself hand back — otherwise handbacks could
  chain arbitration rows forever.
- **Effect on work in process: nothing running is invalidated.**
  - The shipped minting rung: unchanged — it governs branch deltas only, and
    the intake mint is trunk-side, the path it deliberately leaves free.
  - The adjudication row is the natural home for the arbitration cycle — it
    absorbs the handback mint the same way it absorbed the
    backlog-re-evaluation row: same judgement, same agent, one home.
  - The dispatcher row gains only the intake *trigger* (detect a merged
    handback, mint, route); the judgement rides the minted row.
  - WI-395 is unchanged as the wording fix — and this variant **closes the
    original R3 question**: release becomes event-driven (a mint at intake)
    instead of state-polled, so the cross-registry blocker-subscription is
    never needed by anyone.
  - Drain order unchanged. The spec amendments to the dispatcher and
    adjudication rows are ordinary serial trunk-side edits at or before
    claim, which also clear their standing SpecRef-freshness warnings.
- **The no-row alternative, for completeness:** the dispatcher could apply
  dispositions in place on the handed-back row, with no placeholder. Less
  code, but the arbitration act becomes invisible to the frontier and the
  dashboard, and cannot be dispatched or dialed by gate policy. Stated so the
  choice is honest; not recommended.

---

## R4 — OI-11, and what "16 of 111 files map to no terminal state" means

### The vocabulary

- **Terminal state** = how a work item *ended*. There are exactly two:
  `complete` (built and shipped) and `cancelled` (decided against). In the
  live registry this is literally the folder the row's file sits in.
- **Spec-of-record** = the longer design document many work items carry
  beside their registry row. When a work item closes, that document is
  archived into one flat folder, [docs/archive/specs/](../specs/).

### What the design sentence proposed

That the archive folder be split into `complete/` and `cancelled/`
subfolders, so an archived spec's **location** would answer "did this ship or
get cancelled?" without opening anything.

### What the measurement found (why the row that tried to build it refuted it)

Of the 111 files in the archive today — **all of them exist and their
contents are fine; nothing is broken or missing**:

- **92** attribute cleanly to a work item that completed.
- **3** attribute cleanly to a work item that was cancelled.
- **16 attribute to no single ending at all**, in two ways:
  - 15 are **shared effort documents** — design and research notes that
    served *several* work items at once. One of them is cited from both a
    completed and a cancelled work item, so both folders would be
    simultaneously "correct" for it — which means neither is. "Maps to no
    terminal state" means exactly this: for these files, the question "did
    this end complete or cancelled?" has **no single true answer**, so any
    folder placement would assert something false.
  - 1 has a filename that does not match the pattern the sorting code would
    use to attribute it — an accident of naming, not of content.
- For the 92+3 that *do* attribute, the answer **already exists by
  location** — the work item's own file sits in `complete/` or `cancelled/`
  under [docs/work/](../../work/). The archive split would be a second,
  hand-maintained copy of that fact, with no generator keeping it fresh.

So building the split would force a false answer onto 14% of the corpus to
duplicate an answer the registry already gives for the other 86%.

### What is actually being ruled

Only what the **design text** should now say — the build question is closed
(the row is cancelled under every option). The full decision brief, including
one measured trap for whoever executes it (two declared-absences lines must
be **restated, never deleted**, or the strict reference checker gains two
dangling findings), is OI-11 on the owner surface:
[open-items.html](../../open-items.html).

| Option | What changes | For | Against |
|---|---|---|---|
| **(a) Restate** *(recommended — by the OI brief and by the plan)* | The sentence is amended in place to record the finding: the goal is met by the registry's location; no folder layout can serve the 16 shared documents. | The correction lives where the next reader meets the claim — which is what stops the tidy-up being re-proposed (re-proposal is exactly how the refuted row got filed). | A sentence remains describing something deliberately not done. |
| (b) Strike | The sentence is deleted; the reasoning survives only in the ruling record and log. | Cleanest doc; a design doc describes only the design. | The next person browsing the flat archive re-invents the proposal, with the refutation out of sight. |
| (c) Build anyway | Hand-place the 16 and ship the split. | Real browsing convenience. | Asserts endings that are false for 14% of the corpus; duplicates a registry fact with no freshness gate. |

---

*R1 and R2, for the record: ruled 2026-08-01 as recommended — a work branch
never mints a new work-item id (the refusal rung is row 1 of the
[drain plan](backlog-plan-2026-08-01.md)), and the evidence-cell row builds
the file-existence half only, with the node selector ruled prose.*
