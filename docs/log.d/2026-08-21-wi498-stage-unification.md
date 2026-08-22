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

### Slice 2 — selection at-or-above; the bar axis retires from selection (opus worker) — LANDED

Every check-selection site now keys on the effective stage read through
`derive_stage.read`, and `check.py` no longer reads `docs/gate` at all. The
harness selector was the entire A-class half of the bar-vs-stage census; it is
gone, with the membership rule it served.

**THE FINDING THAT SHAPED EVERY THRESHOLD, and it inverts the census's own
translation table.** The obvious re-key — map each bar tag to the lowest STAGE in
that bar's span (`DevStg-Tests` → `DevStg-Arch`, per `STAGE_BAR`) — is wrong, and
measurably so. The bar was a MIN over every in-scope row, so the `DevStg-Tests`
bar was reached **only by a spine already fully decomposed and TC'd**, which on
the ladder is the `DevStg-Impl` RUNG, three above the span's floor; and
`DevStg-Impl` as a bar was never reached at all under the OI-30 D2 ceiling. So
the behaviour-preserving translation is *"the rung at which that bar was actually
reached"*, not *"the lowest rung the bar's span covers"*. Taking the span floor
would have started running five steps three rungs early — on this repo, two of
them RED (see below). The rule each threshold was then derived under: **the
lowest rung at which the artifact the step grades is required to exist and be
complete** — the rung from which a failure is a defect rather than work in
progress.

| step | old `gates=` set | new threshold | reasoning |
|---|---|---|---|
| `format` | {Impl} | `DevStg-Impl` | grades built code. Unreachable from any derived value before (the ceiling) — **OI-51's exact defect** |
| `lint` | {Impl} | `DevStg-Impl` | as `format` |
| `tests+coverage` | {Impl} | `DevStg-Impl` | as `format` |
| `registry-integrity` | **{Reqs} only** | `DevStg-Needs` | a `{Reqs}`-only set is not at-or-above expressible. A structurally broken registry is unreadable at *every* rung. **THE ONE BEHAVIOURAL DELTA** — it now also runs at the top, duplicating `traceability --strict`'s integrity subset; accepted, one cheap read-only pass |
| `derived-gate` | all three | `DevStg-Needs` | freshness of a file still written (dual state, below) |
| `derived-stage` | all three | `DevStg-Needs` | the go-forward guard (slice 1) |
| `traceability` | {Tests,Impl} | `DevStg-Impl` | **not a choice.** Its two orphan rules — "SR has no LLR", "SR has no test" — are literally the predicates holding a repo at the LLReqs and Tests rungs (`spine_stage`), so it cannot be green below Impl by construction. Behaviour preserved exactly |
| `vocabulary` | all three | `DevStg-Needs` | unchanged |
| `need-form` | all three | `DevStg-Needs` | unchanged |
| `privacy` | all three | `DevStg-Needs` | unchanged |
| `doc-navigability` | all three | `DevStg-Needs` | unchanged |
| `perf-budgets` | {Impl} | `DevStg-Impl` | grades measured metrics of a built product |
| `design-flows` | {Tests,Impl} | `DevStg-Tests` | **WIDENED one rung.** Its comment has always read "required from DevStg-Tests on"; the bar's min-fold made it arrive a rung later. The flows answer to a SETTLED decomposition, which is what leaving the LLReqs rung means — the rung the author named is the honest one |
| `trajectory` | {Tests,Impl} | `DevStg-Tests` | **WIDENED one rung**, same restoration. Warn-first here; the `--strict` promotion keeps its own higher rung |
| `backlink-coverage` | {Tests,Impl} | `DevStg-Impl` | **DIVERGES from the old placement argument** ("beside the other spine-coherence steps"). What it grades is a literal `Implements:` declaration IN SOURCE; below the rung where source exists the percentage grades a non-existent artifact and the declared minimum is a floor nobody could meet |
| `trajectory-map` | {Impl} | `DevStg-Impl` | the generated-view family: "churns while the plan is still forming", which stops at Impl |
| `status-map` | {Impl} | `DevStg-Impl` | as above |
| `open-items` | {Impl} | `DevStg-Impl` | as above |
| `okf` | {Impl} | `DevStg-Impl` | as above |
| `ratify-fresh` | {Tests,Impl} | `DevStg-Needs` | **WIDENED to always**, the clearest case in the table. It guards a brief a HUMAN attests FROM, and attestation happens at every rung — the old tag put it out of reach for exactly the repos that attest most (an early one, pinned at the floor for its whole requirements phase). Doubly self-arming already, so a repo with no brief still pays nothing |
| `skills-sync` | {Impl} | `DevStg-Impl` | generated-artifact freshness family |
| `skills-index` | all three | `DevStg-Needs` | unchanged |
| `prompt-catalog` | all three | `DevStg-Needs` | unchanged |
| `staged-divergence` | all three | `DevStg-Needs` | unchanged |
| declared `[step:*]` default | {Impl} | `DevStg-Impl` | value unchanged |

**The two SEVERITY promotions were deliberately NOT widened**, and the asymmetry
with the table above is the point. `trace --require-verified/--strict-schema`
and the `--strict` trio (`trajectory`/`vocabulary`/`backlink`) both keyed on bars
that meant "fully decomposed", i.e. the Impl rung, and both stay there. Moving a
promotion to `DevStg-Arch` — which "past its requirements bar" reads like — would
change a severity the owner ruled warn-first-until-mature. That is a policy
change, not a re-key, and it is not this slice's to make. `ALL` stays excluded
from the `--strict` trio for its original reason: the pre-commit floor passes no
stage and must not block a commit on status.md drift.

**The honesty case, reported not absorbed.** Before touching anything I ran the
plan the mechanical (span-floor) translation would have produced — this repo's
effective stage is `DevStg-Arch`, so the `{Tests,Impl}` family would have gone
live. Real output, `check.py --stage-cleared DevStg-Tests --jobs 0`:
`FAIL traceability` (15 orphan SRs — SR-151/152/160/162/163 and ten more) and
`FAIL backlink-coverage` (49.4% against the declared 50% minimum, 85 LLR rows
with no back-link). **Neither red was a reason to pick a different threshold, and
neither is why the thresholds are where they are** — the derivation above is
independent of them and was written from `spine_stage`'s rung predicates. But
both confirm it from the other side: the orphans ARE the rung-4/5 predicates, so
a repo at Arch failing them is a repo being asked to have finished the rung it is
standing on. The two checks stay red as information; nothing was sanctioned.

**What retired, and why it costs nothing.** `product_floor` + `floor_plan` +
`floor_notice` (the WI-473 monotonic floor) and `window_open` + `advisory_plan` +
`run_advisory` + `ADVISORY_EXCLUDE` (the 2026-07-27 advisory tier) are DELETED,
with `GATE_FILE`, the four `# basis:` regexes, `_basis_counts` and `_window_ord`.
Both mechanisms existed for one cause — a derived bar a single drafted row could
collapse — and the effective stage removes that cause by construction, for EVERY
step rather than the product ones the floor covered. The floor's guarantee is now
a property of the input; the advisory tier's warn-only steps now GATE, which is
strictly stronger than what the ruling bought. The owner's 2026-07-27 ruling is
honoured by deletion rather than violated by it: it said a suppressed step must
still be SEEN, and a step that is not suppressed is seen by running. One thing
genuinely goes: the `modified>0` compatibility arm, which read a field this kit
stopped emitting at D-9 step 7 and which only an old-kit gate file carries.

