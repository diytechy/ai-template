+++
id = "WI-521"
title = "The decomposition debt owner: four wide modules, M-06's four test monoliths, and no sensor watching the test tree"
specref = "docs/plans/2026-08-25-remap-alignment.md"
workstream = "process"
sr_refs = []
needs = []
buildtier = "strong"
safety_class = "ordinary"
priority = 2
+++

## Context

**This row is the module-size ratchet's named DEBT OWNER.** The pointer in
`tests/test_module_size_ratchet.py` moved here from `WI-508` in the same commit
that filed this row, and the reason is the ratchet's own rule, applied one step
further than it has been before.

### Why the pointer moved rather than waiting for `WI-508` to close

The ratchet's docstring records the chain: it directed active debt to `WI-280`
for months after that item closed — "a ratchet whose commentary names a closed
item tells the next author that the debt is somebody's when it is nobody's,
which is the one thing a growth sensor must not do" — so `WI-483` took ownership
on its first day, and handed it to `WI-508` at its close.

Two things make a third hand-off at close the wrong mechanism:

1. **A close-time re-point is a promise; a filed row is a fact.** It has been
   honoured once, deliberately and with the defect named. Relying on it a second
   time makes the sensor's honesty depend on a future session remembering.
2. **`WI-508` was never the right owner for this AXIS, and the ratchet says so
   about its predecessor in the same words.** The docstring notes `WI-483`
   "CLOSED having paid down the axis it was scoped for ... which is precisely
   NOT this file's axis". The same is true here: `WI-508` is a **consolidation**
   program — minimize duplicated behaviour — while this ratchet measures module
   **size**, which is decomposition. `WI-508` inherited the pointer for being the
   live architectural program, not for being scoped to the axis.

So the pointer now names a row scoped to the axis it measures, and **`WI-508`'s
eventual close has nothing to re-point.** That is the dead-owner defect made
unreachable rather than deferred again.

**THIS ROW IS A STANDING DEBT OWNER, NOT A ONE-SITTING TASK.** Do not claim it
expecting to finish it. It is claimable for one scoped slice at a time, and it
is closed only when the debt below is paid or re-homed — and if it is ever
closed, **the ratchet pointer must move in the same commit**, which is the rule
it inherited.

### What it owns — 1: the four wide modules, corroborated from the requirements side

`WI-508`'s blind derivation produced evidence this debt has never had. Two agents
derived a minimal module map from the requirements alone, and where **both**
agreed two obligations belong in *different* modules while the live tree fuses
them, the fusion clusters hard:

| live module | obligation pairs both derivations put APART |
| --- | --- |
| `agent_loop` | 14 |
| `check_trajectory` | 13 |
| `agent_common` | 10 |
| `bootstrap` | 5 |
| `trace`, `check_privacy` | 2 each |
| `check`, `check_doc_refs` | 1 each |

fig: derived="pairs (x,y) of SRs where derivation A and derivation B each place x and y in different modules while the live SR->module join puts them in the same one; the live join reads LLR `module` cells through `sr_refs`"

These are the same four modules the ratchet has baselined as its largest, reached
by a completely independent route — from what the requirements say belongs
apart, not from line counts. **That agreement is the row's strongest asset**: a
size ratchet alone can be answered with "it is big because it does a lot"; this
says which obligations a reader has to hold at once to read it.

**It is NOT a mandate to split all four.** `WI-483` measured `check.steps` and
deliberately LEFT it on four recorded grounds, and that decision stands. Any
slice here re-measures first and may reach the same answer.

### What it owns — 2: M-06's four test monoliths, which now ride nothing

Re-measured at the `WI-483` close: `tests/test_integrate.py` **3,520**,
`tests/test_trace.py` **2,099**, `tests/test_trajectory_arch.py` **1,927**,
`tests/test_agent_loop.py` **1,640**.

`WI-483`'s item 4 ruled that a test split **rides along** with a subsystem
decomposition and that a standalone split slice was out of scope. That rule was
honoured for all seven of its slices and it delivered nothing: every slice
checked its touched tests and none needed a split. `WI-508` then filed no
subsystem decomposition at all, so there was no vehicle to ride.

