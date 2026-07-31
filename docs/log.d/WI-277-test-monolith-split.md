## 2026-07-31 — WI-277 split the test monoliths by stable behavior boundary

Slices S6–S8 only: the three splits that are **independent of the anchor**.
`tests/test_gen_trajectory.py` (S1–S5) is deliberately NOT touched here — its
production module is being decomposed on another branch, and splitting the test
monolith before its seams settle would just move the churn.

Every move is a **verbatim cut-paste** (docstrings and comments included —
several encode owner rulings). No test was renamed, re-tiered, re-ordered or
had its assertions touched; the edits are the three **parent** docstrings
(each gaining a forwarding pointer to its new siblings), the new module
docstrings, the per-module import lines, the helper copies, and **three comment
repairs in S8** (each flagged inline with `WI-277`) where a moved comment would
otherwise have pointed at a file it no longer lives in.

The mechanical check, stated as what it actually shows (the round-1 reviewer
re-cut it stricter — decorators included, duplicate-aware — and their numbers
are the ones below): across trunk's three parents and the resulting modules,
**all 405 top-level functions survive, and exactly ONE body differs** —
`test_parse_map_rejects_entry_without_equals`, the only repair that sits inside
a function. The other two repairs are **module-level section dividers**, which a
function-body comparison cannot see at all. `_vendor_core` is not a changed body
but an added **copy** carrying a copy note; trunk's original survives
byte-identical at `tests/test_agent_loop.py:568`. And `_git` is a **comparison
artifact, not a difference**: trunk already carried two distinct `_git` helpers
(`test_agent_loop.py:154`, `test_agent_loop_worker.py:78`) that differ only in a
local name (`proc` vs `p`); both survive unchanged, and a name-keyed script
collapses them into a phantom diff. All 12 decorated functions' `@parametrize`
blocks are byte-identical — the check that matters most, since a mutated
parametrize is how a split drops cases while keeping every function name.

The suite idiom is preserved: **no test module
imports another**, `conftest.py` stays the only shared home, and the small
fixture writers are **copied per module** with the standard "copied rather than
imported" note (the shape `tests/test_integrate.py::git_repo` states). No new
shared fixture module was created — the plan reserved that for the anchor split,
where the fixtures genuinely express a test API.

### The smoke-tier hazard, and how each slice defused it

`tests/conftest.py` tiers by module **stem**, and an unlisted stem defaults to
`smoke`. So splitting a slow monolith mints new stems that silently rejoin the
per-commit bar — and the WI-281 membership ratchet is blind to a single
omission. Each new stem was therefore added to `conftest.SLOW_MODULES` **in the
same commit as the module it names**, and the split's guard is the two
collect-only counts below: the total must not move (no test dropped) and the
smoke count must not move (no stem forgotten).

The three trajectory / two trace / two agent-loop stems inherit their parent's
tier because they inherit their parent's **cost class** (`run_py` subprocesses
over temp registries / scaffolds / live git repos). That is what makes the
split behavior-preserving.

**The deliberate re-tier: recorded, not taken.** Two of the new modules —
`test_trajectory_arch` (in-process `load_script("check_trajectory")` decisions,
plus the subprocess-driven interface/coupling groups) and, more clearly,
`test_trace_rules` and `test_agent_loop_routing` — are dominated by *in-process*
decision tests, exactly the class WI-281 kept in the commit bar. Splitting them
out is what first makes a re-tier *possible* at module granularity. It is not
taken here: moving a module into the bar is a **measured** decision (module wall
cost against the declared `[smoke-budget]` seconds in `docs/stack.ini`), and
mixing it into a behavior-preserving move would make both unreviewable. It is
left as the option the owner/queue can take later, on its own measurement.

### Permanent guard

`tests/test_smoke_tier.py` gained `test_wi277_split_modules_stay_slow` — every
stem this WI minted must map to `"slow"` via `smoke_tier_for`. Cheap, permanent,
and it fails loudly if a future edit drops a `SLOW_MODULES` line (the failure
mode the ratchet cannot see).

### S6 — `tests/test_trajectory.py` (2,808 lines, 151 tests)

