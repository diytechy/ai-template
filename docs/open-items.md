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

## OI-10 — Should the pending projection carry the before/after, and in what format?

- **One-line:** rule the format for re-attest depth on the owner surface —
  rec: **HTML companion generated beside the markdown brief**, markdown stays
  the decision record.
- **Decision (owner-raised 2026-07-26, at the first re-attestation sitting):**
  the generated *Pending owner actions* block is a **pointer** — it names
  `trace.py --ratify modified` rather than carrying the amendment. The owner
  read it and could not act from it, which is a fair reading of this file's own
  promise: *"one section per pending decision, with the context needed to rule."*
  The blocker is real and not stylistic: the depth that makes a re-attest
  readable is a **word-level diff** (of a 1,500-character cell, forty words
  moved) — and **markdown cannot express that**. So the question is a format
  question, and it is the owner's.
- **Blast radius:** the owner review surface itself, plus one generator and one
  freshness gate. Nothing in the spine or the loop depends on the answer. But
  the choice sets a precedent for every future owner-facing depth view, and
  option (c) in particular adds a *second* render surface under the perceptual
  gate, which is the expensive kind of yes.
- **Options:**
  - **(a) Markdown, deeper.** Inline the per-cell before/after into the
    generated block. *For:* one file, one format, no new machinery. *Against:*
    it IS the wall of text — six amended rows, some cells 1,500 characters, no
    way to mark what moved. This is what the sitting already rejected.
  - **(b) An HTML companion beside the brief** — `trace.py --ratify --html`
    writes `docs/ratify/<date>-reattest.html`, the markdown block and
    `status.md` each link it once. *For:* the brief is already the artifact
    whose one job is before/after, so it gains a format rather than the repo
    gaining a surface; word-diff, collapsible unchanged runs, both themes; zero
    new dependency (stdlib string work, same comparison already implemented);
    it is **not** a render surface, so it never re-reds `perceptual-stale`.
    *Against:* a second file per sitting, and a generated HTML file to keep
    fresh. **← recommended**
  - **(c) Fold it into `PROJECT_STATE.html`.** *For:* one HTML surface for the
    whole repo, themes and freshness already solved. *Against:* it grows
    `gen_trajectory.py`, which is 5,236 lines and under a size ratchet with its
    decomposition (WI-280) still pending; and every edit to it re-reds the
    perceptual gate, so a typo fix in an attestation panel would cost a
    critique dispatch. The dashboard is a *project-state* surface; a sitting
    brief is a *point-in-time* record with a different lifecycle.
  - **(d) Rule it out of scope.** Keep the pointer; the owner reads the brief in
    an editor. *For:* zero work. *Against:* the sitting just demonstrated the
    cost, and the stale-brief defect found the same day
    (see [log.md](log.md)) shows the pointer's other failure — nobody notices a
    brief has gone stale when nothing renders it.
- **Recommendation (recorded):** **(b)**. It puts the depth in the artifact that
  already owns before/after, keeps markdown as the decision record, and buys the
  legibility without touching the render surface or the dashboard's ratchet.
  Whatever is ruled, two fixes are worth doing regardless: the projected SR line
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
