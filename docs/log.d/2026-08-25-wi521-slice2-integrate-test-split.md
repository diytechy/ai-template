## 2026-08-25 — WI-521 slice 2: M-06's largest monolith, split standalone

**Summary.** `tests/test_integrate.py` (3,520 lines, 131 tests — M-06 of the
2026-08-19 repository review, and the largest of the four) is now four modules
plus a shared fixture surface, split along the file's **own** seven banner
sections. `WI-483`'s rule that a test split rides along with a subsystem
decomposition had by now failed to deliver across three programs — its own seven
slices, `WI-508`'s zero decompositions, and this row's slice 1, whose tests
lived in two non-monolith modules — so `WI-521` used the freedom it was filed
with and took it standalone.

Deferred open items: none — the split needed no ruling and files no new
question.

### The boundary is the file's own

| module | subject | lines | tests |
| --- | --- | --- | --- |
| `test_integrate.py` | the CLAIM rung and its refusals | 932 | 42 |
| `test_integrate_admission.py` | what the slot ADMITS — outcome, the R1 mint refusal, the verdict gate, the declared bar, the branch harness, the window audit | 726 | 32 |
| `test_integrate_station.py` | the station protocol — refresh, attestation, merge slot — plus the real-bar e2e | 1,129 | 36 |
| `test_integrate_unload.py` | the §5.6 unload of the branch and its worker worktree | 526 | 21 |
| `integrate_fixtures.py` | the shared surface, never collected | 374 | — |

fig: cmd="python -c \"import pathlib; [print(len(pathlib.Path('tests',n).read_text(encoding='utf-8').splitlines()), n) for n in ('integrate_fixtures.py','test_integrate.py','test_integrate_admission.py','test_integrate_station.py','test_integrate_unload.py')]\"" rev=9c9e1aa7

`tests/integrate_fixtures.py` follows the rule `tests/traj_fixtures.py` states
for itself (WI-277, which split a 5,359-line test monolith the same way): what
lives there is exactly what MORE THAN ONE split module uses, **measured** — the
git plumbing, the repo builders, the pinned commit stamps, and the two builders
whose callers straddle a boundary (`scaffolded_closed_branch`, built by the
station's e2e and reused by the unload queue tests; `_worktree_count`, the other
way round). Anything a single module uses moved WITH that module.

### The proof is node-id set equality, not a green

The collected test node ids of the four new modules are identical AS A SET to
the monolith's at `9c9e1aa7` — 133 ids, `diff` empty — and both sides run
**132 passed / 1 skipped** (the skip is the POSIX-only backslash test, on
Windows). Nothing was renamed, dropped or quietly merged. The carve itself was
line-range based rather than node based, so every banner comment and the
blank-line rhythm travelled with the code it precedes, and the generator
asserted that every source line from 126 to the end was emitted exactly once.

Two tests were RE-HOMED rather than left where their line numbers put them:
`test_the_git_dependency_is_declared_for_this_module` (the env-gate assertion)
went to the claim module, and `test_bar_step_count_is_by_distinct_name_not_by_
echoed_line` — a pure unit test on `integ._passed_steps` — went to the station,
beside the bar whose merge record it measures.

+167 lines across the family (3,520 → 3,687): four module docstrings that each
state their own subject, four import blocks, and the shared file's header.
Nothing executable was added and nothing was deleted.

### The commit bar is unmoved, deliberately

All three new modules join `conftest.SLOW_MODULES` beside the one they came out
of — the same heavy class (real git repositories, real linked worktrees, the
real `check.py` bar in the e2e). Smoke membership reads **1,369 before and
after**; the full collection reads **3,073 before and after**. A split that
quietly moved ~90 heavy tests into the per-commit bar would have been a
regression dressed as tidying, and the membership ratchet would have caught it —
that it did not fire is the point.

### Spine

Four `Evidence` cells re-pointed and no row minted. `TC-132` names claim +
admission + station (its `method` spans all three); `TC-146` and `TC-148` follow
their named tests to the station; `TC-145` stays on the claim module. `Evidence`
is a TRACED cell, so no attested prose moved and no re-attest window is armed.
`check_trajectory --root . --strict` clean, exit 0; `trace.py --strict`
`integrity=0` with its pre-existing findings unchanged (`SR-181` orphan,
`LLR-197` advisories).

### Deviations from spec

- The spec's §2 says a split "should still be taken by stable behaviour boundary
  rather than by line count". It was, and the boundary needed no invention: the
  file already carried seven numbered banner sections and the four modules are
  those sections regrouped, which is why the split moves no argument about what
  `integrate.py` guarantees.
- No ratchet moved, because none watches this tree — which is the row's §3 gap,
  still CARRIED and still not executed.
- The generator overwrote its own source file on one iteration (it re-reads
  `tests/test_integrate.py`, which had already become the claim module).
  Recovered with `git checkout --` from `9c9e1aa7` and re-run; nothing was lost
  and nothing was committed in that state.
- No byte-budgeted file was touched.

### Bar

Commit bar: `pytest -q -n auto -m smoke` **1363 passed, 6 skipped**;
`check_smoke_budget.py --mode enforce` **23.3 s vs 60 s → within**;
`check_docs.py --root . --stale` OK (1096 docs, 1439 links, 0 broken).

One honest wobble worth stating rather than smoothing: the final bar's first
enforced measurement read **50.8 s** and a bare `-m smoke` beside it read
60.3 s — the recorded external-load caveat (another repo's loop intermittently
loads this box), not a regression. An immediate re-run measured 23.3 s. THE
BUDGET WAS NOT RE-STAMPED and both readings were inside it anyway.

Full unfiltered suite, batched at the smoke/slow boundary and summed against
`--collect-only` (3,073 = 1,369 smoke + 1,704 not-smoke):

| batch | result | wall |
| --- | --- | --- |
| `-m smoke` (1,369) | 1363 passed, 6 skipped | 23.3 s |
| `-m "not smoke"`, files 1–34 (858) | 856 passed, 2 skipped | 195.5 s |
| `-m "not smoke"`, files 35–69 (846) | 839 passed, 7 skipped | 398.3 s |
| the four split modules, driven together (133) | 132 passed, 1 skipped | 99.6 s |

`docs/stage` was regenerated twice in this sitting — the fingerprint hashes the
registry content, and both the slice-1 `Module` cells and this slice's
`Evidence` cells are in that basis.

### What remains on the row

Three of M-06's four monoliths (`test_trace.py` 2,099, `test_trajectory_arch.py`
1,993, `test_agent_loop.py` 1,640), the three other fusion heads, the rest of
`check_trajectory`, and the sensor gap. **The row stays ACTIVE** — it is the
standing debt owner and the module-size ratchet still points at it.