**The flag surface, decided.** `--stage` is canonical. `--gate` stays accepted
**silently and indefinitely** — it is a flag NAME an adopter's hooks and CI pass
literally, the word was never retired where it means a check that can fail, and
the sweep measured that `--gate` is the only spelling anything in this repo
actually passes. `--stage-cleared` is accepted and **WARNS**, one line per run:
unlike `--gate` it makes a CLAIM about the axis (the value is a bar being
cleared) and that claim is the exact trap OI-51 retires — it survived inside the
2026-08-18 rename meant to remove it (census C-1). argparse records only the
dest, so `_warn_retired_flag_spelling` reads argv. **No third alias generation is
owed**, which the census expected: the three bar spellings are all ladder rungs,
so an adopter's value stays legal; what changed is the READING, and a reading
migrates by a RESYNC note, not a translation table.

**The adopter-authored surface.** `[step:*]` `gates = <list of bars>` becomes
`from-stage = <one rung>`. The legacy list is translated with one notice per run
naming the SECTION (the CLI aliases cannot name a file; this can), and the fold
is `_LEGACY_BAR_THRESHOLD` — `Reqs→Needs`, `Tests→Impl`, `Impl→Impl` — for the
same min-fold reason as the built-ins, so an adopter's step keeps its effective
arrival rather than starting three rungs early. Declaring both keys fails loudly.
This repo's own three sections were migrated in the same commit.

**The dual state, and who `docs/gate` is still for.** It is still WRITTEN and
still `derived-gate`-freshness-gated, because two un-cut consumers remain and
both are slice 4's: `check_trajectory.read_derived_phases` (the phase-drop
detector, which reads `per-phase=` and *silently drops* what it cannot parse) and
`intake._gate_moved` → `tier_signal`. The three display readers
(`traj_parse`/`traj_panels`/`traj_status`) also still read it; they are
presentation and belong with slice 5's vocabulary work, and leaving them
FUNCTIONING is what the plan's transitional state asks. So only the
production-dead `STAGE_BAR`/`stage_to_bar` crossing table died in `derive_gate`
this slice — the bar ordinals, `BAR_NAMES`, `BAR_ORDER` and the alias table stay
as long as the file they produce does. Slice 5's migration retires the file and
takes them with it.

**The C-01 acceptance, driven at the SELECTION level on a real bootstrapped
scaffold.** A mature, frame-free scaffold, then one ordinary Drafted requirement
added in the SAME phase (a draft in a new phase is ignored by a different arm of
the fold, so it would prove the easier half):

```
MATURE    Plan at stage DevStg-Release (tier smoke): | derived BAR: DevStg-Tests
   steps: 24 [backlink-coverage, derived-gate, derived-stage, design-flows,
   doc-navigability, format, lint, need-form, okf, open-items, perf-budgets,
   privacy, prompt-catalog, ratify-fresh, registry-integrity, skills-index,
   skills-sync, staged-divergence, status-map, tests+coverage, traceability,
   trajectory, trajectory-map, vocabulary]
+1 DRAFT  Plan at stage DevStg-Release (tier smoke): | derived BAR: DevStg-Reqs
   steps: 24 [... identical ...]

BAR MOVED: DevStg-Tests -> DevStg-Reqs   (the retired axis collapsed)
PLAN IDENTICAL: True
```

The two-sided proof matters: without the bar half this is a fixture where nothing
moved. `tests/test_selection_at_or_above.py` (15 tests) drives the same scenario
plus the reachability of the three product steps, the threshold-vs-membership
delta, the `from-stage`/`gates` contract, the flag surface, and a reader-seam
case proving the plan follows an edited tree while the file stays byte-identical.
It SUCCEEDS `test_product_floor.py`, discharging that file's own written
obligation ("this test exists so nobody reads the floor as having fixed it"; both
it and `test_advisory_during_window.py` retired with their mechanisms).

**A FINDING THE ACCEPTANCE TEST FORCED OUT, and it limits the fix's reach.** A
fully decomposed scaffold does NOT reach `DevStg-Release` — it reads
`DevStg-Boundary`, floored to `DevStg-Reqs`. `boundary_incomplete` (rung 1)
applies whenever `external.toml` EXISTS, and a scaffold ships one carrying no
ratified crossing, which is honestly "the frame is in work". So slice 1's banked
finding about the frame rungs dominating is sharper than recorded: **on a fresh
scaffold the product steps OI-51 exists to reach stay unreachable until the
adopter settles or removes their boundary registry.** The fixtures declare no
frame (a legal adopter shape, and the one the census drove its own demonstration
over) and say why in `_mature_frame_free`.

**Scaffold-verified, per the standing lesson.** A real `bootstrap.py --dest` run:
`docs/stage` and `docs/gate` both arrive; `check.py --list` reads
`Plan at stage DevStg-Reqs` (the placeholder makes the reader DERIVE, and an
empty spine floors); the plan is 11 steps and `check.py --tier smoke --lenient`
is **RESULT: PASS** — `ci/check.yml`'s fresh-scaffold promise holds.

Ratchets re-stamped deliberately: `check.py` **2337 → 2164** (the deletion, with
the five additions named on the entry so the net is not read as pure
subtraction); `check.py:main` complexity **16 → 15**; smoke membership
**1343 → 1331** (re-stamped DOWN rather than left as slack — a ceiling would have
absorbed the shrink silently); `derive_gate.py`'s module-size entry **deleted**
(1467, back under threshold) with a tombstone recording that the drop is smaller
than slice 1's note predicted, and why.

Adopter-facing: a RESYNC_PACK §3 entry that LEADS with what starts running,
`stack.ini.template`'s `from-stage` contract, `ADOPTING.md`'s `[step:*]` line,
`README.md`'s harness row, PROCESS.md's tense note + harness line, and
PROCESS_OPTIONS.md's advisory/floor paragraphs replaced by the at-or-above rule.
`ci/check.yml`, `integrate._run_bar` and the five launcher/setup scripts pass
`--stage`. The WI `bar:` frontmatter key is deliberately NOT renamed: its three
values are ladder rungs whose selection is identical under the new thresholds, so
the rename is vocabulary and belongs to slice 5.

Byte deltas: `PROCESS.md` 84,383 → 84,524 (**+141**, flagged, watched);
`PROCESS_OPTIONS.md` 177,258 → 176,428 (**−830**); `byte-budget-guard/SKILL.md`
4,974 → 4,834 (cap 5,000). No capped file grew.

Gates, real output on this box:

- `python -m pytest -q -n auto -m smoke` → **1318 passed, 5 skipped in 80.62 s**
  on the final tree; two readings across the slice: **68.6 / 80.6 s**.
- `python project-trajectory/scripts/check_docs.py --root . --stale` → **OK —
  978 doc(s), 1350 intra-repo link(s), 0 broken (1 orphan warning)**.
