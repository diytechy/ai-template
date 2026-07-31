## 2026-07-31 — WI-277 split the test monoliths by stable behavior boundary

Slices S6–S8 only: the three splits that are **independent of the anchor**.
`tests/test_gen_trajectory.py` (S1–S5) is deliberately NOT touched here — its
production module is being decomposed on another branch, and splitting the test
monolith before its seams settle would just move the churn.

Every move is a **verbatim cut-paste** (docstrings and comments included —
several encode owner rulings). No test body was edited, renamed, re-tiered or
re-ordered; the only edits are the new module docstrings, the per-module import
lines, and the helper copies. The suite idiom is preserved: **no test module
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
