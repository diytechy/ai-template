## 2026-08-21 — WI-498, the stage unification program: per-slice record

The owner's directive (2026-08-21): roll through the ruled plan's slices
0–5 in series (opus for the design-bearing slices, sonnet where
mechanical), each slice ending green at the commit bar. Spec-of-record:
[../plans/2026-08-21-stage-unification-plan.md](../plans/2026-08-21-stage-unification-plan.md)
(v1 FINAL); the OI-51 ruling is its authority. One section per slice as it
lands; adjacent findings accumulate at the bottom.

Deferred open items: none yet — declarations accumulate per section; this
top-matter line is re-derived at each close.

### Slice 0 — one enum home (opus worker) — LANDED

The eight-rung `DevStg-*` ladder moved to **`project-trajectory/scripts/kitlib/ladder.py`**:
the rung labels, `STAGE_ORDER`, the derived `STAGE_OF`, `STAGE_DESC`,
`LADDER_RUNGS`, and `stage_ord`. `derive_gate` re-exports every name under its
former spelling (six modules and the suite already read `derive_gate.STAGE_*`;
re-pointing every citation is churn this slice does not need), `agent_common`'s
`LADDER_RUNGS` literal and `traj_status`'s `_STAGE_LABELS` bind to the shared
objects. No derived value moved: `docs/gate`'s `# basis:` line is unchanged
except for the row counts the mint below adds.

**Why `ladder` and not `stage`.** It is the word the repo already uses for this
table (`LADDER_RUNGS`, `tests/test_stage_ladder.py`, process.md §4 "The stage
ladder"), so no new term enters the lexicon; it leaves `stage` free for slice
1's derivation-and-reader module (plan §2 names "the kitlib stage module" for
the declared input set, the fingerprint and the common reader), keeping pure
vocabulary strictly below the thing that derives over it; and `stage.py` beside
`station.py` is a confusable pair a package this small should not create. The
module imports **nothing at all**, not even stdlib — the strongest form of the
kitlib import-discipline rule, asserted from its own AST.

**Pins retired, and the warrant.** `tests/test_ratification_level.py`'s
`assert ac.LADDER_RUNGS == set(dg.STAGE_ORDER)` is gone: both names now resolve
to one object, so "the copies agree" cannot fail, and a test asserting a
frozenset equals itself is vacuous rather than weak. Replaced by identity
assertions (`is`) — the WI-448 precedent verbatim (`tests/test_rule_sync.py`,
"the declared-line reader: WAS 5-way, now ONE home"). The `DIAL_HOLDS`
containment half survives: it is a hand-authored mapping, not a copy.

**A FIFTH definition home the design-record §3 inventory missed**, found while
executing: `traj_status._STAGE_LABELS` was a byte-identical copy of `STAGE_DESC`
pinned by **nothing**. Worse place than the pinned ones — a reworded or inserted
rung would have shown the dashboard the old sentence, or dropped the stage
bullet entirely (`stage in _STAGE_LABELS` degrades to bar-only wording), with
every test green. It now imports `kitlib.ladder` **directly**, not through
`derive_gate`: a render leaf should not load a 1,400-line derivation engine for
eight strings (the WI-483 `station` direction).

**`check_vocab` needed no change** — a deviation from the slice brief, which
expected restatements there. Inspected: its only `DevStg-*` occurrences are the
`ALIAS`/`GATE_ALIASES` tables mapping *retired* spellings to current ones
(migration shims, explicitly in scope to keep) and prose. It restates no live
enum, so there was nothing to import.

**Spine mint, and it drags no bar.** `check_trajectory --strict` refused the new
module as owned by no component. Minimal honest resolution was a Drafted mint,
not an amendment: appending `ladder.py` to LLR-181's cell would have put it
under the four-way usage tag LLR-182 explicitly refuses (it suppresses the
cross-component seam rule on the new edges), and LLR-157 — the row that owns the
stage axis — is **Approved** and not a worker's to touch. So **LLR-184**
(single tag `CMP-006`, the component that decides the stage's meaning; a
consumer reading a table does not own it) + **TC-179**, watermark bumped by
`trace.py --bump-ids` (LLR 183→184, TC 178→179). Evidence it dragged nothing:
the gate read `computed=DevStg-Below … phase=5 per-phase=…5=DevStg-Below
stage=DevStg-Reqs` before the mint and reads the same after — phase 5 was
already floored by 9 existing drafts.