- `python project-trajectory/scripts/check_trajectory.py --root . --strict` →
  **clean (495 work item(s), 461 done (93%), 21 cancelled, graph acyclic)**.
- `python project-trajectory/scripts/trace.py --root . --strict-integrity` →
  **SN=27 SR=73 LLR=168 TC=164 orphans=15 integrity=0 components=4
  component-findings=0 interfaces=130 interface-findings=0**.
- `python project-trajectory/scripts/check_vocab.py --root . --strict` →
  **clean (459 live authored file(s); no retired gate tags)**.
- `python project-trajectory/scripts/check.py --jobs 0` (this repo's own plan, at
  the new keying) → **RESULT: PASS**, 11 steps — the 10 that ran before plus
  `ratify-fresh`, which the re-derivation widened and which passes.
- `python -m pytest -q -n auto` (full, unfiltered, on the landed tree) →
  **2786 passed, 14 skipped in 658.42 s**. The count fell from slice 1's 2798
  because two test modules retired with the mechanisms they pinned
  (`test_product_floor`, `test_advisory_during_window`) and
  `test_selection_at_or_above` succeeded them with 15.

**Smoke wall-clock, reported not absorbed:** 80.6 s against the declared 60 s, on
a tier that read 51.3 / 62.9 / 55.0 s at slice 1 and 72.8 s at slice 0. One box
is one data point; the SECONDS budget was NOT moved and remains OI-52's.

Deferred open items: none — the two red checks above are information about this
repo's spine, not a decision owed; the WI-473 disposition is a program
bookkeeping act recorded in the findings below; and the smoke wall clock is
already OI-52's.

### Slice 3 — Founded reaches Impl; Release is evidence-gated; the phase rule arms (opus worker) — LANDED

The vacant rung is occupied and the top of the ladder is honestly empty.
`spine_stage`'s Impl/Release cell discriminator is DELETED — not re-polarized —
so a spine decomposed and TC'd through the test tier reads **`DevStg-Impl`**, and
**`DevStg-Release` is returned by nothing**.

**The discriminator's new shape, and why the arm collapsed rather than flipping.**
The two lines were `if not all(is_approved(r) or is_founded(r) for r in srs):
return STAGE_IMPL` / `return STAGE_RELEASE`. Under the owner's semantics BOTH
arms land on Impl, so the test had nothing left to decide and went with it. The
fall-through now ends `return STAGE_IMPL`. This is a **polarity inversion**, not
a tightening: rung 6 used to mean "the spine is NOT yet blessed" and now means
"the spine IS blessed and the code is being made to pass" — the reading the rung
was inserted for. One consequence worth stating because it looks like a
regression and is not: an unmigrated out-of-vocabulary `Modified` cell still
reads Impl, but now by falling through with everything else rather than by being
the ONE value that could reach a rung no legal spine could occupy.

**Slice 1's claim VERIFIED, not assumed.** `derive_stage` calls
`derive_gate.spine_stage` at exactly two sites (`:153` global, `:161` per-phase),
so editing the one fall-through moved both files with no second edit. Driven:
this repo's `docs/stage` and `docs/gate` were both still `--check`-fresh
afterwards, because neither derived VALUE moved here (see below).

**`DevStg-Release` is unreachable, and that is the deliverable.** Leaving Impl
means "all the declared test cases PASS", and the kit has no machine reading of
that — the evidence carrier is its own future row. Rather than approximate it,
the rung has no producer. Pinned twice, deliberately: exhaustively over the
closed Status enum plus a retired value across all three tiers and both
LLR-exemption shapes (2x4³ = 128 spines, none reaches Release), and
STRUCTURALLY, by asserting `spine_stage`'s source contains no
`return STAGE_RELEASE` — because enumeration cannot catch a return behind a
condition no fixture happens to build. Deleting that second test is how the
harness driver lands: an act, not a drift.

**The OI-30 D2 ceiling: the mapping old → new, recorded at the mechanism.**

| | old | new |
|---|---|---|
| the RULE — "a Status cell may never claim the evidence passed" | D2's ceiling comment | UNCHANGED, restated on the axis of record: `spine_stage`'s docstring |
| the STAGE half — the Impl→Release cell test | `spine_stage:935-937` | **DELETED**, and the guard is *stronger*: a ceiling flag says "we could compute this but decline to"; no-producer says "nothing here can compute it", which is true |
| the BAR half — `_RELEASE_CEILING` / `_CEILING_NOTE` / `bar_label` | live | **KEPT VERBATIM.** `docs/gate` is still written for slice 4's two committed-history detectors, so the bar is still read; lifting its ceiling would raise a live value on the strength of cells, which is exactly D2's hazard. Retires WITH the file, slice 5 |
| the EXIT condition — "delete when the harness driver lands" | live | UNCHANGED and **NOT claimed**. Making the rung honestly unreachable is not the same act as making it computable |

**The phase rule — surface, tier, and a measurement that reshaped it.**
`derive_stage.phase_rule_findings` + `--phase-rule` / `--strict`. Surface chosen
against the brief's two candidates: `trace.py` and `check_trajectory.py` both
deliberately avoid importing the derivation (trace keeps F5 duplicates of the row
predicates precisely so it need not), and the rule needs a real before/after
effective stage. `derive_stage` already owns the derivation and every input, so
it hosts the rule and reads the before-state from git. **Tier: WARN-FIRST**,
exit 0, `--strict` promotes to exit 1; it is deliberately NOT wired into
`check.py` and cannot block a commit. OI-51 ruled the rule EXISTS, not that it
hard-fails on day one, and a rule whose fire has never been observed on real
authoring should not gate. The arming path is one call-site edit — the predicate
and its vocabulary do not change (the `trace.schema_advisories` warn-first twin
idiom).

**THE MEASUREMENT THAT CHANGED THE RULE'S TRIGGER SET, driven before the rule was
written.** Plan §4 says "a newly drafted/redrafted row would DECREASE the
effective stage". Driven on a frame-free synthetic spine:

```
BASELINE (2 SR settled, phase 1)                      -> DevStg-Impl    (baseline)
+ NEW DRAFTED SR in the CURRENT phase (1)             -> DevStg-Impl    SAME
+ NEW DRAFTED SR in a NEW phase (2)                   -> DevStg-Impl    SAME
+ NEW *RATIFIED* SR in the CURRENT phase, no children -> DevStg-LLReqs  DECREASE -2
+ NEW *RATIFIED* SR in a NEW phase (2), no children   -> DevStg-LLReqs  DECREASE -2
REDRAFT an existing LLR (phase 1)                     -> DevStg-LLReqs  DECREASE -2
REDRAFT an existing TC (phase 1)                      -> DevStg-Tests   DECREASE -1
REDRAFT an existing SR (phase 1)                      -> DevStg-Impl    SAME
```

**A newly DRAFTED row cannot decrease the effective stage at all** — slice 1
excludes drafts from the settled fold, so the plan's literal trigger is inert BY
CONSTRUCTION, in both the standing-phase and new-phase directions. Keying on the
literal words would have shipped a rule with no reachable trigger. The rule keys
on "added, or `Status` moved", which CONTAINS the plan's set and catches the two
shapes that actually decrease the reading. This is not a defect in either slice —
it is slice 1's C-01 fix working — and it is pinned by its own test so nobody
"restores" the literal wording later.

