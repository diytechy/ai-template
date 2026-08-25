## 2026-08-24 — WI-483 slice 7: the layering measured rather than assumed, `check.steps` decided, and the row closed

**Summary.** The row's last two owed items, both of which were DECISIONS rather
than techniques, and neither answer is the one the spec predicted. Item 1: the
surviving `integrate -> intake` edge was re-measured and is a **downward** call
— the word "upward" was inherited from the cycle era and has been false since
slice 2 — so program shape item 4 was already true and what the slice ships is
the **instrument that was missing**, `LIFECYCLE_RANK` plus a strict-descent
rule, mutation-checked three ways. Item 3's remainder, `check.steps`, is
**LEFT**, on four recorded grounds and with the observation that leaving it is
not unguarded. `WI-483` closes; the size ratchet's debt owner moves to `WI-508`
so the close does not recreate the very defect (H-05) the row's first act fixed.

Deferred open items: none — neither decision changes an owner-visible contract.
No module moved, so no MAPPING/spine/RESYNC/seam surface changed and no
`Approved` cell is rewritten anywhere in the diff. No ratchet was re-stamped in
either direction: `integrate.py` is net-zero at 2,597 lines.

### Item 1: the measurement, and what it refuted

The spec had called `integrate -> intake` "a real upward call" for two slices.
Read off the same walker the ratchet uses, the lifecycle band's entire edge set
is:

| edge | kind |
| --- | --- |
| `dispatch -> handback`, `lane`, `integrate`, `intake` | module-level |
| `handback -> integrate` | module-level |
| `lane -> integrate` | module-level |
| `integrate -> intake` | deferred (the post-merge mint at the held slot) |
| `intake -> ` *(nothing in the band)* | — |

fig: `import_graph()` from `tests/test_import_layers.py`, restricted to
`LIFECYCLE`, at `14759fc8`.

That is a strict total order: `dispatch` 0, `handback`/`lane` 1, `integrate` 2,
`intake` 3. `intake` imports no lifecycle module at all, which is the definition
of the bottom. The "above" reading was true only while `intake -> dispatch`
existed and put intake above `integrate` THROUGH THE CYCLE — **slice 2 cut that
edge and the sentence beside the call site was never re-derived.** It is the
same class of defect as `handback.py`'s "never the reverse", which is one of the
two prose drifts the 2026-08-19 review opened this program with, and it is
corrected in place.

### The decision: KEEP the edge, `integrate.py merge` UNCHANGED

Recorded in the spec file too, because the row is `safety_class = spine`. The
three alternatives and why each is worse:

- **Hoist the mint into `dispatch`.** The mint must run inside the HELD merge
  slot — serial by construction, all-or-nothing on one trunk commit (rulings
  R1/R3). Above `integrate` it runs after the slot is released, unless lock
  acquisition moves up out of `_slot`, whose docstring names itself the one
  acquisition site "and it must stay that way (§A2.0 requirement 1)".
- **Inject the hook** (`integrate_one(..., after_merge=…)`). Either
  `integrate.main` supplies the default, in which case the import edge moves up
  one function and the graph is byte-identical — a cosmetic fix — or it does
  not, in which case a human's `integrate.py merge` lands the merge and
  **silently mints nothing**. That is an owner-visible contract change trading a
  correctness hazard for one graph edge, and the edge was not pointing the wrong
  way to begin with.
- **Move the mint family down.** `intake_after_merge` reaches `_amendment_
  drafts`, `_close_drafts`, `_disposition_drafts` and `_mint` — most of
  `intake.py`. Moving it below `integrate` is renaming the module.

`integrate_one` composing "merge, then mint" is not a second composer: it is
what taking the slot MEANS. `dispatch` stays the only module that sequences
lifecycle services against each other.

The import **stays deferred**, and its reason is now stated honestly rather than
as a layering claim: it keeps a plain `integrate.py claim` — the hot path of
every lane run — from paying the mint family's import (`trace`,
`check_trajectory`, `census`, `schedule`, `baseline_snapshot`, `wi_convert`).
It hides nothing, because every rule in `test_import_layers.py` reads function
bodies.

### What shipped: the rule that was missing

The ratchet file's own comment said it: *"this file's `test_a_view_never_imports
_a_lifecycle_service` is the only rule policing direction today"*, and
`integrate` is not subject to it. So "an acyclic tangle is still a tangle" was
untested, and program shape item 4 lived in a spec file with nothing measuring
it.

`LIFECYCLE_RANK` declares the order; two tests hold it:

- **`test_the_rank_map_covers_the_whole_lifecycle_band`** — the ranks must equal
  `LIFECYCLE` exactly, so a new lifecycle module forces a placement instead of
  being silently exempt from the direction rule. That is the same hole
  `MAX_INTRA_CYCLE_EDGES` closes for `CYCLES`.