**This row inherits them, and is explicitly NOT bound by that rule.** The
ride-along constraint was `WI-483`'s own scope decision, not a standing ruling,
and it has now failed to deliver across two programs — which is the evidence
that a rider with no vehicle is a rider that never moves. A standalone split is
in scope here. It should still be taken by stable behaviour boundary rather than
by line count, and a slice that decomposes a subsystem should still take its
tests with it.

### What it owns — 3: the sensor gap, and the unruled question under it

`tests/test_module_size_ratchet.py` censuses `SCRIPTS` only, so **no armed
sensor watches the test tree** — which is why three of the four monoliths grew
5–36% between the 2026-08-19 review and the `WI-483` close with nothing saying
so.

**Do not just extend the census.** That file's own docstring banks an unruled
owner question — whether the line-count axis survives at all, given the owner's
`OI-16` correction that "the monolith risk was always about FUNCTION size and
complexity, not file length" and the worked counterexample where a structurally
simpler `bootstrap.py` was made to demand a reviewed bump. Extending a disputed
axis to a second tree doubles whatever is wrong with it. The honest sequence is
to raise the axis question with the measurement this row can now supply, and
extend only what survives the answer.

### Standing constraints

- Every slice ends green at the commit bar; a baseline is re-stamped only
  deliberately, with the reason in the log, and **never to clear a finding**.
- Moving lines into a new module is the intended escape hatch: the new module
  stays under `THRESHOLD` or earns its own reviewed baseline, and the shrunk one
  re-stamps downward in the same commit.
- If this row closes, **move the ratchet pointer in the same commit.**

### SLICE 1 LANDED 2026-08-25 — the acceptance record leaves the checker

**The evidence was RE-DERIVED before anything was designed, and it does not say
what this row's table says.** The three-way agreement reproduces EXACTLY —
A vs LIVE **94.6%**, B vs LIVE **94.8%**, A vs B **97.0%** over the same 71 SRs
and 2,485 pairs — which is the strongest possible check that the re-derivation
reads the same partitions the alignment pass read. The FUSION table does not
reproduce:

| live module | recorded (WI-508) | re-derived | tie-break stable? |
| --- | --- | --- | --- |
| `check_trajectory` | 13 | **13** | YES |
| `agent_loop` | 14 | **11** | no — rests on ONE tied SR |
| `agent_common` | 10 | 10 | YES |
| `bootstrap` | 5 | 5 | YES |
| `trace` / `check_privacy` | 2 / 2 | 2 / 2 | YES |
| `check` / `check_doc_refs` | 1 / 1 | 2 / 0 | no — one SR swaps |
| **total** | **48** | **45** | |

fig: derived="pairs (x,y) of SRs where derivation A and derivation B each place x and y in different modules while the live SR->module join puts them in the same one; A and B read from their own `## Forward: every SR to exactly one owning module` tables, the live join reads LLR `module` cells through `sr_refs` and assigns each SR the module its rows name most often"

**Why the difference, and why it matters more than the difference.** The live
join's rule — *the module an SR's own LLR rows name most often* — is
**underdetermined for 13 of the 71 SRs**, whose top module is a TIE. `SR-026` is
a three-way tie between `agent_session`, `agent_loop` and `dispatch`; break it
toward `agent_loop` and that module reads 14 and heads the table, break it any
other way and it reads 11 and does not. **The head of this row's strongest asset
turns on one arbitrary tie-break**, and nothing recorded which way the original
run went. That is stated here rather than quietly corrected: the table is still
good evidence about WHICH modules fuse obligations, and it is not reliable about
their exact order.

**`check_trajectory` is the worst offender under BOTH tie-breaks, so the choice
needed no argument.** It reads 13 either way; it was the largest of the four
fusion heads at **4,963 lines** (`agent_loop` 3,614, `bootstrap` 3,146,
`agent_common` 2,643); it holds the kit's two most complex checker functions
(`main` 24, `interface_findings` 20); and unlike `agent_loop` — which `WI-483`
decomposed twice — nothing had ever come out of it.

**The boundary, in one sentence.** Everything that compares **two git trees**
cell by cell to answer whether attested text has moved away from the copy
recording its acceptance moved to `project-trajectory/scripts/acceptance_record.py`;
everything that asks what the registries say **today** stayed. 677 lines moved
VERBATIM: the §A5.1 cell split (`SPINE_TRACED_CELLS`/`SPINE_APPROVED_CELLS`,
`spine_cell_class`, `traced_cells`), the comparison (`SPINE_CSVS`,
`_spine_rows_at`, `_spine_revs`, `split_changed_cells`,
`staged_spine_amendments`), the two staged warns, and the mirror invariant in
both staged and committed form.

