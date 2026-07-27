# Open items — owner decision briefs

The **single owner-review surface**: one section per pending decision, with the
context needed to rule — what's being decided, blast radius, options with
pros/cons, and the driver's recommendation. [status.md](status.md) carries only
the one-line form of each; the DAG rows live in
[work-items.csv](requirements/work-items.csv). **A section lives here only
while the decision is pending** — the ruling appends to [log.md](log.md)'s
Decisions log and the section is deleted. (Format:
[specs/open-items-surface.md](archive/specs/open-items-surface.2026-07-20.md).)

_Ruled items are recorded in [log.md](log.md)'s Decisions log (and the sitting's
GATE audit entry) and their sections deleted per the pending-only rule above — so
ruled history is **not** restated here. The sections below are the currently open
decisions._

---

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

---

## OI-10 — Retire this file in favour of one generated HTML reference view?

- **One-line:** rule whether `open-items.md` is retired outright for a single
  generated HTML owner surface — rec: **yes to the surface, but a generated view
  needs a source; keep per-item markdown as that source**. Kit-wide change with a
  downstream migration.
- **Owner direction (2026-07-26):** *"I would go further and say open-items.md is
  no longer even necessary. A single html reference view is sufficient, the md
  can be retired in its entirety."* The question below is scoped to what that
  costs and what must not be lost with it — the direction itself is the owner's.
- **Decision (owner-raised 2026-07-26, at the first re-attestation sitting):**
  the generated *Pending owner actions* block is a **pointer** — it names
  `trace.py --ratify modified` rather than carrying the amendment. The owner
  read it and could not act from it, which is a fair reading of this file's own
  promise: *"one section per pending decision, with the context needed to rule."*
  The blocker is real and not stylistic: the depth that makes a re-attest
  readable is a **word-level diff** (of a 1,500-character cell, forty words
  moved) — and **markdown cannot express that**. So the question is a format
  question, and it is the owner's.
- **Blast radius — measured 2026-07-26, and it is kit-wide, not local.** This
  file is not just a local surface; it is a **shipped artifact**:
  - `OPEN_ITEMS.template.md` is a `bootstrap.py` MAPPING destination — every
    repo that adopted this kit has a `docs/open-items.md`;
  - **11 references** across the kit's own docs (`PROCESS_OPTIONS.md` ×6,
    `ADOPTING.md` ×2, `README.md`, `STATUS.template.md` ×2);
  - **7 test modules** assert it (`test_gen_trajectory_pending.py` alone has 20
    references), plus one SR / one LLR / one TC row that name it;
  - `agent_dispatch.py` uses it as a **status-map marker** and refreshes its
    pending block each dispatch loop; `check_trajectory.py` keys a rule on it.

  So retiring it is a **kit version bump with a documented migration**, not a
  cleanup. That is not an argument against — it is the price, and it should be
  paid deliberately.
- **The one thing that must not be lost.** This file is **two things wearing one
  name**: a *generated* pending projection (which HTML renders better, no
  argument) and a set of *hand-authored briefs* — blast radius, options,
  recommendation, written by a human or an agent. A generated view needs a
  source. "Retire the md" therefore has to answer: **where does brief prose live
  after this?** Everything else in the decision follows from that answer.