**The rule as landed:** when the effective stage decreases, every row the edit
added or re-statused must carry a `Phase` tag that is NOT the phase the settled
work was standing in (`max` over non-Drafted rows on the before side — the same
value `phase=` records, so the rule and the field cannot mean different things).
A new higher phase and an already-open lower phase both satisfy it. Phase stays a
pure function of the registries: no stored counter, plan §4 alternative (ii)
declined.

**A DESIGN CORRECTION THE EXEMPTION FORCED.** The before-state first held the
FRAME (SN/BIF/CMP) at the live tree, to isolate the spine edit. That is wrong,
and the ruled exemption is what proves it: `DevStg-LLReqs → DevStg-Arch` is
derived from the COMPONENT registry, so a frame pinned live makes the owner's one
permitted decrease **unreachable** — the rule could not see the transition it is
required to forgive. The before-state now materializes every declared input at
`HEAD` into a temp tree and runs `load_spine` over it, which also buys carrier
resolution, the `-000` filter, and the `have_bifs`/`have_cmps` applies-when
(where absent and empty mean opposite things) for free instead of by
re-implementation.

**The four directions, driven** (`tests/test_phase_rule.py`, 11 tests, real git
repos): a stage-lowering edit in the standing phase FIRES; the byte-identical
edit with one `Phase` cell changed PASSES; an already-open LOWER phase also
passes; the `LLReqs → Arch` decrease passes with no phase tag; and a decrease
that merely ENDS at Arch (Impl → Arch, three rungs) still FIRES — the exemption is
a PAIR, not a predicate over the Arch rung, per the owner's refusal of a wider
Arch-tier exemption. Plus the redrafted-child shape, the no-git degrade, and the
WARN/`--strict` contract.

**THIS REPO'S OWN STATE, MEASURED — no allowlist needed, and the brief asked
either way.** Over the last **80 commits**, the effective stage DECREASED **zero
times**; it moved once, upward (`2d51f140`, `DevStg-Reqs → DevStg-Arch`), and only
two distinct values occur across that whole range. So the rule fires on nothing
retroactively and no seeded allowlist (the OI-43/WI-488 precedent) was created.
Two independent reasons, both already banked by earlier slices: the 15 Drafted
rows are all `phase = 5` AND cannot lower the reading anyway, and the two
repo-global frame rungs pin every phase at `DevStg-Arch` while the partition is
in work. `derive_stage --phase-rule` on this tree: **clean**.

**The pins that inverted: NINE, not the five the deep-check counted — and the
undercount has the same shape slice 0 found.** The deep-check's census
("The test pins that would move") named five, all in
`tests/test_ratification_level.py`. Nine reddened there, and four more in
`tests/test_selection_at_or_above.py` that postdate the deep-check. The four
extra in the first file are the FRAME-RUNG tests, which use the settled value
only as a baseline ("nothing here holds the rung open") — they are not claims
about the top of the ladder at all, but spelling `dg.STAGE_RELEASE` at each made
them look like ones. Fixed at the root: a module-level **`SETTLED = dg.STAGE_IMPL`**
now names what those tests mean, so the next re-discrimination moves one line.
The census keyed on tests ABOUT the rung and missed the ones that merely USED it —
the same blind spot as slice 0's enum inventory keying on CONSTANT NAMES.

Flipped deliberately, each citing the ruling:

1. `test_a_settled_spine_is_the_TOP_RUNG` → `..._is_the_IMPL_rung_and_the_top_rung_is_NOT_DERIVED`. The ladder still ENDS at Release and the second assertion still says so — the rung was made evidence-gated, not deleted.
2. `test_the_MODIFIED_rung_RETIRED_and_took_no_successor` — the `Founded` arm. Same value, different reason, and the comment says which.
3. `test_an_LLR_EXEMPT_requirement_needs_no_LLR`.
4. **`test_an_unverified_SR_over_AUTHORED_tests_is_the_IMPL_rung`** — the pin the deep-check called "designed to fail on this change". Its own docstring ended: *"pin the CURRENT truth, INCLUDING THE UNREACHABILITY, so that landing the harness driver reddens this test rather than sliding past it."* It reddened. Rewritten to record that **the vacancy moved UP rather than disappearing**: Release is now the rung nothing derives, which is the correct thing for the TOP of a ladder to say, instead of a hole in the middle.
5-8. the four frame-rung tests, via `SETTLED`.
9-12. `test_selection_at_or_above.py` ×4, including the reachability test whose text also predicted this slice by name.