**The seam was FOUND, not carved, and the census is the proof.** The moved
block's only non-builtin dependencies in 4,963 lines of scope were
`spine_carrier` and one git primitive — no `argparse`, `csv`, `re`, `difflib`,
`configparser` or `pathlib`. `tests/test_acceptance_record.py` pins that as the
boundary rather than re-asserting rules already covered where they were.

**Both derivations asked for this module by name.** Team A's `A2` and team B's
`M06` are both "Acceptance Record", and 8 of `check_trajectory`'s 13 fused pairs
run through `SR-178`/`SR-179` — the largest single fusion reduction available in
the module. Mechanically it was already visible: `intake.py` imported a
4,963-line validator, and **all three of its executable uses were inside the
moved block**, so re-pointing them deleted the `intake -> check_trajectory`
import edge outright.

**Byte-identical, measured that way.** Nine driven CLI paths
(`check_trajectory` ×5 including `--staged` and a non-root `--root`, `trace
--strict`, three `intake` help surfaces, `baseline_snapshot --help`) and 56 API
probes over the live repo, capture-diffed against a HEAD-rebuilt scripts tree
after the harness self-diffed empty twice. **One intended difference and no
others**: `intake.py --help` prints its own docstring, which now names
`acceptance_record.staged_spine_amendments`.

**Ratchets: one re-stamped DOWN, one RE-KEYED, one reviewed bump.**
`check_trajectory.py` **4,963 → 4,327** (−636); `acceptance_record.py` is 758
lines, under `THRESHOLD`, so it opens no entry. The complexity entry for
`committed_snapshot_findings` (12) was RE-KEYED to the new file, not re-stamped —
the function is byte-identical and this file keys on (path, name), so a move has
to be spelled or the census reports the same 12 twice. `bootstrap.py` +7, the
MAPPING row and its reason.

**TOPOLOGY DECISION (recorded here because module moves touch the spine).**
Three LLR `Module` cells re-point and **no new spine row is minted** — the
instruction this row inherited is that a module move re-points TRACED cells only
(the `WI-483` slice 2/3 precedent), and re-pointing already contains the new
module, so a mint would have added `Drafted` rows to the owner's approval surface
for nothing. `LLR-158` and `LLR-202` name `acceptance_record.py` alone.
**`LLR-178` names BOTH**, on cause rather than symmetry: its attested rationale
says the mirror invariant "lives in `check_trajectory` rather than in
`baseline_snapshot` because the writer must not also be the judge of its own
writes", and its detail says it "joins the failure set at `check_trajectory`'s
main aggregation". Both stay literally true through the re-export and the
aggregation, and rewriting an `Approved` cell to tidy a diff is not a session's
act. `IF-091` (owner `LLR-158`, consumer `scripts/intake`) follows its owner and <!-- path-ok: the interface registry MODULE LABEL quoted from IF-091, not a file path -->
now declares `acceptance_record -> intake`, which is the live edge —
verified through `check_trajectory --strict`, which reported the containment
error before the re-point and the seam error before `intake` was moved, and is
CLEAN after both.

**One shared helper widened, because the cut needed it.**
`check_trajectory._git` was a FOURTH copy of `kitlib.git.git_out` that the
D-8/`OI-16` consolidation missed — the same body plus an optional `stdin`, which
is why it read as a different function. `stdin` is now a parameter on `git_out`
and both modules alias the one home (the `check.py` idiom). Recorded as a
consolidation act inside a decomposition slice rather than left unsaid.

**M-06 rides nothing here, and the reason is measured rather than inherited.**
The moved tier's tests live in `tests/test_trajectory_staged.py` (1,301 lines)
and `tests/test_baseline_snapshot.py` (966) — neither is one of M-06's four
monoliths, and both drive the tier through the CLI or the re-exported API, so
neither needed to move. The four monoliths are re-measured for the record:
`test_integrate.py` **3,520**, `test_trace.py` **2,099**,
`test_trajectory_arch.py` **1,993** (was 1,927 at the `WI-483` close — it has
grown again, with nothing watching), `test_agent_loop.py` **1,640**.