Kept in the parent (**56 tests**): the parse + decision core — vacuous/opt-out,
graph validation, cycles and deep chains, soft `~` edges, SR refs, the R-A/R-E/
R-F SSOT rules, SpecRef anchor resolution, the terminal `retired` status,
status.md forward-only (R-D), and the WI-284 generated-frontier cascade.

| new module | behavior boundary | tests | moved from |
| --- | --- | --- | --- |
| `test_trajectory_staged.py` | git effect + recovery | 25 | `--staged` no-validation-delta, WI-316 spine-amend-without-flip (incl. the BOM case), the WI-068 critique-loop ratchet, WI-205 backlog staleness, WI-243 critique staleness, and the §5.4 latest-critique **selection-by-git-time** tests |
| `test_trajectory_arch.py` | decision over architecture inputs | 45 | WI-056 interface coverage, WI-073/FB5 top-view bound, WI-153 knowledge⇒component coupling, WI-093 phase anchors + drop detector, WI-146(b) ratify-brief view lint, WI-064 cross-CMP-edge-without-IF, WI-191 spec interfaces |
| `test_trajectory_specs.py` | decision over spec bodies | 25 | WI-349 control-character cell integrity, WI-352 completion reconciler (Done-when completion, the section boundary, the warn-only trailer, the close-time half, the signal deliberately not reimplemented) |

56 + 25 + 45 + 25 = **151** — the parent's exact test count, redistributed.
`os`, `subprocess` and `skip_without_env_gates` left the parent's imports with
the last test that used them (ruff-verified, not eyeballed).

Collect-only: **1713 → 1714 total**, **556 → 557 smoke**. The single `+1` on
both sides is the new permanent guard test in `test_smoke_tier.py` (a smoke
module); the **slow** count is unchanged at 1157, which is the number that would
have moved had a stem been forgotten or a test dropped.

### S7 — `tests/test_trace.py` (2,304 lines, 81 tests)

Kept in the parent (**44 tests**): the scaffold-driven half — orphan detection,
strict/schema gates, the verification-category buckets (Test / Attest /
Demonstrated / Critique), phase scoping, the generated outline / Mermaid / HTML
render, the schema-safe optional columns, the WI-056 IF seam tier, WI-065 seam
citations, the WI-089/WI-090 Draft exemptions, the WI-188 ratified-phase rule
and the repo-review regressions.

| new module | behavior boundary | tests | moved from |
| --- | --- | --- | --- |
| `test_trace_rules.py` | pure decision, in-process | 21 | the spine-prose predicates (a row states the system not its own history; one testable obligation; the paraphrase advisory that warns but never gates; the optional LLR Rationale column), WI-229/WI-364 supersession integrity, the WI-129 LLR/TC status-coherence lint, the WI-146(a) `--ratify` view, and the WI-081 Slice C helpers (`_bucket_by_ref`, `exit_code`) |
| `test_trace_briefs.py` | git effect + recovery | 16 | WI-316 `--ratify modified` (baseline walk, `--since`, off-git degradation, a BOMmed baseline) and the WI-325 freshness gate on it, whose load-bearing case is that `--check` reads the baseline the FILE declares |

44 + 21 + 16 = **81** — the parent's exact test count. `tests/golden/` and
`test_trace_golden.py` were not touched.

Two deviations from the plan's line ranges, both resolved by CONTENT (the plan
said to relocate by name where the ranges had shifted):

- The WI-081 Slice C block (`_bucket_by_ref` + the `_findings_stub` exit-code
  policy) sits *after* the reattest-brief section on disk, so the plan's single
  range for briefs would have swept it in. The plan names it under **rules**,
  which is also where it belongs by behavior (two pure helpers, no git), so
  `test_trace_rules.py` is two ranges rather than one.
- The plan's gloss listed "draft exemptions" under rules, but the WI-089/WI-090
  draft tests are scaffold-driven and sit inside the parent's own stated range;
  moving them would have split the WI-090 section mid-way. They stay with the
  scaffold half. Net: rules 21 (plan estimated ~27), briefs 16 (~14),
  parent 44 (~40) — the redistribution, not the total, moved.

