# The handback contract — the context an owner ruling needs (2026-08-03)

Written at the owner's request, mid-grind, after three REVIEW-A rounds on
[WI-416](../../work/cancelled/WI-416-dispose-wi-413-handed-back-e56f4e2c201.md) surfaced
a pattern the rounds themselves could not fix. **Nothing here executes until
ruled.** The grind is paused: WI-416 is open and uncommitted, and every row
downstream of it waits on this.

Self-contained for someone who has not lived in the vocabulary. Every number in
it was measured today, and each measurement names the command or file that
produced it.

---

## 1. What the contract is today

A lane that cannot finish **hands back**. `hand_back`
([handback.py](../../../project-trajectory/scripts/handback.py)) does three things to
the work item's own spec file, and nothing else:

1. appends a `## Handback` section to its body — the lane name, the reason, and
   the commit range of the partial work;
2. adds `blockref = <its own path>` to its frontmatter;
3. moves it `active/<branch>/` → `queued/`.

The branch then merges like any other (§A3: every lane ends in a merge, so no
branch dangles). On trunk, `intake.py` sees the merged handback and mints a
**disposition row** of the `adjudication` kind, whose job is to choose one of
R3's four outcomes: cancel / defer / re-queue with drafted follow-up / surface
an open item.

**The whole record of the return lives inside the returned spec.** There is no
separate artifact. `schedule._disposition` reads `queued` + a `blockref` as
`blocked`, which is what keeps the driver from claiming, handing back, and
re-claiming the same row forever.

## 2. Why this is on the table

Seven findings across three independent cross-family review rounds
([reviews/WI-416-REVIEW-A.md](../../reviews/WI-416-REVIEW-A.md)), plus the two rounds
that killed WI-413 before it
([reviews/WI-413-REVIEW-A.md](../../reviews/WI-413-REVIEW-A.md)). The disposition
itself was affirmed every round. Every rejection landed on the *mechanism* for
answering one question:

> Given a returned spec, is a disposition still owed for **this** return?

Five mechanisms have now been proposed and driven. Every one leaked:

| Mechanism | How it failed | Round |
|---|---|---|
| Merge sha in the title | bare sweep uses symbolic `HEAD`; every re-sweep re-mints | the original defect |
| Spec's last-touch commit | any lifecycle edit moves it; shallow/untracked falls back to a moving observer | WI-413 rd 1 |
| SHA-256 digest of the note | note is mutable, not section-bounded; 48-bit truncation collides | WI-413 rd 2 |
| Open-disposition state read (B/B+/B+2) | seven-char title token still authoritative → owed judgement silently dropped | WI-416 rd 1–2 |
| Provenance via `WI-Refs`/`SpecRef` | broad relationship fields, not provenance → unrelated rows **starve** a genuine return | WI-416 rd 2 |

**The common root:** the returned spec is a *mutable, movable, self-referencing*
object, and the return event has no artifact of its own. So every mechanism has
to reconstruct "did a return happen, and was it judged?" from a proxy — git
archaeology, content digests, or field co-occurrence — and every proxy has a
hole. All seven failures are **starvation-class**: an owed judgement silently
not happening.

## 3. The proposal (owner, 2026-08-03)

> Instead of the WI spec updating its own definition with a handback, a lane
> that cannot finish creates a **brand-new handback document**, and at the same
> time **dispositions itself** according to what it was able to complete — so it
> cannot be stranded.

The load-bearing half is the first: **one document per return event**.

## 4. What that dissolves

The seven classes WI-416 recorded as constraints on any future fix
(§2 of its Deliverable), checked against the proposal:

| Class | Under a per-return document |
|---|---|
| **F1** a genuine second return must mint despite a colliding title token | **dissolved** — no derived token exists; the document *is* the event |
| **F2** no re-mint after any of the four R3 outcomes closes | **dissolved** — one document ↔ one disposition, checked against all rows |
| **F3** the shared `_mint` callers must stay intact | **remains** — still a constraint, but easier: nothing needs to bypass title dedup |
| **F4** a suppressor must key off positive disposition provenance | **dissolved** — citing the document *is* positive provenance |
| **F5** a real return does not guarantee a non-empty `blockref` | **dissolved for handbacks** — no blockref needed; see §7, the general defect survives |
| **F6** suppression must never be silent and artifact-free | **remains** — a design principle, not contract-specific |
| **F7** the target spec's path is not durable | **dissolved** — an immutable document never moves |

Four dissolved outright, one for this use, two remaining as ordinary
constraints. *(An earlier verbal estimate of "three" was made against a partial
list; the measured figure against F1–F7 is four.)*

The reason it dissolves rather than mitigates: the proposal supplies **the
immutable per-return-event identity that WI-413's own handback note asked for**
and could not get —

> *a correct fix needs a return-event identity PERSISTED AT HANDBACK TIME*

— achieved structurally, by the document's existence, instead of by adding an id
field to a mutable spec.

## 5. The one correction this doc recommends

**"Dispositions itself according to what it completed" is a judgement, and
belongs to the adjudicator.**

Choosing `complete/` versus `cancelled/` asserts whether the row's goal was met.
A lane that stopped early declaring itself complete is a self-assessment — the
same layering violation as a lane writing `NEEDS-HUMAN`, which is already filed
as [WI-417](../../work/cancelled/WI-417-handback-reason-does-two-jobs.md).