fig: cmd="python -c \"import pathlib; [print(len(p.read_text(encoding='utf-8').splitlines()), p.name) for p in sorted(pathlib.Path('tests').rglob('*.py'))]\"" rev=c3bc6e07

**The sensor gap stays CARRIED, not executed**, per this row's own §3.

**An accident, recorded because a session that hides one teaches nothing.** The
byte-identical harness drove `intake.py census` as if it were a read. It is not:
it minted `WI-522`/`WI-523` and COMMITTED the whole working tree. Reset with
`git reset --mixed`, the two minted specs deleted, and `docs/id-watermark`,
`docs/stage`, `docs/status.md`, `PROJECT_STATE.html` and
`components.derived.toml` restored to `c3bc6e07`; the watermark reads `WI = 521`
again and no id was spent. The harness now drives `--help` on the subcommands
instead, with the reason written at the site.

**STILL OWED BY THIS ROW after slice 1.** The three remaining fusion heads
(`agent_loop`, `agent_common`, `bootstrap`), the rest of `check_trajectory`
(4,327 lines, 5 fused pairs left, `main` still at complexity 24), M-06's four
monoliths, and the sensor gap. **Nothing here closes the row.**

**Deferred to the owner: nothing new.** `LLR-178`'s rationale now locates the
judge one indirection away from where the code sits; the multi-module cell keeps
the sentence true, so this is a finding, not a decision withheld.

### SLICE 2 LANDED 2026-08-25 — M-06's largest monolith, split standalone

**The rider finally has no vehicle to wait for, so it walked.** `WI-483`'s item 4
held that a test split RIDES ALONG with a subsystem decomposition; it was
honoured across seven slices and delivered nothing, `WI-508` filed no
decomposition at all, and slice 1 above found the same thing a third time — the
acceptance record's tests live in `test_trajectory_staged.py` and
`test_baseline_snapshot.py`, neither a monolith, and neither needed to move.
**Three programs, zero deliveries.** This row is explicitly unbound from that
rule, and slice 2 is the standalone split.

**Re-measured, and the worst offender is unambiguous.** `test_integrate.py`
**3,520** lines / 131 tests; `test_trace.py` 2,099 / 88;
`test_trajectory_arch.py` 1,993 / 86; `test_agent_loop.py` 1,640 / 66. No tie to
break here.

**The boundary is the file's OWN, not a line count.** It already carried seven
numbered banner sections; the split follows them, which is why it moves no
argument:

| module | subject | lines | tests |
| --- | --- | --- | --- |
| `test_integrate.py` | the CLAIM rung and the refusals in front of it | 932 | 42 |
| `test_integrate_admission.py` | what the slot ADMITS — outcome, the R1 mint refusal, the verdict gate, the declared bar, the branch harness, the window audit | 726 | 32 |
| `test_integrate_station.py` | the station protocol — refresh, attestation, merge slot — and the real-bar e2e | 1,129 | 36 |
| `test_integrate_unload.py` | the §5.6 unload of the branch and its worktree | 526 | 21 |
| `integrate_fixtures.py` | the shared surface (never collected) | 374 | — |

fig: cmd="python -c \"import pathlib; [print(len(pathlib.Path('tests',n).read_text(encoding='utf-8').splitlines()), n) for n in ('integrate_fixtures.py','test_integrate.py','test_integrate_admission.py','test_integrate_station.py','test_integrate_unload.py')]\"" rev=9c9e1aa7

**`tests/integrate_fixtures.py` follows `traj_fixtures.py`'s stated rule
exactly** (WI-277, which split a 5,359-line test monolith the same way): what
lives there is what MORE THAN ONE split module uses, **measured** — the git
plumbing, the repo builders, the pinned commit stamps, and the two builders whose
callers straddle a boundary (`scaffolded_closed_branch`, `_worktree_count`).
Anything one module uses moved WITH that module: `claim_dir`/`spec_move` to
claim, `verdict_repo` to admission, `station_repo` to the station,
`residue_lane` to unload.

**The proof is node-id set equality, not a green.** The collected node ids of the
four new modules are **byte-identical as a set** to the monolith's at `9c9e1aa7`
(133 ids, `diff` empty), and both sides run **132 passed / 1 skipped** — the skip
is the POSIX-only backslash test on Windows. Nothing was renamed, dropped or
quietly merged.