Every git-backed test left the parent, so `skip_without_env_gates` and `SCRIPTS`
left its imports with them — and the WI-333 note explaining *why*
`skip_without_env_gates` is imported rather than assumed moved verbatim to
`test_trace_briefs.py`, which now hosts the tests it guards. A comment that
outlives the code it documents is how the next reader gets misled.

Collect-only: **1714 total / 557 smoke, both unchanged** (1157 slow).

### S8 — `tests/test_agent_loop.py` (2,256 lines, 111 test functions)

Kept in the parent (**56 functions**): everything that needs the
`FAKE_AGENT`/`loop_repo` subprocess harness — the exit/stall/budget ladders,
the guardrails injection matrix, throttle and error handling, the dirty-tree
and telemetry effects, the live status line, the `_git` helper and zero-commit
guards, the per-checkout coordinator lock, and the repo-review regressions.

| destination | behavior boundary | fns | moved from |
| --- | --- | --- | --- |
| `test_agent_loop_routing.py` *(new)* | pure decision | 21 | the WI-080 Slice C `RoutingState` transitions (phase pick, `route_intent` family exclusions and tier pins, `apply_decision`, critique/review verdict bookkeeping, `note_session`/`stall_verdict`), the WI-264 win-stay policy executed end to end in process, and the Slice D `classify_outcome` ladder |
| `test_agent_loop_policy.py` *(new)* | parse / decision | 26 | the §5.6 tracked pause, the WI-148 blackout edge/wake/wrap parsers, the WI-261 banner + countdown, both `seconds_until_reset` clock readings, the declared-policy parser agreement, `parse_map`, the WI-080 Slice B session-construction seams, the WI-274/IF-068 dial precedence, and the **ungated** Slice D/E main() seams (`worker_exit_banner`, `build_worker_assignment`'s not-a-worker case, `parse_args` defaults) |
| `test_agent_loop_worker.py` *(existing)* | git effect (worker leg) | 8 | the Slice D `worker_endstate` block and the git-backed Slice E `build_worker_assignment` cases, with the `_train_repo`/`_build_commit` helpers |

56 + 21 + 26 + 8 = **111** — the parent's exact function count. As collected
(parametrized cases expanded): `test_agent_loop` 121 → 58, `test_agent_loop_worker`
23 → 31, plus routing 29 and policy 26. **121 + 23 = 58 + 31 + 29 + 26 = 144.**

No new stem for the worker block, as planned: it appends to the module that
already owns the worker leg and its own equivalent `_git`, so the moved tests
need neither a copy nor an import.

**Round-1 review fix (MINOR).** The first cut of this slice put the whole Slice
D/E block in the worker module — including three tests that touch no git. That
module carries a module-wide `pytestmark = env_gate_skipif("git")`, so those
three inherited a gate they never had: the reviewer drove both sides with git
off `PATH` and got **3 passed on trunk, 3 SKIPPED on the branch**. Three pure
seams would have stopped running on an ungated machine, silently — the very
failure mode the `WI-333` note S7 was careful to move verbatim is about. The
fix is the boundary the WI is named for: the pure units live in the ungated
policy module, the git-dependent ones stay in the worker leg. The worker
module's block header now says plainly that its mark *adds* a gate, so nobody
parks an ungated test there again. The behavior-preservation claim holds only
after this fix; before it, this slice had exactly one exception.

Deviations, all in the direction of *not splitting a coherent section in half*:

- The WI-080 **Slice B** seams moved whole (6 functions: `session_model`,
  `session_template`, and the four `compose_session_prompt` cases) rather than
  the four the plan named. The section's own comment says "the three
  session-construction functions"; leaving two behind would have left that
  header lying in the parent about tests that were no longer there.
- `test_seconds_until_reset_weekly_same_weekday` moved alongside
  `..._parses_both_clock_formats`. The plan named only the latter, but they pin
  the same pure function and splitting them serves nothing.
- Three section dividers are now **in both modules** (`WI-148 weekday blackout`,
  `WI-080 Slice A`, `WI-274 part B / IF-068`) because each heads tests on both
  sides of the boundary — the loop_repo end-to-end guard stays with the parent,
  the parser moves. Duplicating a divider is cheaper than orphaning one.
- `_vendor_core` is **copied** into the policy module (the parent still uses its
  own), with the standard "copied rather than imported" note.

Three comments were repointed rather than moved verbatim, each flagged inline
with `WI-277` so the edit is visible in review: two `above` references
(`parse_map`'s "the preflight above", the Slice C banner's "the golden-net
suites above") that would have dangled once their referent was in another file,
and a note on the Slice D header recording that its worker half went to the
worker module. The S7 rule again: a comment that outlives the code it documents
misleads the next reader.

Collect-only: **1714 total / 557 smoke, both unchanged** (1157 slow).

### Verification

Run at the close of each slice with
`c:\Projects\ai-template\.venv\Scripts\python.exe`:

```
python -m pytest -q --collect-only        1713 -> 1714 (S6, the new guard) -> 1714 -> 1714
python -m pytest -q -m smoke --collect-only   556 -> 557 (S6) -> 557 -> 557
python -m pytest -q -n auto -m smoke      1 failed, 552 passed, 4 skipped
```

The full unfiltered suite, run over the final S8 tree (the slice/close bar):

```
1 failed, 1701 passed, 12 skipped in 674.43s (0:11:14)
```

1701 + 1 + 12 = **1714** — the collected total, all of it actually executed.

The single red is the standing `test_check_lane.py::test_this_repo_is_not_a_work_branch`
— expected on a claimed branch, never chased.

`check_docs --root . --ignore docs/test/report.md --ignore "docs/work/*" --stale`
→ `OK - 331 doc(s), 933 intra-repo link(s), 0 broken` (330 before the round-1
review doc landed).
`check_trajectory --root . --strict` → `clean (375 work item(s), 359 done (96%),
14 retired, graph acyclic)`.

#### After the round-1 review fixes

Collect-only **1714 total / 557 smoke / 1157 slow — all three unmoved** (the
three tests changed module, not existence). Per module: `test_agent_loop` 58,
`_policy` 26, `_routing` 29, `_worker` 31 = **144**, still `121 + 23`. Smoke
`1 failed, 552 passed, 4 skipped` (the standing work-branch red). The affected
modules together — the four `test_agent_loop*` legs, the four `test_trajectory*`
legs and `test_smoke_tier` (the `test_trace*` legs are NOT in this set; measured
2026-07-31) — run `297 passed, 1 skipped`, the lone skip being the pre-existing
POSIX-only advisory-lock case, not a split artifact. The reviewer's own method, rerun —
with git off `PATH`, `pytest tests/test_agent_loop_policy.py -k "<the three>"`
now gives **3 passed, 23 deselected** (was 3 skipped). The strict AST check
rerun after the moves: **405/405 survive, exactly one body differs** (the
`parse_map` repoint), matching the reviewer's number.

### What this WI still owes

The anchor split (`tests/test_gen_trajectory.py`, plan slices S1–S5) is
deliberately not started: its production module is being decomposed on another
branch, and the plan's shared-fixture module for it should express the seams
that decomposition settles on, not the ones it is about to move. That work
resumes once the production split merges.

> *Settled the same day* — WI-280 merged and the anchor split ran; see the
> next section.

## 2026-07-31 (later) — WI-277 the ANCHOR split (S1–S5)

WI-280 merged, so the deferred half ran. `tests/test_gen_trajectory.py`
(5,359 lines, 163 tests after the trunk merge) is now **eight modules**, cut
along the seams WI-280 drew in production — the same reason the anchor waited:
the split had to express the seams the decomposition settled on, not the ones it
was about to move.

The merge itself had one conflict, in `tests/test_trajectory.py`: trunk appended
the WI-280 `_render_surface_paths` pair to a file S6 had already split.
Resolved by carrying both tests **verbatim** into `test_trajectory_staged.py`,
beside the critique-staleness warn whose watched file set they pin — never by
hand-merging the two shapes.

### The anchor inventory

| module | subject (WI-280 sibling) | tests | lines |
| --- | --- | --- | --- |
| `test_gen_trajectory.py` *(stays)* | the facade + CLI | 14 | 295 |
| `test_traj_parse.py` | `traj_parse.py` — sources + the git/subprocess seam | 5 | 233 |
| `test_traj_graph.py` | `traj_graph.py` — layout + wire routing | 25 | 770 |
| `test_traj_views.py` | `traj_views.py` — What / When / How-SW | 37 | 897 |
| `test_traj_panels.py` | `traj_panels.py` — Knowledge / Process / next-work | 31 | 691 |
| `test_traj_render.py` | `traj_render.py` — primitives + design system | 32 | 1,290 |
| `test_traj_render_sweeps.py` | `traj_render.py`, swept not sampled | 12 | 718 |
| `test_traj_status.py` | `traj_status.py` — the `--status` snapshot | 7 | 209 |

14 + 5 + 25 + 37 + 31 + 32 + 12 + 7 = **163**, the anchor's exact test count.

`test_traj_render` and `test_traj_render_sweeps` share a production subject and
split on **assertion shape** instead: the first pins one emitter at a time, the
second walks `_every_emitter_document` and asserts a CLOSED property over every
member. That is the boundary a reader needs; one 1,800-line module is not.

### The one sanctioned shared module: `tests/traj_fixtures.py`

S6–S8 created no shared module and copied fixtures per module. The anchor cannot:
`_every_emitter_document` composes `make_repo`, `with_bundle`, `_flat_bundle`,
`tiered_repo` + `TIER_UNION_WIS`, `containerize`, `_how_sw_flat`, `with_gate`,
`gen` and `html_of` — builders whose homes land in **four different** split
modules — and it is called from both `test_traj_render_sweeps` and
`test_traj_graph`. Copying that per module would fork the one place the emitter
list lives, which is precisely what its docstring says it exists to prevent.

So `tests/traj_fixtures.py` holds it: no `test_` prefix, therefore never
collected, imported the way `conftest` is. **No test module imports another test
module** — the S6–S8 idiom is intact. `_every_emitter_document` moved
byte-identical; its docstring encodes the 2026-07-30 owner ruling on
shipped-vs-fresh truth-times.

Membership is **measured, not chosen**: a name lives here iff more than one of
the eight modules uses it (computed from the anchor's own reference graph, then
re-proved by `ruff check` on the result — an over-inclusive fixture module shows
up as an unused import somewhere, a missing one as an `F821`). Anything used by
exactly one module moved with that module: `make_status_repo`, `status_text`,
`block_of`, `_know_section`, `_loops_div`, `_hero_of`, `_landing_dashboard`,
`_label_boxes`, `_spine_with_sns`, `sw_section`, `_sample_path_d`,
`_viewbox_of`, `_scrambled_spine`, `_SubprocessShim`, … .

That measurement put **six names in the fixture module that the WI's plan had
listed elsewhere**, each recorded rather than quietly absorbed:

| name | measured users |
| --- | --- |
| `_wcag` | render (4 tests), panels (1), sweeps (2) |
| `_css_var` | panels (1), sweeps (2) |
| `_style_surfaces` | render (2), sweeps (2) |
| `_palette_vocabularies` | render (1), sweeps (1) |
| `SMALL_WIS` | views (2), panels (2) |
| `_layer_with` | views (3), render (3) |

The plan's parenthetical ("`_wcag` … used by exactly ONE module") was a guess
the measurement refutes: `_wcag` is the WCAG contrast primitive, and three
different modules assert floors with it. The alternative — copies in three
modules — is the duplication this WI exists to remove.

The module's own docstring carries the standing instruction not to let it
accrete: a helper one module calls belongs in that module, and a second caller
has to be justified the same way these six were.

### Smoke-membership proof

Tiering is by module **stem**, and an unlisted stem defaults to `smoke`. Seven
new stems each joined `conftest.SLOW_MODULES` **in the same commit as the module
it names**, with the same reasoning S6–S8 used: identical cost class (every test
drives the real `gen_trajectory.py` through `run_py`), so they inherit the
parent's tier — behavior-preserving, not a re-tier.

`tests/test_smoke_tier.py::test_wi277_split_modules_stay_slow` gained the seven
stems **and a derived half that needs no future editing**: every
`tests/test_traj_*.py` on disk must map to `"slow"`. A ninth sibling that
forgets its `SLOW_MODULES` row now reds without anyone remembering to extend a
literal. It was folded into the existing test rather than added beside it, so
the slice guard below stays a clean signal.

The guard, run at every slice close (`.venv` interpreter, as above):

```
python -m pytest -q --collect-only            1716   (S1..S5: 1716 1716 1716 1716 1716)
python -m pytest -q -m smoke --collect-only    557   (S1..S5:  557  557  557  557  557)
python -m pytest -q -m slow  --collect-only   1159   (S1..S5: 1159 1159 1159 1159 1159)
```

All three flat across all five slices. Smoke unmoved is the proof no stem was
forgotten (a forgotten stem moves 163-odd tests from slow into smoke); total
unmoved is the proof no test was dropped.

### Loss proof (AST, run over the final tree)

Trunk's pre-split anchor vs. the eight modules + `traj_fixtures.py`, comparing
every top-level name's source segment byte for byte:

```
before: 282 top-level names
after : 282 top-level names across 9 files
MISSING (dropped): none
EXTRA (new): none
DUPLICATED across modules: none
BODY CHANGED (0):
test functions: before=163 after=163 equal=True
```

Nothing dropped, nothing invented, nothing copied into two homes, and **zero
bodies differ** — including the four monkeypatch sites WI-280 repointed to
`gt.traj_parse.subprocess` / `gt.traj_graph._detour_points` /
`_lane_candidates`, which arrived already repointed on trunk and so needed no
edit here.

### Deviations

Three, all in the direction of keeping a coherent section whole and the shared
module small:

- **The T7 scale-to-fit pair goes to `test_traj_views`**, which the WI's
  per-module lists did not name at all. Both tests drive `_spine_with_sns`, the
  What-icicle fixture, and the section they sit in is literally headed
  "T7 + T4" — one banner, one behavior. Sending them to the render module would
  have made `_spine_with_sns` a third shared fixture for no gain.
- **`test_u3_sw_drill_has_a_legend_and_a_wired_detail_aside` goes to
  `test_traj_views`** rather than travelling with the rest of the design-system
  block. It asserts on the containerized How-SW section through
  `sw_section`/`containerize`; keeping it with its view keeps `sw_section`
  single-homed.
- **Six extra names in `traj_fixtures.py`** (the table above), because the
  measurement disagreed with the plan's guess.

One incidental fix, reported rather than buried: with the other `sys` users
gone, the facade's module-level `import sys` became redundant against the local
one inside `test_gen_trajectory_self_heals_sibling_import` (ruff `F811`). The
**module-level** import was dropped, not the local one — the local import is
part of what that test deliberately exercises, and this way the test body stays
byte-identical to trunk, which is what the loss proof above reports.

### Verification

Per slice: `ruff format` **and** `ruff check` (both, every time — a recent WI
shipped seven `F401`s by running only `format`), the three collect-only counts
above, the split family green, and

```
python -m pytest -q -n auto -m smoke      1 failed, 552 passed, 4 skipped
check_docs  --root . --ignore docs/test/report.md --ignore "docs/work/*" --stale
            -> OK - 333 doc(s), 934 intra-repo link(s), 0 broken
check_trajectory --root . --strict
            -> clean (376 work item(s), 360 done (96%), 14 retired, graph acyclic)
```

The single red is the standing
`test_check_lane.py::test_this_repo_is_not_a_work_branch` — expected on a
claimed branch, never chased.

The split family itself, run whole after S5:

```
python -m pytest -q -n auto tests/test_gen_trajectory*.py tests/test_traj_*.py
174 passed
```

174 = the anchor's 163 + the 11 in `test_gen_trajectory_pending.py`, which this
WI did not touch.

The full unfiltered suite (the WI/slice close bar), run over the final tree:

```
python -m pytest -q -n auto
1 failed, 1703 passed, 12 skipped in 355.37s (0:05:55)
```

1703 + 1 + 12 = **1716** — the collected total, all of it actually executed, and
the same 1716 the pre-split anchor produced.