The structure survives intact with one change: **a single terminal state for
"stopped early"** — a `returned/` directory. That is a *fact* the lane can
assert without judging. It is terminal, so nothing strands and nothing
re-claims; the adjudication then decides whether a successor row is minted.

The lane reports what happened. The adjudicator decides what it means.

## 6. The surface a change would touch — measured

Smaller than it looks, because `blockref` and the handback definition are
separable.

| Surface | Measured | Note |
|---|---|---|
| Code reading the `## Handback` **section** | 8 sites / ~4 distinct behaviours | writer `handback.py:167`; sweep trigger `intake.py:873`; reason reader `intake.py:476`; note-stripper duplicated 3× by the F5 copy rule (`agent_common.py:788`, `check_trajectory.py:491`, `schedule.py:364`) |
| `blockref` | 47 sites / 12 files | **general mechanism, not handback-specific** — predates handback, serves any blocked row, would stay |
| Tests specific to handback | 15 in `test_handback.py`; 12 named across the suite | not the 579 in files that merely mention the word |
| Status directories | 6 declared | `draft, queued, active, deferred, cancelled, complete→done`; terminal = `done, cancelled` |

*(Produced by `grep -rn SPEC_HANDBACK project-trajectory/scripts/*.py`, `grep -c
blockref` per file, `grep -c "def test_" tests/test_handback.py`, and
`schedule.SPEC_STATUS_DIRS` / `agent_common.TERMINAL_STATUSES`.)*

## 7. What the ruling would force

1. **Amend R3.** Its "re-queue" outcome mutates the returned row back onto the
   frontier. If the row is terminal in `returned/`, continuing means **minting a
   successor**, not unblocking. That is arguably more R3-consistent — intake
   mints from the adjudication's draft, and lanes never mint (R1) — but it
   retires a ratified outcome, which is an owner call.
2. **Amend §A3's handback row** in [concurrency-v2.md](../../concurrency-v2.md) — the
   terminal-outcomes table names `queued/` (or `draft/`) plus a blockref.
3. **Declare `returned/`** in `SPEC_STATUS_DIRS`, `_TERMINAL_DISPOSITION` (or
   `_NEVER_READY`), the loaders, and the dashboard views.
4. **Successor lineage** must be explicit, or partial work loses its thread
   across the id change.
5. **The two already-drafted follow-ups stay valid either way.** The
   `blockref = ""` producer defect still affects ordinary blocked rows, and the
   `spec_move` stale-`specref` defect was driven to break the **ordinary claim
   path**, not just handbacks.

## 8. A constraint discovered while writing this

**The handback document must not be a `WI-*.md` file under `docs/work/`.**

`agent_common.spec_files` is `work_dir.rglob("WI-*.md")` filtered only on "not
directly in `work_dir`". So a report at `docs/work/handbacks/WI-nnn-<branch>.md`
*would* be walked, `parse_spec_status("handbacks")` would raise, and
`read_spec_rows` would silently skip it — the exact §B3 invisible-spec trap that
made `draft/` a declared directory, and worse here, because `intake.next_wi_id`
counts filenames and would have treated the report's id as TAKEN.

**Ruled, and shipped as SR-144:** the reports live at
[`docs/handbacks/`](../../handbacks/README.md), outside `docs/work/` entirely, which
avoids the question rather than answering it. That directory's
[README](../../handbacks/README.md) states the two rules the design rests on — never
edit a report, never delete one — and why the terminal
[`docs/work/partial/`](../../work/partial/) state is its other half.

## 9. Migration

**One file.** `grep -rl "^## Handback" docs/work` returns exactly
[WI-413](../../work/cancelled/WI-413-bare-sweep-re-mints-open-dispositions.md) and
nothing else. Whatever is ruled, the migration is a single hand edit — the same
measurement that made the *old* fix's migration question a non-issue.

## 10. What the ruling must answer

1. **Per-return document: yes or no?**
2. **`returned/` as a single terminal state, or the lane choosing
   `complete`/`cancelled`?** (§5 argues for the former.)
3. **Does R3's re-queue outcome retire in favour of minting a successor?**
4. **Where do handback documents live?** (§8 constrains this.)
5. **What happens to WI-413?** It is currently re-queued in the working tree
   against the *old* contract. If the contract changes, its brief is moot and
   the honest disposition is defer.

## 11. What executes if ruled

- WI-416's disposition is re-decided in light of the ruling and its review round
  re-run; the tree is uncommitted, so nothing needs unwinding.
- WI-413 is re-scoped or deferred.
- [WI-417](../../work/cancelled/WI-417-handback-reason-does-two-jobs.md) is checked
  against the ruling — its judgement (2) asks whether a handback reason is
  constrained at all, which a per-document contract reopens.
- The `## Dispositions` drafts already written into WI-416 are minted by the
  machinery at its close, unchanged — both defects are real under either
  contract.
- The kit's own spine (`SR`/`LLR`/`TC`) rows describing the handback contract
  are amended in the same window as [WI-390](../../work/queued/WI-390-concurrency-v2-program-close.md)'s
  program close, per §A4's one-sitting rule.