**+167 lines across the family** (3,520 → 3,687): four module docstrings that
each state their own subject, four import blocks, and the shared file's own
header. Nothing executable was added and nothing was deleted.

**Two tests were RE-HOMED rather than left where the line numbers put them.**
`test_the_git_dependency_is_declared_for_this_module` asserts the module's env
gate would have skipped — it went to the claim module; and
`test_bar_step_count_is_by_distinct_name_not_by_echoed_line` is a pure unit test
on the bar's step count in the merge record, so it went to the station beside the
bar it measures.

**The commit bar is unmoved, deliberately.** All three new modules join
`conftest.SLOW_MODULES` beside the one they came out of — same heavy class (real
git repos, real worktrees, the real bar in the e2e) — so smoke membership reads
**1,369 before and after** and the total **3,073 before and after**. A split that
quietly added 90 heavy tests to the per-commit bar would have been a regression
dressed as tidying.

**Spine: four `Evidence` cells re-pointed, TRACED only, no row minted.**
`TC-132` now names claim + admission + station (its `method` spans all three),
`TC-146` and `TC-148` follow their named tests to the station, `TC-145` stays on
the claim module. `Evidence` is a TRACED cell, so no attested prose moved;
`check_trajectory --strict` clean, `integrity=0`, `trace.py` findings unchanged.

**M-06 after this slice: one of four done.** `test_trace.py` (2,099),
`test_trajectory_arch.py` (1,993) and `test_agent_loop.py` (1,640) remain, and
the sensor gap stays CARRIED — extending a disputed line-count axis to a second
tree still doubles whatever is wrong with it.

**Deferred to the owner: nothing new.**

### SLICE 3 LANDED 2026-08-30 — M-06's second monolith, and the sensor gap is now owner-ruled

**The sensor gap this row's §3 CARRIED is no longer this row's to carry.** OI-68
was ruled 2026-08-30 (log 2026-08-30, `WI-537`/`WI-538` filed): the disputed
line-count axis §3 banked as an unruled owner question is settled — **(1c)** both
sensors stay armed and the module-size ratchet is re-based to SLOC, **(2a)** the
*complexity* sensor (not the line ratchet) is the one that censuses `tests/`, so
"`WI-521`'s refusal to extend a disputed axis to a second tree is honoured". The
test-tree sensor is the complexity sensor, filed as `WI-537` (report-only) →
`WI-538` (arm + re-base). `WI-538` carries a SOFT edge to this row and **amends
this §3** (IF-054: a hard edge on a standing debt owner would deadlock). So §3's
"raise the axis question with the measurement this row can now supply, and extend
only what survives" is discharged — the question was raised, ruled, and re-homed.
Nothing on the sensor gap is owed by this slice.

**WI-538 EXECUTED the ruling, 2026-08-30.** The complexity sensor is now ARMED in
this repo (`[step:complexity]`, `--mode enforce`, `docs/complexity-baseline`) and
its census covers `tests/` as well as the kit scripts, so the test tree has an
armed sensor for the first time — on the COMPLEXITY axis. The module-size line
ratchet was re-based from raw physical lines to SLOC in the same WI (OI-68 1c) and
stays scripts-only. **Residual this row still owns, stated honestly:** test-tree
SIZE growth — a monolith that accretes fixtures or test functions without any one
function crossing cognitive 15 — is watched by NEITHER armed sensor (the line
ratchet is scripts-only; the complexity sensor scores functions, not files). So §3's
test-monolith debt is real and unchanged; what closed is the AXIS question and the
per-function complexity watch, not a size measurement of the test tree.

**So this slice is the M-06 work, and the target is re-measured, not inherited.**
`test_trace.py` **2,323** (was 2,099 at slice 2 — it grew again, with nothing
watching), `test_trajectory_arch.py` **2,290** (was 1,993), `test_agent_loop.py`
**1,640**. The two that grew are the sensor gap in action, exactly what OI-68
now closes.

fig: cmd="python -c \"import pathlib; [print(len(pathlib.Path('tests',n).read_text(encoding='utf-8').splitlines()), n) for n in ('test_trace.py','test_trajectory_arch.py','test_agent_loop.py')]\"" rev=56e7e52b