- **Options** (all of them retire this aggregate file as a *reading surface*;
  they differ on the source):
  - **(a) HTML view over per-item markdown sources** — one
    `docs/open-items/OI-N.md` per pending decision, one generated
    `docs/open-items.html`. *For:* prose stays writable, diffable in review, and
    readable by the agents that work from these docs; the generated view is the
    single reference the owner reads; the aggregate file — the thing that is
    genuinely unnecessary — is what disappears. *Against:* still markdown on
    disk, which is not literally "retired in its entirety".
    **← recommended**
  - **(b) HTML view over a CSV registry** — `open-items.csv` beside
    `work-items.csv`, one row per OI. *For:* the purest form of the owner's
    direction; makes OI state queryable, so the pending projection becomes
    derived data rather than a text block; matches the registry→dashboard
    pattern the repo already runs on. *Against:* multi-paragraph options and
    recommendations inside CSV cells is exactly what makes `work-items.csv`
    unreadable raw — it moves the wall of text rather than removing it, and
    every future brief is written into a spreadsheet cell.
  - **(c) Fold OI state into `work-items.csv`** as a row kind. *For:* one
    registry. *Against:* an OI is a *decision*, a WI is *work*; the repo
    deliberately separates them, and merging would blur the DAG's semantics.
  - **(d) Keep the file, add the HTML depth beside it** (the original
    recommendation before the owner's direction). *For:* zero migration.
    *Against:* leaves two surfaces where the owner wants one.
- **Recommendation (recorded):** **(a)**. It delivers what the direction asks —
  one HTML reference view, no aggregate markdown document — while keeping the
  brief prose in a form a human can write, a reviewer can diff, and an agent can
  read. Retiring markdown *as the owner's reading surface* is the win; retiring
  it *as the authoring format* would buy nothing and cost the loop its context.
  Sequence it after the current sitting closes, and ship it with the kit
  migration note.
  Two fixes are worth doing regardless of the ruling: the projected SR line
  should **say** how many chain rows re-attest with it (four lines for six rows
  is correct, but nothing says so), and any rendered view must **print the
  baseline revision** it diffed against — an empty section means *check the
  baseline*, never *nothing changed*.
- **Work item:** [WI-322](requirements/work-items.csv), spec
  [specs/WI-322.md](specs/WI-322.md) — gated on this ruling.

---

<!-- Generated pending-owner-actions projection (WI-234) — do NOT hand-edit; a
     pure view of durable state (blocked rows, refs/llm/conflict records,
     quarantined trains, the NEEDS-HUMAN run-state ask), regenerated by `python
     project-trajectory/scripts/gen_trajectory.py --status` and freshness-gated by
     the harness status-map step. The hand-authored briefs ABOVE this comment are
     byte-untouched by regeneration; each line here is a pointer, not a brief. -->

## Pending owner actions (generated)

<!-- BEGIN GENERATED PENDING -->
_Pending owner actions — a generated projection of durable, committed-tree state (blocked rows with a ratify/attest pointer, Draft/Modified spine rows owing a ratification or re-attest, and the NEEDS-HUMAN run-state ask); regenerated by `python project-trajectory/scripts/gen_trajectory.py --status`, do not hand-edit. This section is freshness-gated by the harness `status-map` step. The briefs above are hand-authored and untouched by regeneration._

- **WI-322** blocked — attest/ratify `OI-10`, then unblock the registry row.
- **SR-049 `Modified` — re-attest owed** (phase 1 pulls the derived gate): Derived gate from artifact states — bless the amendment in a reviewed Status-change commit (`Modified`→`Verified`, or →`Planned` if the evidence no longer verifies the amended text); before/after brief: `python project-trajectory/scripts/trace.py --ratify modified` (a pre-regime streak — amendments that landed while the row stayed Verified — needs `--since <rev>`; committed briefs live in `docs/ratify/`).
- **SR-052 `Modified` — re-attest owed** (phase 3 pulls the derived gate): Dashboard accessibility (rubric-adjudicated) — bless the amendment in a reviewed Status-change commit (`Modified`→`Verified`, or →`Planned` if the evidence no longer verifies the amended text); before/after brief: `python project-trajectory/scripts/trace.py --ratify modified` (a pre-regime streak — amendments that landed while the row stayed Verified — needs `--since <rev>`; committed briefs live in `docs/ratify/`).
- **SR-053 `Modified` — re-attest owed** (phase 3 pulls the derived gate): Dashboard UI uniformity (rubric-adjudicated) — bless the amendment in a reviewed Status-change commit (`Modified`→`Verified`, or →`Planned` if the evidence no longer verifies the amended text); before/after brief: `python project-trajectory/scripts/trace.py --ratify modified` (a pre-regime streak — amendments that landed while the row stayed Verified — needs `--since <rev>`; committed briefs live in `docs/ratify/`).
- **SR-054 `Modified` — re-attest owed** (phase 3 pulls the derived gate): Dashboard usability (rubric-adjudicated) — bless the amendment in a reviewed Status-change commit (`Modified`→`Verified`, or →`Planned` if the evidence no longer verifies the amended text); before/after brief: `python project-trajectory/scripts/trace.py --ratify modified` (a pre-regime streak — amendments that landed while the row stayed Verified — needs `--since <rev>`; committed briefs live in `docs/ratify/`).

_Machine-local advisory — source conflicts, reservations, quarantines, and stranded-train attestations re-derived from `refs/llm/*` as of the dispatch machine at generation time. These refs do not transport with clone/push, so this section is regenerated every dispatch loop and is NOT part of the `--status --check` freshness gate (M-10/WI-266); a second clone (CI, another machine) may show it empty._

_None currently observed on this machine._
<!-- END GENERATED PENDING -->