**Scaffold-verified, per the standing lesson.** Bootstrapped a real scaffold and
ran the shipped scripts in it: `kitlib/ladder.py` arrives; `derive_gate` writes
`stage=DevStg-Needs stage-ord=0 stage-of=8`; `check_vocab` clean; `trace` clean;
`agent_common.human_holds` resolves the rung set (and still holds an unknown
rung — the conservative direction); `traj_status._stage_line` renders
"stage 3 of 8, architecture (partition) in work" from the shared table.

**Ratchets re-stamped deliberately.** `bootstrap.py` 2920→2926 (the MAPPING row
+ its reason comment; a manifest growing). `agent_common.py` 2414→2412
(re-stamped DOWN). `derive_gate.py` **entry deleted** — it fell 1531→1424, below
the 1500 threshold, exactly as its own note predicted ("a re-stamp downward if
the stage-axis half is ever extracted"); a tombstone comment records why.
Smoke membership 1306→1315 for the six new in-process tests (measured 1307).
**The 60 s seconds budget was NOT moved** — see the breach note below.

Adopter-facing: RESYNC_PACK entry `kitlib/ladder.py — the eight-rung stage
vocabulary gets one home [since f23e6002]`, plus the kit-contents README row and
the package docstring's themed-module list.

Gates, real output on this box:

- `python -m pytest -q -n auto` (full, unfiltered) → **2755 passed, 14 skipped
  in 592.38 s**. The run BEFORE this one is worth recording rather than
  overwriting: **2753 passed, 14 skipped, 2 failed in 597.76 s**, and both
  failures were mine and both were the guards doing their job — the smoke
  membership ratchet (re-stamped above) and `check_vocab` refusing the retired
  `G*` tags my new test quotes as INPUTS. The second was fixed by marking the
  offending lines `check_vocab: allow`, which is that check's documented escape
  for a line that must name the retired vocabulary, not a sanction: the tags
  are the arguments `stage_ord` is being proven to reject.
- `python -m pytest -q -n auto -m smoke` → **1302 passed, 5 skipped in
  72.84 s** (on the final tree; an earlier mid-slice run read 1296 / 86.04 s).
- `python project-trajectory/scripts/check_docs.py --root . --stale` → **OK —
  978 doc(s), 1350 intra-repo link(s), 0 broken (1 orphan warning)**.
- `python project-trajectory/scripts/check_trajectory.py --root . --strict` →
  **clean (495 work item(s), 461 done (93%), 21 cancelled, graph acyclic)**.
- `python project-trajectory/scripts/trace.py --root . --strict-integrity` →
  see the close line below.
- `python project-trajectory/scripts/check_vocab.py --root . --strict` →
  **clean (455 live authored file(s); no retired gate tags)**.

**Smoke wall-clock breach, reported not absorbed:** 72.8 s (and 86.0 s on the
mid-slice run) against the declared 60 s. CLAUDE.md already records 54.9 / 64.0
/ 55.7 s on this box on 2026-08-20, so the tier was already at the ceiling
before this slice; one box is one data point and the budget is not moved to fit
it. OI-52's execution row owns that decision.

Deferred open items: none — the component-ownership question this slice brushed
is already OI-48 (ruled (d), execution queued as WI-494), and the smoke wall
clock is already OI-52's; neither is a new decision owed.

### Slice 1 — derive_stage + docs/stage + the common reader (opus worker) — LANDED

The stage axis gets its own derived file, its own producer, and the reader the
ruled plan §3 asks for. **`docs/gate` is untouched and still authoritative for
every one of its readers** — the transitional dual state the plan specifies;
slice 2 cuts them over.

**The module boundary, which is this slice's real design decision.** `kitlib`
may import no sibling, and the derivation needs `spine_carrier` plus ~600 lines
of rung logic that slices 2 and 3 REWRITE. So the split is by PURITY, not by
subject:

- **`kitlib/stage.py`** — the DECLARED input list (stated once), the
  fingerprint, the `docs/stage` format, the ordering that admits the per-phase
  sentinel, the `require_rung` guard, the floor, the per-phase fold, and
  `read_stage`, the common reader.
- **`derive_stage.py`** — the half that needs the carrier: it calls
  `derive_gate.load_spine` and `derive_gate.spine_stage` rather than restating
  the predicates, so **slice 3 re-discriminates the ladder by editing ONE
  fall-through and both files follow**.

The reader takes `derive` as an **argument** — not a lazy import, not a module
global. The alternative considered and rejected was moving the derivation into
`kitlib`: it would drag the registry-parsing graph into the scaffolder's one
import, and it would move code that is about to be rewritten, which is the same
argument slice 0 gave for leaving the bar axis alone. `derive_stage.read()` is
the one-line wiring every production consumer will call in slice 2.

**The effective stage, and the one place the design could have gone wrong.** It
is the min over the phases that have EARNED a rung, then floored to
`DevStg-Reqs`. Two decisions carried the weight. **Min, not max**: a max over
phases is a high-water reading, and process.md §4 rules that one may only be
shown BESIDE the honest value — a settled phase 1 must not let the repo report
"nothing in work" while phase 5 drafts. **Phases with nothing settled are
IGNORED, not folded as the sentinel**: that is where the draft collapse actually
stops, since folding a new phase's sentinel in would drop the repo to the floor
on the arrival of one draft — C-01 reproduced on the new axis, which is exactly
what the slice existed to prevent. The floor is a SELECTION guarantee, not a
claim: `live-stage=` carries the honest unfloored reading and `floored=yes` says
plainly that the two differ.

**The file is key=value, not positional** — a deliberate break from
`docs/gate`'s "first non-comment line" idiom, which is re-implemented in five
readers and silent on mis-order. Fields: `stage` / `stage-ord` / `stage-of` /
`floored` / `settled-stage` / `live-stage` / `phase` / `per-phase` /
`per-phase-live` / `drafted` / `fingerprint`, with the as-of revision in an
uncompared stamp (comparing it would report the file stale the instant it was
committed). This repo reads **`stage = DevStg-Arch`** with
`live-stage = DevStg-Reqs`, `drafted = 15`, every phase at Arch — the two
inserted frame rungs are repo-global and currently dominate (see the findings).

**All nine corner cases from the deep-check are driven, and each is an
acceptance test rather than a nicety.** `tests/test_kitlib_stage.py` (26 tests,
in-process, in the commit bar) carries the five that are properties of the
carrier: the sentinel's ordering, the truncation refusal, the cross-ladder
refusal, the mid-process input change, the CRLF invariance — plus
reader-never-writes and a COUNTED fast path proving the fingerprint actually
skips the derivation. `tests/test_derive_stage.py` (15 tests) carries the four
that need real rows: the draft drop (in-phase and new-phase), the per-phase
reading with a defined global over it, the fresh scaffold, and the claimed-branch
lane. Two honest limits are written into the tests rather than glossed: the three
spellings the retired bar vocabulary SHARES with this ladder cannot be separated
by any value-level guard, and what contains them is carriage (distinct keys in
distinct files) until slice 2 deletes the other axis.

**Scaffold-verified, per the standing lesson.** Bootstrapped a real scaffold:
`kitlib/stage.py`, `derive_stage.py` and the `docs/stage` placeholder all
arrive; `--check` passes the placeholder with a note (so a fresh scaffold stays
green — `ci/check.yml`'s promise); deriving there writes
`stage = DevStg-Reqs floored = yes live-stage = DevStg-Needs`, which is the
fresh-scaffold corner defined rather than raising; editing an input under the
reader made it return `derived` instead of `recorded` and left the file
byte-identical; and `--check` then reported STALE, exit 1.

**Ratchets re-stamped deliberately, and one refused.** `bootstrap.py` 2926→2946
and `check.py` 2320→2337, both declaration-only, reasons on the entries.
Smoke membership 1315→1342 for the 26 in-process carrier tests — and the same
slice filed `test_derive_stage` into `conftest.SLOW_MODULES` beside
`test_derive_gate` (it is scaffold-and-subprocess work of exactly that class),
which is what shows the stamp is not budget-shopping. **`test_complexity_ratchet`
fired on `kitlib.stage.parse` at 11 and was answered by DECOMPOSITION, not a
baseline entry** — `_refuse_non_rungs` split out, because reading a key=value
block and judging what the values may say are two jobs.

**`derive_gate.py` re-enters the module-size baseline at 1503, one slice after
slice 0 deleted its entry for falling under — and the sequence is worth keeping
because it is the ratchet nearly being gamed.** It measured 1502 mid-slice; a
genuinely dead return key came out (`sn_path`, which nothing read) and it landed
at EXACTLY 1500, which PASSES. Trimming to a threshold is the ratchet inverted,
so it was recorded as a near-miss rather than banked — and then `ruff format`
settled the question by taking it to 1503 on its own. The honest reading is that
the module is over the line: it still holds the whole bar axis. The
decomposition the ratchet wants is already scheduled and is a DELETION — slice 2
removes that axis — so the entry says re-stamp down there rather than trim here.
What grew is a SHARED SEAM, not a feature: `load_spine` (so `derive_stage` reads
identical rows by identical rules) and `spine_stage`'s `cited_srs` (so the same
fall-through is callable per phase).

Spine: **LLR-185** (`kitlib/stage.py`) + **LLR-186** (`derive_stage.py`), both
single-tagged `CMP-006` under `SR-139` following slice 0's LLR-184 precedent,
with **TC-180**/**TC-181**; watermark bumped by `trace.py --bump-ids`
(LLR 184→186, TC 179→181). No Approved row amended. Adopter-facing: a
RESYNC_PACK §3 entry (with the regenerate-don't-preserve directive `docs/gate`
already carries), three `bootstrap.py` MAPPING rows, the `[generated]`
declaration, the `WIRED` enforcer row, the README kit-contents prose, the
ADOPTING first-green-run list, and the §9.1 step table.

Gates, real output on this box:

- `python -m pytest -q -n auto` (full, unfiltered) → **2798 passed, 14 skipped in 644.25 s**
- `python -m pytest -q -n auto -m smoke` → **1330 passed, 5 skipped in 51.31 s**
  on the final tree. Three readings were taken across the slice and the SPREAD
  is the honest figure, not the best of them: **51.3 / 62.9 / 55.0 s** — the
  tier straddles its own ceiling on this box run to run.
- `python project-trajectory/scripts/check_docs.py --root . --stale` → **OK —
  978 doc(s), 1350 intra-repo link(s), 0 broken (1 orphan warning)**.
- `python project-trajectory/scripts/check_trajectory.py --root . --strict` →
  **clean (495 work item(s), 461 done (93%), 21 cancelled, graph acyclic)**.
- `python project-trajectory/scripts/trace.py --root . --strict-integrity` →
  **SN=27 SR=73 LLR=168 TC=164 orphans=15 integrity=0 components=4
  component-findings=0 interfaces=130 interface-findings=0**.
- The pre-commit floor (13 steps incl. the new `derived-stage`) → all PASS.

**Smoke wall-clock, reported not absorbed:** one of this slice's three readings
(62.9 s) is past the declared 60 s and two are under it. That matches what the
tier was already doing — CLAUDE.md records 54.9 / 64.0 / 55.7 s on this box on
2026-08-20 and slice 0 read 72.8 s — so the tier straddled its ceiling before
this slice and still does. One box is one data point, the SECONDS budget was NOT
moved, and OI-52's execution row owns the decision. Recording the spread rather
than the final green reading is the point: a single passing measurement here
would misreport a tier that fails roughly a third of the time.

Deferred open items: none — the module-size threshold question is recorded at
the ratchet entry and resolves in slice 2 by deletion, and the smoke wall clock
is already OI-52's; neither is a new decision owed.

### Adjacent findings accumulating for the program close

_(per-slice sections are inserted ABOVE this section, in land order;
banked findings accumulate below as list items)_

- **The design-record §3 enum inventory was incomplete** (slice 0). It listed
  four definition homes plus the crossing table and the alias shim; it missed
  `traj_status._STAGE_LABELS`, an unpinned byte-identical copy of `STAGE_DESC`.
  The census that produced §3 evidently keyed on the CONSTANT NAMES rather than
  on the values, so a copy under a private name was invisible to it. Slices 2-5
  should assume the same blind spot for the bar axis: grep the VALUES
  (`"DevStg-`), not `BAR_`/`STAGE_`.
- **`kitlib/ladder` joins the pre-existing "connectivity undeclared" class**
  (slice 0): `check_trajectory --strict` WARNs that no `IF-###` row names it —
  the same advisory `kitlib/config`, `kitlib/git` and `kitlib/registry` already
  carry, while `kitlib/station` has IF-093 because WI-483 declared its
  cross-component seam. The ladder's consumer edges (`agent_common`,
  `traj_status`) cross components under its single `CMP-006` tag and are
  policed-but-undeclared. Declaring them is IF-minting, well outside slice 0;
  the natural home is WI-494 (OI-48 (d), the kernel's one owning component),
  which should decide the seam rows for the whole package at once rather than
  per-module.
- **`derive_gate` is now under the module-size threshold** (1424 < 1500) for the
  first time, with the bar axis still inside it. Slice 2 deletes that axis, so
  the module will fall further — worth a deliberate look at whether what remains
  is still one coherent module or wants the `stage`/`bar` split the plan
  implies.

- **The two INSERTED frame rungs are repo-global and currently dominate every
  per-phase reading** (slice 1). `boundary_incomplete`/`arch_incomplete` read
  repo-wide registries and sit BELOW every spine rung, so while the frame is in
  work every phase reports the frame's rung however mature its own requirements
  are. On this repo that means all four phases read `DevStg-Arch` and the
  per-phase breakdown discriminates nothing — all four CMP rows are Drafted, so
  even the SETTLED subset is empty and `arch_incomplete`'s "a partition of
  nothing is incomplete" arm fires. Honest (the boundary happens once, for the
  whole system) but it means **slice 4's phase-drop detector will get no signal
  from the stage axis until the frame settles**, and it should be designed
  knowing that rather than discovering it. Pinned by
  `test_the_FRAME_rungs_are_repo_global_and_cap_every_phase`.
- **`spine_stage` needed a `cited_srs` seam to be callable per phase** (slice 1),
  and the class of defect it prevents is worth remembering for slices 2-4: the
  need-COVERAGE rung is a repo-global question ("does every ratified need have a
  requirement answering it") evaluated against whatever row set the caller
  passes. Run naively over one phase's rows it reads every OTHER phase's needs as
  uncovered and reports `DevStg-Needs` for every phase but the first. Any future
  per-scope re-run of a repo-global predicate has the same shape — check what
  each rung's SCOPE actually is before subsetting its input.
- **`derive_stage` reaches into two of `derive_gate`'s PRIVATE predicates**
  (slice 1): `_caps` and `_maturity`, to decide which off-spine rows a settled
  reading keeps. Deliberate over duplicating the maturity tables — one wrong
  copy of "is this row Drafted" would let the two axes disagree, which is the
  whole failure the shared-seam approach avoids — but it is a private edge, and
  slice 2/3 hollow out that module. When they do, these two want a public home
  (with `is_drafted`, which is already public and does the spine half of the
  same job) rather than being carried across as underscore imports.
- **The fingerprint catches staleness the value comparison cannot** (slice 1).
  Because `fingerprint=` is itself a compared field, an input edit that moves no
  stage value still reds `--check` — correctly, since the recorded fingerprint
  has become a false claim. Worth knowing before slice 2 wires more readers: the
  file goes stale strictly more often than its headline changes, and that is the
  intended direction, not noise to tune out.
