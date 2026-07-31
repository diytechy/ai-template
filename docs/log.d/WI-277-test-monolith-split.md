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