**The near-tie was broken by the boundary, per this row's own rule.** `test_trace`
and `test_trajectory_arch` are 33 lines apart — no line-count winner — and the
row splits "by stable behaviour boundary rather than by line count". `test_trace`
splits along `trace.py`'s own tiers, and one is a genuinely self-contained
subsystem: the **IF-### interface-seam tier** (`process.md` §8), with its own
carrier (`interfaces.toml`/`.csv`), its own closed vocabularies, its own
reachability advisory, and nine dedicated helpers used by nothing else in the
file (`_ifs_toml`, `_write_ifs`, `_report`, `_warn_run`, `_if_row`,
`_toml_write`, `_toml_warn_run`, `_toml_finding_run`, `_seam_scaffold`).
`test_trajectory_arch`'s sections are heterogeneous rules with no comparable
seam, so the boundary — not the 33 lines — chose `test_trace`.

**The seam was FOUND, not carved.** The tier is one contiguous banner block
(`WI-056` through the `WI-065` seam-citation tests), and its only cross-boundary
tie was the two-line `_report` reader, which four core sites also used. `_report`
moved WITH its cluster and those four sites were inlined to the trace family's
own idiom (`tests/test_trace_rules.py` reads `report.md` inline the same way) —
the only non-move edit in the slice, recorded rather than left unsaid.

| module | subject | lines | tests |
| --- | --- | --- | --- |
| `test_trace.py` | the SN→SR→LLR→TC spine: orphan/strict gates, the four verification-category buckets, the schema-safe extra columns, the SN status vocabulary, the Drafted exemptions, the approved-phase rule | 1,370 | 52 |
| `test_trace_interfaces.py` | the IF-### interface-seam tier: id integrity + owner-shape findings, the IF+CMP schema warns, the endpoint reachability advisory, the OI-67 owner/consumers reshape + carriage, the WI-065 seam citation | 978 | 40 |

fig: derived="len(splitlines()) and the collected `::` count of each split module in this commit's tree; the pre-split `test_trace.py` was 2,323 lines / 92 tests at 56e7e52b, so the family is +25 lines (the new module's docstring + import block, plus ruff rewrapping the four inlined `_report` reads) and the 92 tests are conserved 52+40"

**The proof is node-id set equality, not a green.** The sorted collected node-id
sets of the two modules are **byte-identical as a set** to the pre-split
`test_trace.py` at `56e7e52b` (92 ids, `diff` empty), and both run **91 passed /
1 skipped** — the skip is the POSIX-only provenance-allow test on Windows,
unchanged. Nothing was renamed, dropped or merged.

fig: derived="the sorted collected node ids of tests/test_trace.py + tests/test_trace_interfaces.py in this commit, stripped to `::name`, diffed against the same for tests/test_trace.py at 56e7e52b — empty diff, 92 ids each side"

**The commit bar is unmoved, deliberately.** `test_trace_interfaces` joins
`conftest.SLOW_MODULES` beside `test_trace` — same heavy class (a real `trace.py`
subprocess per test) — so both stay OUT of the `-m smoke` tier and smoke
membership is unchanged (1,378 collected before and after). A split that added 40
subprocess tests to the per-commit bar would have been a regression dressed as
tidying.

**Spine: three `Evidence` cells re-pointed, TRACED only, no row minted.** The
live `TC` rows whose `evidence` named a moved test now name
`tests/test_trace_interfaces.py` (`test_if_tier_integrity`,
`test_channel_refuses_an_unknown_value_as_a_warn`,
`test_missing_required_if_field_is_a_warn`); the sibling ids in those same cells
that stayed (`test_out_of_vocabulary_aspect_is_a_schema_finding`,
`test_critique_verification_value`) were left. `Evidence` is a TRACED cell, so no
attested prose moved; `check_trajectory --strict` clean, `integrity=0`,
`interface-findings=0`, `trace.py` findings unchanged (SR-181's orphan is the
pre-existing one owned elsewhere).

**M-06 after this slice: two of four done** (`test_integrate`, slice 2;
`test_trace`, here). `test_trajectory_arch.py` (2,290) and `test_agent_loop.py`
(1,640) remain.

**Deferred to the owner: nothing new** — OI-68's ruling already re-homed §3's
sensor/axis question to `WI-537`/`WI-538`.