**DIAL_HOLDS: verified unchanged, re-driven AFTER the change** (the brief's
check, not the deep-check's claim carried forward). `human_holds` separates
`DevStg-Impl(6)` from `DevStg-Release(7)` at **NONE** of the five dial levels —
both fall into the `4: None` holds-everything short-circuit — and
`APPROVAL_RUNGS` governs **no** registry at ord 6 or 7. So the re-discrimination
is behaviourally INERT for all 27 stage-keyed ratification sites, exactly as
predicted, and `DIAL_HOLDS` needed no edit.

**Scaffold-verified, per the standing lesson, and this is where OI-51's defect
visibly closes.** A real `bootstrap.py --dest` run: `derive_stage.py` arrives; a
fresh scaffold writes `stage = DevStg-Reqs` (sane, floored); `--phase-rule`
degrades cleanly with no git. Then an all-Founded frame-free fixture written into
that scaffold:

```
derive_stage: wrote docs/stage -> DevStg-Impl.
stage = DevStg-Impl / settled-stage = DevStg-Impl / live-stage = DevStg-Impl

Plan at stage DevStg-Impl (tier smoke):
  - format           [product] [>=DevStg-Impl]  ...ruff format --check src tests
  - lint             [product] [>=DevStg-Impl]  ...ruff check src tests
  - tests+coverage   [product] [>=DevStg-Impl]  ...pytest -q -m smoke
```

The three product steps OI-51 exists to reach now SELECT from a derived value on
a real adopter shape. The frame had to be removed first — slice 2's banked
finding holds unchanged: a scaffold's blank `external.toml` still pins it at
`DevStg-Boundary`, so an adopter reaches this only once their boundary registry
settles or is declared absent.

**Ratchets re-stamped deliberately.** `derive_gate.py` **RE-ENTERS** the
module-size baseline at **1523** (+56 from 1467) — and the entry is honest about
what grew: **comment mass on a slice that deleted executable lines.** The three
records added are the D2 rule on the axis of record, the old→new ceiling mapping
where the surviving mechanism is, and the polarity-inversion note (without which
a reader misreads the new arm as a tightening). **Not trimmed to fit:** the +56
was measured after the fact, and cutting prose to clear a threshold is the
ratchet inverted — slice 1's own near-miss note. This is the **third
enter/delete cycle in three slices** (1503 in, deleted at 1467, back at 1523),
which says the threshold sits exactly where this module oscillates while it holds
two axes; the resolution remains slice 5's DELETION, not a bump.
`tests/test_phase_rule.py` filed into `conftest.SLOW_MODULES` beside
`test_derive_stage` — every test in it commits a real git repo, so it is that
class, not a borderline call. Smoke membership moved 1318 → 1320 (the two new
in-process pins) and needed no re-stamp.

Adopter-facing: a RESYNC_PACK §3 entry that LEADS with the value change — an
adopter's derived stage can move at re-sync with no edit to their registries —
states both new rung readings plainly, and records the phase rule as warn-first
and unwired, so **no action is required at re-sync**.

Gates, real output on this box:

- `python -m pytest -q -n auto -m smoke` → **1320 passed, 5 skipped in 67.76 s**.
- `python project-trajectory/scripts/check_docs.py --root . --stale` → **OK —
  978 doc(s), 1350 intra-repo link(s), 0 broken (1 orphan warning)**.
- `python project-trajectory/scripts/check_trajectory.py --root . --strict` →
  **clean (495 work item(s), 461 done (93%), 21 cancelled, graph acyclic)**.
- `python project-trajectory/scripts/trace.py --root . --strict-integrity` →
  **SN=27 SR=73 LLR=168 TC=164 orphans=15 integrity=0 components=4
  component-findings=0 interfaces=130 interface-findings=0**.
- `python project-trajectory/scripts/check_vocab.py --root . --strict` →
  **clean (460 live authored file(s); no retired gate tags)**.
- `python project-trajectory/scripts/check.py --jobs 0` → **RESULT: PASS**.
- `derive_stage.py --check` → **up to date (DevStg-Arch)**; `derive_gate.py
  --check` → **up to date (DevStg-Reqs)**. Neither derived value moved on THIS
  repo, because the frame rungs sit below every spine rung here — the change is
  visible on a settled spine, which is what the scaffold run above demonstrates.
- `python -m pytest -q -n auto` (full, unfiltered) → **2799 passed, 14 skipped in
  610.33 s**. Up 13 from slice 2's 2786: the 11 new `test_phase_rule` tests plus
  the two new in-process pins on the Release rung's unreachability.

**Smoke wall-clock, reported not absorbed:** 67.8 s against the declared 60 s. The
tier read 51.3 / 62.9 / 55.0 s at slice 1, 68.6 / 80.6 s at slice 2 and 72.8 s at
slice 0, and CLAUDE.md records 54.9 / 64.0 / 55.7 s on this box on 2026-08-20. One
box is one data point; the SECONDS budget was NOT moved and remains OI-52's.

No spine mint was owed and none was made: `check_trajectory --strict` is clean,
because this slice adds behaviour to modules the spine already owns (LLR-186
carries `derive_stage.py`) rather than a new module. No Approved row amended.

Deferred open items: none — the module-size oscillation is recorded at the
ratchet entry and resolves in slice 5 by deletion; the evidence carrier is
already the ruled plan's own separately-sequenced row, not a new decision; and
the smoke wall clock is already OI-52's.

### Slice 4 — the detectors move to stage history; the tier signal lives again (opus worker) — LANDED

Both event detectors now read the stage axis, and `docs/gate`'s remaining readers
are exactly four, all slice 5's. **WI-497 folded and closed** — its spec is in
`docs/work/complete/` with the Deliverable filled and its SpecRef cleared (R-F).

**THE ANCHOR TRANSLATION IS THE SLICE'S REAL DECISION, and the spelling is a
trap in both rows.** A phase anchor is a WI TITLE (`[v2]-[g1]`, `[v2]-[reqs]`) —
committed history — so the retired spellings are TRANSLATED on read, never
re-recorded, exactly as the `g1`/`g2` changeover already did one generation ago.
What they translate TO was the question, and the deep-check's warning ("three
spellings are shared between the axes, so a mechanical remap is unsafe") is
concrete here:

| anchor token | what closing it means | recorded reach | the spelling |
|---|---|---|---|
| `reqs` / `g1` | the phase's SRs are authored AND ratified, clearing `spine_stage`'s `any(is_drafted(sr))` test | **`DevStg-LLReqs`** | `DevStg-Reqs` — the rung it has just LEFT, two below |
| `tests` / `g2` | LLRs and TCs authored and non-Drafted, clearing the LLReqs and Tests predicates both | **`DevStg-Impl`** | `DevStg-Tests`, one below |

An anchor records **the rung the phase stands at once it closes** — slice 2's
inversion finding applied on this axis. Taking the spelling would have recorded a
reach below the phase's real standing, i.e. made the detector UNDER-report, which
is the failure direction that loses the event it exists for. Going forward the
canonical spelling IS the rung: `[<phase>]-[DevStg-LLReqs]`, `[<phase>]-[DevStg-Impl]`,
or any other rung — one vocabulary, and a title that says which rung it means.
The predecessor-shape rule generalized with it, from "a `tests` anchor lists its
`reqs` anchor" (expressible only with two fixed levels) to "each anchor lists the
next-LOWER anchor of its own phase".

**THE DETECTOR READS THE *LIVE* PER-PHASE FIELD; SELECTION STAYS ON THE SETTLED
ONE — and that split is what discharges slice 3's banked tension rather than
trading it away.** The event is "new or reopened content entered a phase whose
anchor is closed", and a Drafted or re-Drafted row IS that event. `per-phase`
excludes drafts by construction (slice 1's C-01 fix, which exists so one draft
cannot collapse selection), so keying detection there would make the detector
blind to precisely its own subject. `per-phase-live` is where the drafts are.
Driven from both sides: the same fixture fires on the live field and is silent on
the settled one.

That answers the slice-3 finding directly. `arch_incomplete`'s "self-reporting
recursion" — minting a Drafted component for a newly identified sub-component
drops the reported stage with nobody deciding to — became false of the EFFECTIVE
stage at slice 1 and stays false, correctly. It is true of the LIVE reading, and
the live reading is what the detector consumes. Driven on a real scaffold: adding
one `Drafted` CMP row leaves `per-phase` byte-identical and moves `per-phase-live`
to `DevStg-Arch`. **The signal survives where events are detected; only the
headline stopped moving.** No design had to give.

**THE ABSTENTION, which is the one part that is not a re-key, and it is why the
detector is quieter on this repo than the bar axis was.** Three of the eight
rungs are decided by REPO-WIDE registries even when `spine_stage` is called with
one phase's rows — `DevStg-Needs` (the need registry, and through `cited_srs` the
whole settled SR set), `DevStg-Boundary` (external), `DevStg-Arch` (components);
the frame arguments are passed whole to every per-phase call. When a phase reads
one of those, EVERY phase reads it at once and none is reporting anything about
its own content. Concluding "new or reopened content entered phase 4" from that
value is arithmetically true and causally invented. So `kitlib.stage.REPO_GLOBAL_RUNGS`
is declared beside the per-phase sentinel it is a sibling of, and the detector
abstains there — **and says so**, once, naming the rung and the phases. The
schedule map's standing criticism of this detector (reader H) was that it "silently
drops what it cannot parse", going vacuous where a reader assumes clean; an
abstention that announces itself is the correction to that, not a second defect.

**THE HONEST COST, stated because it is a live warn changing shape on this repo.**
Before this slice `check_trajectory --strict` printed:

```
WARN - phase '4' dropped to DevStg-Reqs but its closed [4]-[tests] anchor
       recorded level DevStg-Tests
```

After it, that warn is gone and the stand-down warn is in its place: phases 3 and
4 both read `DevStg-Arch` (all four CMP rows are Drafted), a repo-global rung. The
underlying fact — a drafted row sits in phase 4 — has not been fixed and is not
being hidden; the stage axis simply cannot attribute it to phase 4 while the frame
dominates, and slice 1 banked exactly this warning ("slice 4's phase-drop detector
will get no signal from the stage axis until the frame settles"). The choice was
between abstaining loudly and fabricating an attribution, and the second is not
available. It resumes on this repo when the partition settles; it works today on
any repo whose frame is settled or absent, which the scaffold run below shows.

**The tier signal, fixed on the NEW carrier and PROVEN able to fire.**
`intake._gate_moved` → **`_stage_moved`**: a two-point delta of `docs/stage`'s
`stage` FIELD across the two git trees, through `kitlib.stage.parse`. Not "the
first non-comment line" as WI-497's spec proposed — `docs/stage` is key=value
precisely so a reader addresses a field by name, which is the stronger fix and is
the deviation from that spec's literal wording. `tier_signal`'s keyword became
`stage_moved` so the signal and its input name one axis. Unreadable on either side
now answers False, which the retired docstring CLAIMED and the code did not do (a
None against a value compared unequal and reported a move); that matters at exactly
one commit per adopting repo — the kit upgrade that first writes `docs/stage`.

**The proof the fix alone does not give.** A function dead since the derived-gate
migration needs more than a unit test of its input: it needs the ROW. So
`intake._amendment_drafts` is driven over a real two-commit repo whose merged delta
both amends a ratified spine cell and moves the recorded stage — the minted row
reads `buildtier = "strong"` — against the byte-identical counterfactual with the
stage held still, which reads `medium`. One row touched in both, so `rows_touched > 3`
cannot be what carried it. Re-driven inside a real bootstrapped scaffold as well:
`_stage_moved: True`, `tier_signal: strong`.

**WI-497's sibling sweep, mechanized.** Two `splitlines()[0]` sites remain in the
kit (`integrate.py`, `trunk_step.py`) and NEITHER is in the defect class — both
read the first line of git command output, where line 0 is the value by the
command's own contract. The sweep is now an AST read
(`test_no_kit_script_takes_splitlines_0_of_a_GENERATED_file`) naming those two, so
a third site must be judged rather than inherited. It reads the AST rather than
grepping because the clearest way to record a retired defect is to NAME it, and a
grep-shaped pin reds on the comment explaining why the code is gone.

**The dead `read_declared` claim, corrected at the smallest honest scope.** The
schedule map's reader E is documented in two homes as "still the reader for
`docs/gate`" and is called on that file by NOTHING. The function itself is very
much alive — it is the reader for the legacy half of the SN-028 dual-read window —
so the honest change is to the CLAIM, not the code: no deprecation, no removal, and
a note recording why the claim could never have been true (`docs/gate` is a
deliberate NON-row in `PROCESS_KEYS` twenty lines below), so the next census does
not re-add it.

**THE CUT-OVER ACCOUNTING, and it corrects slice 2's own enumeration.** Slice 2
recorded `docs/gate`'s survivors as two event detectors plus three display readers.
Both detectors are now cut over — and the remaining set is **four**, not three:

| reader | class | whose |
|---|---|---|
| `traj_parse._gate_value` | display | slice 5 |
| `traj_panels` | display | slice 5 |
| `traj_status._gate_facts` | display | slice 5 |
| **`agent_common.spine_stage_of`** | **RATIFICATION AUTHORITY** — regex-scrapes `stage=` off the `# basis:` line and feeds `human_holds` | slice 5 |

The fourth was in the schedule map (reader F, "the sharpest" windowed reader) and
out of slice 2's list. It is not display, and it is why the `derived-gate`
freshness step stays wired until the file retires: three of the four draw pages,
one decides who may ratify. `derive_gate` still writes the file and the bar
ordinals stay with it. Recorded at `check.py`'s own note and in the lane spec.

**Scaffold-verified, per the standing lesson**, and this is where the design is
visible rather than argued. A real `bootstrap.py --dest` run, two settled phases,
one legacy `[1]-[g2]` anchor and one canonical `[2]-[DevStg-Impl]` anchor:

```
A. two settled phases                stage = DevStg-Impl
   per-phase-live = 1=DevStg-Impl;2=DevStg-Impl        -> no warn

B. phase 2's TC goes back to Drafted  stage = DevStg-Tests
   per-phase-live = 1=DevStg-Impl;2=DevStg-Tests
   WARN - phase '2' dropped to DevStg-Tests but its closed [2]-[DevStg-Impl]
          anchor recorded reach DevStg-Impl - new or reopened content entered

C. one Drafted component              stage = DevStg-Arch
   per-phase-live = 1=DevStg-Arch;2=DevStg-Arch
   WARN - phase-drop detector stood down for phase(s) 1, 2: each reads
          DevStg-Arch, a repo-global rung ...
```

Both anchor spellings resolve, the drop fires on the reopen, and the abstention
takes over the moment the frame goes into work. A fresh scaffold is silent
(`check_trajectory` vacuously clean, exit 0).

**Tests: 29 new, split by the DECLARED cost criterion rather than by subject.**
`tests/test_stage_event_detectors.py` (11, in-process, in the commit bar) carries
the decisions: the translation table and both traps, the live-vs-settled split
driven from both sides, the abstention matrix over all eight rungs, the three
hook-safe degradations, and three cut-over pins (the sweep, the corrected
`read_declared` claim, and no `docs/gate` PATH literal left in either re-keyed
module — read off the AST, excluding docstrings, so prose explaining the history
does not red them). `tests/test_stage_event_detectors_driven.py` (7) is filed into
`conftest.SLOW_MODULES`: every test either takes the `scaffold` fixture or commits
a real git repo. That split cost the slice its own headline pin — the end-to-end
`strong`-arm fire needs two committed trees and so runs at close and in CI, not per
commit — which is the direction that shows the tiering is by criterion and not by
convenience. `tests/test_trajectory_arch.py`'s five existing phase tests were
re-keyed in place (+2 new: a canonical-spelling parse, and a `DevStg-*` token
naming no rung, which must be refused loudly now the regex's token set is open).

**A FIXTURE-ORDER FRAGILITY FOUND WHILE EXECUTING, and fixed in the three modules
this slice touched.** `kitlib` is a package under `scripts/`, which nothing puts on
`sys.path` until the first `load_script` call — so a module-level `from kitlib
import ...` in a test file resolves only when some earlier-collected module happens
to have called it first. It held by accident until an xdist worker collected
`test_trajectory_arch` first and the module errored at import. The three modules
here now insert the path explicitly; the same latent pattern in
`test_kitlib_stage`, `test_derive_stage` and `test_phase_rule` is banked below
rather than swept, since touching them is outside this slice.

**Ratchets re-stamped deliberately, four of them, each with its reason on the
entry.** `check_trajectory.py` **4398 → 4496**: the block measures 217 lines of
which 64 are comment or blank, and the bump is mostly those — the translation
table's derivation, the live-vs-settled reasoning, and the abstention. Not
decomposable as a unit (it is one detector sharing one anchor vocabulary), but the
module has now grown at five of the last six stamps and the entry says so rather
than implying otherwise. `intake.py` **1901 → 1940**: the executable half is
roughly a wash; the bump records a defect that was silent for a whole vocabulary
generation, because a dead mechanism that leaves no note behind is how it gets
rebuilt. `agent_common.py` **2412 → 2418** and `check.py` **2164 → 2171**: both
COMMENT ONLY, zero executable change. Smoke membership **1331 → 1344** for the
eleven in-process tests, headroom stated as a count (+8) exactly as the last
fourteen stamps did. **The 60 s SECONDS budget was NOT moved** — see below.

Adopter-facing: a RESYNC_PACK §3 entry that LEADS with the fact that a mechanism
which has been silently dead in an adopter's repo starts firing, and is explicit
that no NEW adjudication rows appear — some existing ones are simply graded at the
tier they always warranted. It also states the anchor translation with both traps,
the new canonical spelling, and the abstention's user-visible shape (one stand-down
warn instead of a false drop warn per phase).

No spine mint was owed and none was made: `check_trajectory --strict` is clean —
this slice adds behaviour to modules the spine already owns and one new TEST module
pair, which is the `test_phase_rule` precedent. No Approved row amended.

Gates, real output on this box:

- `python -m pytest -q -n auto -m smoke` → **1331 passed, 5 skipped**; two readings on the
  final tree, **146.3 / 73.3 s** (the first taken immediately after a full
  `check.py --jobs 0` run on the same box, which is why the SPREAD is reported
  rather than the better number)
- `python -m pytest -q -n auto` (full, unfiltered) → **2817 passed, 14 skipped in 642.87 s**.
  Up 18 from slice 3's 2799: the 18 new tests across the two new modules, against
  the two retired `test_trajectory_arch` phase tests replaced by four
- `python project-trajectory/scripts/check_docs.py --root . --stale` → **OK —
  978 doc(s), 1350 intra-repo link(s), 0 broken (1 orphan warning)**.
- `python project-trajectory/scripts/check_trajectory.py --root . --strict` →
  **clean (495 work item(s), 462 done (93%), 21 cancelled, graph acyclic)** — the
  done count moved 461 → 462 with WI-497's close.
- `python project-trajectory/scripts/trace.py --root . --strict-integrity` →
  **SN=27 SR=73 LLR=168 TC=164 orphans=15 integrity=0 components=4
  component-findings=0 interfaces=130 interface-findings=0**.
- `python project-trajectory/scripts/check_vocab.py --root . --strict` →
  **clean (461 live authored file(s); no retired gate tags)**.
- `python project-trajectory/scripts/check.py --jobs 0` → **RESULT: PASS**
- `derive_stage.py --check` / `derive_gate.py --check` → **up to date (DevStg-Arch)** / **up to date
  (DevStg-Reqs)**. Neither derived value moved: this slice edits no registry row

**Smoke wall-clock, reported not absorbed:** 73.3 s on an idle box (and 146.3 s on a loaded one) against the declared 60 s.
The tier read 51.3 / 62.9 / 55.0 s at slice 1, 68.6 / 80.6 s at slice 2, 72.8 s at
slice 0 and 67.8 s at slice 3, and CLAUDE.md records 54.9 / 64.0 / 55.7 s on this
box on 2026-08-20. One box is one data point; the SECONDS budget was NOT moved and
remains OI-52's.

Deferred open items: none — the abstention's practical effect on THIS repo is a
consequence of the frame being in work, not a decision owed; the `check_trajectory`
module-size question is recorded at its ratchet entry; and the smoke wall clock is
already OI-52's.

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
- **WI-473's row is still QUEUED and its mechanism has now been superseded**
  (slice 2). The product-regression floor was BUILT under that id (the
  module-size entry records the +146) but the row never left `docs/work/queued/`,
  so this slice deleted the deliverable of an open work item. The deletion is
  the ruled plan's (§5 item 2 supersedes the floor), not a worker's improvisation
  — but the row now needs a disposition, and `complete` versus `cancelled` is a
  real judgement: it SHIPPED and was then superseded. Not touched here, because
  closing another WI's row is not this slice's to do. Whoever closes it also owns
  `docs/work/queued/WI-473-monotonic-product-floor.md:62`, which cites the now
  deleted `tests/test_product_floor.py` — the one NEW dangling doc-reference this
  slice created (`check_doc_refs --strict` went 93 → 90 dangling overall, so the
  net moved the right way, and that step is red at HEAD too and gated at no rung
  this repo occupies). `docs/requirements/open-items.toml:2043` cites the same
  deleted test inside OI-51's own record; the successor test carries the
  obligation forward in its docstring.
- **A fully decomposed SCAFFOLD cannot reach the rung OI-51's fix needs**
  (slice 2), which sharpens slice 1's frame-rung finding rather than repeating
  it. `boundary_incomplete` applies whenever `external.toml` EXISTS, and
  `bootstrap.py` ships one with no ratified crossing — honestly "the frame is in
  work" — so a scaffold with a perfect SN→SR→LLR→TC chain reads
  `DevStg-Boundary`, floors to `DevStg-Reqs`, and selects none of the
  `DevStg-Impl`-threshold steps. The product checks OI-51 exists to make
  reachable therefore stay unreachable for an adopter until they settle their
  boundary registry or declare no frame. Nothing here is wrong — the rung is
  reporting a real state — but the fix's reach is narrower than "a decomposed
  spine gets its product checks", and slice 3 should decide knowing it.
- **`derive_gate` is again under the module-size threshold (1467), and the drop
  was much smaller than slice 1's entry predicted** (slice 2). That entry said
  "slice 2 removes the bar ordinals, BAR_NAMES, BAR_ORDER and STAGE_BAR — expect
  a large drop"; only the production-dead crossing table could actually go,
  because the module still WRITES `docs/gate` for two live detectors. The bar
  axis cannot leave `derive_gate` until the FILE leaves, which is slice 5. Worth
  carrying: the same expectation will be wrong again if slice 4 is planned as
  "delete the bar" rather than "re-key the detectors first".
- **`ruff check` reports two PRE-EXISTING unused imports** (slice 2), found while
  linting this slice's own edits: `tests/test_agent_loop.py:16` (`inspect`) and
  `tests/test_trace_hats.py:38` (`pytest`). Not touched — unrelated code — and
  recorded because of WHY they survived: `lint` is a `DevStg-Impl`-threshold
  product step, and this repo's effective stage is `DevStg-Arch`, so it does not
  run here. That is the same class of gap OI-51 names, showing up in the kit's
  own tree; it closes for this repo when the spine settles, not by an edit.
- **Rung 3's "self-reporting recursion" DOES NOT SURVIVE INTO THE EFFECTIVE
  STAGE** (slice 3), and this is the sharpest tension the slice found between two
  landed designs. `arch_incomplete`'s docstring calls it "the mechanism the whole
  eight-rung design rests on": minting a `Drafted` CMP row for a newly identified
  sub-component "DROPS the reported stage back to Arch with nobody deciding to,
  which is the honest report". That is true of `spine_stage` over LIVE rows and
  **false of the effective stage** — `derive_stage._settled_off_spine` filters
  Drafted components out of the settled fold exactly as drafts are filtered from
  the spine, so identifying a sub-component now moves nothing. Found by driving
  it: the phase rule's exemption test could not produce a `LLReqs → Arch`
  decrease that way at all, and had to use a settled row recording
  `Standing = "has-gap"` instead. Neither design is wrong on its own — slice 1
  suppressed draft-driven collapse deliberately — but a headline behaviour of
  rung 3 is now reachable only through the standing axis, and `derive_gate`'s
  docstring still promises the draft route. Slice 5's prose sweep owns the
  wording; whether the SIGNAL should be restored (the recursion is a real event
  the ladder was built to report) is a design question for the program close.
- **The deep-check's pin census undercounted for a structural reason worth
  carrying into slices 4-5** (slice 3): it named five inverting pins and nine
  reddened, because it found the tests ABOUT the top rung and missed the four
  that merely USED the settled value as a baseline. Same shape as slice 0's enum
  inventory keying on constant NAMES. The fix generalizes: where a test needs "a
  spine with nothing holding it", give the value a NAME
  (`test_ratification_level.SETTLED`) rather than spelling the rung. Slices 4/5
  should assume any census of "what pins value X" is short by the incidental
  uses, and grep the VALUE across `tests/` before trusting a count.
- **`derive_gate.is_approved` and `is_founded` now have NO CALLER in their own
  module** (slice 3) — the Impl→Release discriminator was the last one. They stay
  because they are a shared VOCABULARY pinned equal to `trace.py`'s copies by
  `test_rule_sync`, not private helpers, and deleting the mirror of a live
  predicate to satisfy a dead-code reading would take the pin with it. But the
  F5 duplication now exists with only one live side, which is a weaker
  arrangement than when it was written. When slice 5 retires the bar axis, these
  two want either a single home or an explicit note that `derive_gate` keeps them
  solely for the pin.
- **The phase rule is warn-first and UNWIRED — it runs only when invoked**
  (slice 3). `derive_stage --phase-rule` is in no `check.py` step and in no hook,
  so nothing runs it automatically, on this repo or an adopter's. That is the
  deliberate arming posture (a rule whose fire has never been observed should not
  gate), but it means the rule accumulates no field evidence on its own. Whoever
  arms it should wire it warn-only into the pre-commit floor FIRST and collect a
  few real firings before promoting to `--strict`; arming straight to hard from
  zero observations would repeat the pattern OI-51 exists to correct.
- **The fingerprint catches staleness the value comparison cannot** (slice 1).
  Because `fingerprint=` is itself a compared field, an input edit that moves no
  stage value still reds `--check` — correctly, since the recorded fingerprint
  has become a false claim. Worth knowing before slice 2 wires more readers: the
  file goes stale strictly more often than its headline changes, and that is the
  intended direction, not noise to tune out.

- **Slice 2's dual-state enumeration UNDERCOUNTED `docs/gate`'s readers, and the
  one it missed is the least display-like of them** (slice 4). It recorded "two
  event detectors plus three display readers"; the real remainder after cutting
  the detectors over is FOUR, because `agent_common.spine_stage_of` scrapes
  `stage=` off the `# basis:` line and feeds `human_holds` — RATIFICATION
  AUTHORITY, not presentation. It was in the schedule map (reader F, called "the
  sharpest" windowed reader) and simply did not make the slice's list. Corrected
  at `check.py`'s note and in the lane spec. **This is the same census blind spot
  slices 0 and 3 each recorded once already** — slice 0's enum inventory keyed on
  constant NAMES and missed a private copy; slice 3's pin census keyed on tests
  ABOUT a rung and missed the ones that merely USED it; this one keyed on the
  reader CLASS the slice was working in. Three for three: slice 5 should build
  its retirement list by grepping the FILENAME across the kit, not by extending
  any of these lists.
- **`derive_gate.basis_line`'s `per-phase=` field now has NO code consumer at
  all** (slice 4). `check_trajectory.read_derived_phases` was the last one. The
  field is still emitted and is still compared by `--check`, so it cannot rot
  silently, but nothing reads it — which means it can be renamed freely and no
  test would teach anyone that. Recorded at
  `test_the_basis_line_still_parses_under_its_SURVIVING_consumer`, which this
  slice re-pointed onto `agent_common.spine_stage_of`/`stage=` (its second
  re-pointing; slice 2 was the first). Slice 5 retires the line with the file.
- **The phase-drop detector is VACUOUS ON THIS REPO and now says so out loud**
  (slice 4). Every phase reads `DevStg-Arch` while the four CMP rows are Drafted,
  so the detector abstains rather than attribute a repo-wide fact to a phase, and
  the bar axis's one live warn (phase 4) is replaced by one stand-down warn. The
  detector is correct and the repo's frame is genuinely in work — but it means
  **a real signal class has no home right now**: "the repo as a whole dropped
  below what its closed anchors recorded" is a true and useful event that no
  detector reports, because this one is scoped per phase. Whether the frame rungs
  deserve a REPO-level drop detector beside the per-phase one is a design question
  for the program close; it was deliberately not invented here, since a second
  detector is not a re-key.
- **`check_trajectory.py` is 4,496 lines and grew at five of the last six
  stamps** (slice 4). Its ratchet entry now says so. Each bump has been
  individually defensible — a checker gains checks — but "is this still ONE
  checker" is a question the module-size ratchet asks and nobody has answered.
  WI-483's decomposition program is the natural home; this slice deliberately did
  not open it.
- **A test module's `from kitlib import ...` resolves by ACCIDENT of collection
  order** (slice 4). `kitlib` is a package under `scripts/`, which nothing puts on
  `sys.path` until the first `load_script` call, so a module-level kitlib import
  in a test file works only if an earlier-collected module happened to call it.
  It held until an xdist worker collected `test_trajectory_arch` first and the
  module errored at import. Fixed explicitly in the three modules this slice
  touched; **`test_kitlib_stage.py`, `test_derive_stage.py` and
  `test_phase_rule.py` still carry the latent form** (and `test_kitlib_stage`'s
  `from conftest import SCRIPTS  # noqa: F401  (puts scripts/ on sys.path)`
  states a belief that is simply not true — importing conftest does not do it).
  Not swept here: they are other slices' modules and green today. Whoever touches
  them next should make it explicit, or `conftest` should do it once at import.
- **The anchor GRAMMAR moved but the PROSE that teaches it did not** (slice 4).
  `PHASE_ANCHOR_RE` and `RATIFY_ANCHOR_RE` now accept `[<phase>]-[DevStg-<Rung>]`
  and are held equal to each other by a test rather than by a comment. But the
  `gate-advance` skill, the PROCESS surfaces and the WI-146 records still teach
  `[phase]-[g1|g2]`, and `docs/concurrency-v2.md` still describes ratification
  "at the phase `[g2]` close". That is slice 5's vocabulary sweep by the program's
  own division of labour — noted here so the sweep has the new canonical spelling
  and the translation table to work from rather than re-deriving them.