- **`test_a_lifecycle_edge_never_points_up`** — every intra-band edge points
  STRICTLY down. Strict, not `>=`: an edge between two equal-rank peers means
  one of them is really above the other and nobody has said which.

**Mutation-checked, three ways, not asserted:**

| mutation | cycle tests | new rule |
| --- | --- | --- |
| deferred `intake -> integrate` (an inversion) | RED | RED |
| deferred `lane -> dispatch` + `lane -> handback` (the 2026-08-21 review's own) | RED | RED |
| deferred `handback -> lane` (SIDEWAYS, two peers) | **GREEN** | **RED** |

fig: each probe appended to the named script, `pytest -q
tests/test_import_layers.py` run, `git checkout --` reverted; the working tree
was confirmed clean between probes.

The third row is the point. A sideways edge forms no cycle, so `CYCLES` is
byte-identical and the density count sees no component to be inside — both
existing ratchets report success while the band de-layers. The re-ranking
escape is closed the way this repo closes them: the docstring says editing
`LIFECYCLE_RANK` to clear a finding IS accepting what it measures.

The walker self-test's pin stays on `integrate -> intake`, and its docstring
changes from "it will move exactly once more" to a stable pin — the edge is
ruled kept, so the pin is no longer a countdown against the program.

### Item 3's remainder: `check.steps` is LEFT

Re-measured before deciding: **649 lines** (628 at slice 4 — it drifted +21
unnoticed), **complexity 8**, and **350 of the 649 lines are comment**, 299
code.

fig: `wc -l` + `python -m ruff check --select C901 --config
"lint.mccabe.max-complexity=1"` over `project-trajectory/scripts/check.py`, plus
an `ast` span/comment count of the `steps` node, at `14759fc8`.

Four grounds:

1. **Not debt on this program's axis.** The owner's `OI-16` correction — the
   monolith risk is FUNCTION COMPLEXITY, not file length — is quoted by the size
   ratchet's own docstring and by slice 4. `steps` measures 8, under the limit
   and BELOW three functions in the same file nobody proposes splitting
   (`approval_immutability` 10, `staged_divergence` 8, `run_plan` 8). Splitting
   the long flat one while leaving the branchy short ones is length-chasing,
   which is the axis the owner disputed.
2. **The bulk is RATIONALE.** 54% comment: which rung each check arrives at and
   why. A split relocates comments.
3. **The list's ORDER is load-bearing and reads top to bottom today** — *"Listed
   before traceability so at `--gate all` the fuller report.md wins"*. Per-band
   helpers would distribute that ordering across call sites.
4. **The data-file carrier already exists and is deliberately partial.** An
   adopter adds steps via `docs/stack.ini` `[step:<name>]` and overrides the
   three product commands there; the PROCESS floor stays in code, where a
   profile cannot edit it away. Moving that floor into data hands the assurance
   floor to the file the project owns.

**And leaving it is not an unguarded state**, which is what makes this a
decision rather than a shrug: `tests/test_complexity_ratchet.py` compares the
C901 census for EXACT equality, so a function absent from the baseline that
crosses the limit reds. The day `steps` stops being a flat declaration it fails,
with no new instrument. A second sensor for one function would duplicate an
armed one, so none was added.

### Item 4 (M-06): rides nothing, and is named unfinished

Nothing was decomposed here, so nothing needed splitting. The four monoliths,
re-measured against the review's figures:

| module | review 2026-08-19 | today |
| --- | --- | --- |
| `tests/test_integrate.py` | 3,495 | **3,520** |
| `tests/test_trace.py` | 1,826 | **2,099** |
| `tests/test_trajectory_arch.py` | 1,412 | **1,927** |
| `tests/test_agent_loop.py` | 1,567 | **1,640** |

fig: `wc -l` at `14759fc8`.

Item 4's own rule held for all seven slices — a split rides along with a
subsystem decomposition; a standalone split slice is out of scope — and each
slice checked its touched tests and found none needing one. So the four are
**unsplit at close, deliberately**, and they belong to the next subsystem
decomposition (`WI-508`).

**FINDING, left for its own row rather than fixed here** (working agreement: a
design smell is surfaced, not fixed inline). `tests/test_module_size_ratchet.py`
censuses `SCRIPTS` only, so **no armed sensor watches the test tree grow** —
which is why three of these four gained 5-36% since the review recorded them and
nothing said so. Whether the census should extend to `tests/` is a real
question, not a drive-by: the ratchet's own docstring already banks an unruled
owner question about whether the line axis survives at all.

### The debt owner moves to `WI-508`

This row's FIRST act was re-pointing `tests/test_module_size_ratchet.py` away
from the closed `WI-280`, on H-05's finding that "a ratchet whose commentary
names a closed item tells the next author that the debt is somebody's when it is
nobody's, which is the one thing a growth sensor must not do". Closing `WI-483`
while it is named there recreates that defect exactly, so the pointer moves in
the same commit: `WI-508` is the live architectural-remapping program, it
`needs` this row, and its declared output is consolidation WIs filed against
exactly this residue. Three live pointers moved (the module docstring, the
BASELINE header, the failure message) plus the two in
`tests/test_import_layers.py`; the **dated per-entry bump notes are NOT
re-pointed**, for the reason that file already states — rewriting a dated record
to cite an item that did not exist on its date would falsify it.

### What the row delivered, end to end

7 modules / 12 intra-cycle edges → **0 / 0** over a graph that includes
function-body imports; the band layered and asserted; the `gen_trajectory`
facade at zero importers; five read models extracted below their readers
(`kitlib/station.py`, `census.py`, `pending.py`, `coherence.py`); four
complexity-baseline entries DELETED (`trace.analyze` 50, `agent_loop.main` 27,
`session_bookkeeping` 31, `run_iteration` 20); four attribute bags typed, two of
them frozen and total, which exposed a dead field and two defaulted `getattr`
reads that would have silently meant "human-held, don't keep going".

### Gates

```
python -m pytest -q -n auto -m smoke   -> 1325 passed, 5 skipped in 23.28s
python scripts/check_smoke_budget.py --mode enforce
                                       -> 21.3s vs 60s budget -> within
python project-trajectory/scripts/check_docs.py --root . --stale
                                       -> OK, 1071 docs, 1393 links, 0 broken
python project-trajectory/scripts/check_trajectory.py --root . --strict
                                       -> clean (515 WIs, 488 done, graph acyclic)
python project-trajectory/scripts/gen_trajectory.py --root . --check
                                       -> dashboard up to date
python project-trajectory/scripts/gen_open_items.py --root . --check
                                       -> open-items view up to date
python -m ruff format --check / check   -> formatted; 2 lint errors, BOTH PRE-EXISTING
```

**THE FULL SUITE WAS RUN BATCHED, AND THE BATCHING IS THE HONEST PART.** The
unfiltered run exceeded this session's 600 s per-call ceiling twice, so it was
split along the tier boundary (`smoke` + `slow` are TOTAL by construction —
`conftest.smoke_tier_for` maps every test to exactly one) and the slow half into
seven groups. **Coverage was VERIFIED rather than assumed**: `pytest -q
--collect-only` reports **3029** tests (1330 smoke / 1699 slow), and the batch
results sum to exactly 3029 with **zero failures**.

```
-m smoke                                       1325 passed,  5 skipped  100.42s
pre_push_hook bootstrap onboard_devsetup
  profile stack_profile                         152 passed,  4 skipped   68.78s
pre_commit_hook (ALONE — see below)              19 passed                69.00s
check_perf check_flows meta_repo_hook
  old_kit_resync dual_plan_round integrate       179 passed,  1 skipped  241.47s
dispatch handback gen_trajectory traj_*
  gen_trajectory_pending gen_okf                 258 passed              313.71s
agent_loop* session_stdin                        223 passed,  1 skipped  135.40s
trace* check_docs registry_checks
  check_privacy check_harness check_stubs        304 passed,  2 skipped  119.01s
trajectory* components_registry modules_registry
  spine_rules derive_stage phase_rule
  stage_event_detectors_driven
  selection_at_or_above                          300 passed               79.62s
ac_advisory perf_budgets procurement
  gen_release_checklist assets gen_arch_map
  gate_policy run_menu prereq_toolchain
  launcher_interpreter external_frame
  baseline_snapshot adjudicate_brief intake      255 passed,  1 skipped  113.78s
                                               ----------------------------------
                                                3015 passed, 14 skipped = 3029
```

fig: each line is one `python -m pytest -q -n auto --basetemp=D:\tmp\…`
invocation on this tree (`--basetemp` off C:, which has the least headroom);
the totals line is the sum, checked against `pytest -q --collect-only`.

### Two findings surfaced while running, neither fixed here

Both are pre-existing and outside this row's scope, so they are surfaced rather
than repaired inline (the working agreement).

1. **`tests/test_pre_commit_hook.py` cannot be run in an xdist BATCH with other
   modules** — it errors at import with `ModuleNotFoundError: No module named
   'kitlib'`, while passing cleanly alone (19 passed) and inside the full
   unfiltered run. Some other module's `sys.path` setup is what makes it
   importable, so the module has an undeclared collection-order dependency. This
   matters precisely because batching is the documented workaround for this
   box's time/disk constraints: the batch that hides it reports `1 error` where a
   whole-suite run reports green.

   fig: reproduced identically on `git stash`ed HEAD with the same file list, so
   it is not this slice's doing; and reproduced twice on this tree.

2. **No armed sensor watches the test tree's size.**
   `tests/test_module_size_ratchet.py` censuses `SCRIPTS` only, which is why
   M-06's four monoliths grew 5-36% since the 2026-08-19 review with nothing
   saying so. Whether the line-count census should extend to `tests/` is a real
   question, not a drive-by — that file's own docstring already banks an unruled
   owner question about whether the line axis survives at all.
