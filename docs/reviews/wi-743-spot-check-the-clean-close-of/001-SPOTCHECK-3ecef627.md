# SPOTCHECK — WI-743 — the clean close of WI-740, judged at 3ecef627

This is a sampled spot check of a GREEN close (`docs/process.toml
[attestation] complete_review = "sample"`). It asks one question: does what
shipped answer what the row asked for? WI-740's Context had three numbered
items:

1. keep-warm pings only a route whose runner's adapter bounds a call to one
   turn, decided through `adapter_for`, with no runner-name list in
   `session_keep.py`, and every other behaviour of such a route left exactly
   as it is;
2. LLR-270's `detail` replacement, plus the new symbol in `code_symbol`;
3. TC-268's `method` insertion, plus the opencode and claude twin test.

The OUT OF SCOPE list came with them. The close stands whatever is found
here. A finding is a successor row, never a reversal.

What was read: the closed spec
`docs/archive/work/complete/WI-740-keep-warm-only-a-route-whose-r.md`, and its
queued form at `3ecef627^`. A script confirmed that the `## Context` sections
of the two are identical, so I checked against the same draft the builder had.
Also read:

- the squash `3ecef627`: `git show`, `--name-status`, and the diffs of both
  registries, the two scripts, the test file, `docs/stage`,
  `docs/ratify/CURRENT.md` and the coordinator log;
- the review `docs/reviews/2026-09-28-wave6/sonnet-wi740.md`;
- the rows LLR-270 and TC-268, before and after;
- in `session_adapters.py`: `PlainAdapter` (with `one_turn` and the new
  `bounds_one_turn`), `ClaudeAdapter.one_turn`, `_basename`, `_BY_PREFIX` and
  `adapter_for`;
- in `agent_session.py`: `build_argv`, `_validate_prompt_transport`,
  `_batch_prompt_error` and `_windows_batch_executable`;
- in `session_keep.py`: `KeepConfig`, `keepwarm_due`, `due_routes` and
  `take_warm_lease`;
- in `session_service.py`: `KeepWarmer` and `keep_warmer`;
- `dispatch.run`, where the warmer is built, and `_session_config_refusal`;
- the routes in `project-trajectory/agents.template.toml` and
  `docs/agents.toml`;
- the TC-268 section of `tests/test_session_keep.py`;
- the two sibling rows minted at `768b209d`, WI-741 (the LLR-270 amendment
  adjudication) and WI-742 (TC-268's first approval).

I checked each clause against the registries, the code, the tests or the
diff, not against the builder's or the reviewer's account. HEAD stayed at
768b209d throughout.

What was run, in this worktree unless a scratch directory is named:

- `python -m pytest -q -n 2 tests/test_session_keep.py tests/test_session_service.py tests/test_session_adapters.py -p no:cacheprovider`
  gave `106 passed in 25.07s`. The Deliverable's `111 passed` also counted the
  two ratchet modules, which the review's command line names.
- `python -m pytest -q -p no:cacheprovider -m smoke "tests/test_session_keep.py::test_keep_warm_pings_only_a_route_whose_adapter_bounds_one_turn"`
  gave `1 passed in 2.41s`. The twin test is in the smoke tier, which
  TC-268's `tier = "Smoke"` requires.
- A verbatim check. A script parsed both registries at `3ecef627^` and at
  `3ecef627` with `tomllib`. It confirmed that the draft's two before-strings
  and two after-strings appear backticked in the Context. It then checked
  that each anchor occurs exactly once in its parent cell, applied the edit,
  and compared the result with the squash. The results:
  - LLR-270 `detail`: the old clause occurs once, and applying the
    replacement gives the squash cell exactly.
  - TC-268 `method`: the anchor occurs once, and inserting the drafted text
    after it gives the squash cell exactly.
  - Across the whole LLR registry, only LLR-270's `detail` and `code_symbol`
    changed. Across the whole TC registry, only TC-268's `method` changed.
  - Of `code_symbol`'s five `;` groups, only the third (the
    `session_adapters` group) changed. It gained
    `PlainAdapter.bounds_one_turn`, after `ClaudeAdapter.one_turn`.
  - LLR-270 reads `Approved` both before and after. TC-268 reads `Drafted`
    both before and after.
- A counterfactual for the twin test. I exported `project-trajectory/`,
  `tests/`, `conftest.py` and `pytest.ini` from HEAD into a scratch directory
  outside the repository, and ran the twin test there: `1 passed`. I then put
  back the pre-fix `session_service.py` from `3ecef627^`: `1 failed`, at
  `assert opencode.thread is None`, because a `_ping` thread had started. The
  test fails without the fix.
- A classification probe over this repo's `docs/agents.toml` at HEAD.
  `KeepWarmer.routes` came out as exactly the four ANTHROPIC rows, all on
  claude. The OPENAI (codex) and OPENCODE rows are excluded.
  `bounds_one_turn()` is True for `ClaudeAdapter` and False for
  `CodexAdapter`, `OpencodeAdapter` and the plain adapter.
- A construction probe. On this Windows box, with the dial on
  (`KeepConfig(context_reset_pct=80, keepwarm_minutes=50)`), I called
  `keep_warmer` over a scratch root whose `docs/agents.toml` is the shipped
  `agents.template.toml`:
  - With a stub `gemini.cmd` on PATH, HEAD raised `ValueError: unsafe prompt
    delivery refused: '...gemini.cmd' is a Windows batch shim ...`. The
    pre-fix `session_service.py` built the warmer.
  - Without the shim, HEAD built it with `routes = ['ANTHROPIC-OPUS-4.8']`.

  A direct `KeepWarmer` construction over a `gemini.cmd -p {prompt}` row
  showed the same split: HEAD raised, and the pre-fix code built it. See
  Finding 1.

Every scratch file lived in the session scratchpad, outside the worktree, and
was deleted at the end. After that, `git status --short` shows only this
record.

## Per-item findings (WI-740 Context, items 1 to 3)

1. [MET, with Finding 1 as a side effect] The code.
   - "pings a retained session only on a route whose runner's adapter
     bounds a call to one turn". `KeepWarmer.__init__` builds `self.routes`
     once. It keeps each registry row whose
     `adapter_for(build_argv(row.cmd_template, ...)[0]).bounds_one_turn()` is
     true. `tick` passes that set to `take_warm_lease`. `build_argv` returns
     `(argv, stdin)`, so `[0]` is the argv list, which is what `adapter_for`
     takes.
   - "reads the route's adapter ... a runner gaining a one-turn bound later
     needs no second edit". `bounds_one_turn` is true when a subclass
     overrides `one_turn`, so a new override needs no second edit.
   - "Do not add a runner-name list to `session_keep.py`". `session_keep.py`
     is not in the squash at all.
   - "A route that fails the test is never pinged". `take_warm_lease` drops
     every route not in `routes` from `due` before it takes the lock, so that
     route gets no lock, no lease write and no `Keep`, and `_start` is never
     reached. The twin test and the counterfactual above show this.
   - "Leave its retention, resume, drain and retirement exactly as they
     are". `keep_for`, `keep_argv`, `drain_reason`, `is_clear_point`,
     `keep_bookkeep`, `keep_abandon` and the tombstone path are unchanged.
     The squash touches `session_service.py` only in `KeepWarmer.__init__`
     and in the `routes=` argument of `tick`.

     One edge, by reading: the keep-warm path's `retire_stale_lease` sits
     inside `take_warm_lease`, after the filter. So a non-bounding route's
     expired lease is no longer retired by a tick. It is retired at the next
     `keep_for` instead, before any reuse. That is how a route missing from
     the registry was already treated, and the session is still never
     reused. I read it as consistent with "never pinged", not as a change to
     the route's retirement.
   - "No shipped configuration changes behaviour" (the Deliverable). This
     holds for the ANTHROPIC routes, per the classification probe. It does
     not hold for construction. See Finding 1.
2. [MET] LLR-270. The `detail` replacement landed verbatim, and nothing else
   in the row moved except `code_symbol` (script above). The new symbol went
   into the `session_adapters` group, as the draft asked. It sits beside the
   other adapter methods rather than at the group's end. The draft said
   "append ... in the group", and the reviewer judged this placement to
   follow the repo's practice; I agree it is immaterial. The row stays
   Approved. WI-741, minted at `768b209d`, owns the §A5.2 amendment
   adjudication.
3. [MET] TC-268. The `method` insertion landed verbatim after the named
   anchor, and nothing else in the row moved. The anchor was present, so the
   draft's stop-and-report branch did not arise.
   `test_keep_warm_pings_only_a_route_whose_adapter_bounds_one_turn` sits
   under the file's `# --- keep-warm (TC-268)` banner, and does what the
   draft named:
   - the opencode half uses a retained ANTHROPIC session, idle past the
     minutes (`clock = 10**10`), on an `opencode run -m anthropic/model` row;
   - it asserts no returned line, no thread, no `lease` in the record and no
     launch;
   - the claude half pings the same session and asserts
     `--max-turns 1` in the argv.

   The row stays Drafted, and WI-742 owns its first approval.

## Scope held

- SR-227, SR-222 and TC-264 are untouched: the SR registry is not in the
  squash, and TC-264 is not among the changed TC paths. DA-016 and DA-017 are
  untouched: no decisions file is in the squash.
- No one-turn bound was added for opencode or codex. `CodexAdapter` and
  `OpencodeAdapter` still inherit `one_turn` unchanged.
- None of the four readings ruled as wording was touched: the conversation
  id, the lock-free whole write of the tombstone, the 0.5 s lock wait and
  prefix matching (`_basename`, `_BY_PREFIX` and `adapter_for` are
  unchanged).
- The other files in the squash are bookkeeping:
  - the generated `PROJECT_STATE.html`, `docs/open-items.html` and
    `docs/ratify/CURRENT.md`. The ratify brief restates the before and after
    cells of LLR-270 and TC-268;
  - `docs/stage`, where only the fingerprint and the as-of line move;
  - the closed spec's Deliverable;
  - the review;
  - the coordinator log.

## Findings

1. **FOLLOW-UP. The warmer's construction now builds every registry row's
   argv, so a row with a refused prompt transport stops the dispatcher at
   start.**

   `KeepWarmer.__init__` calls `agent_session.build_argv` on every row of
   `docs/agents.toml`, whatever its family and whether or not it is enabled.
   `build_argv` ends in `_validate_prompt_transport`. On Windows, that raises
   `ValueError` for a `{prompt}`-in-argv template whose executable is, or
   resolves on PATH to, a `.cmd` or `.bat` shim. `dispatch.run` calls
   `session_service.keep_warmer(...)` with no handler, just before its main
   loop.

   So with the `[adjudicator]` dial and `keepwarm_minutes` on, on Windows, a
   roster holding such a row now fails the whole run at start. The row need
   not be ANTHROPIC, or even routed. Before this squash the same row was
   refused only when a launch was made on it.

   The shipped template's `GOOGLE-GEMINI-3-PRO` row (`gemini -p {prompt}
   --output-format json`) is such a row wherever `gemini` is an npm shim. The
   construction probe above shows exactly this, and the pre-fix code builds
   the warmer. The template's own note on that row already says a shim is
   refused, but at launch, not at dispatcher start.

   The exposure is narrow. The dial ships off, and this repo's roster
   carries no `{prompt}`. Still, it is a behaviour change to a shipped
   configuration under a non-default dial, which the Deliverable's "No
   shipped configuration changes behaviour" does not cover. It is also more
   work than the decision needs: only `argv[0]` is read.

   A likely fix: take the executable the way `cli_version` in the same
   module already does, `agent_session.split_cmd(row.cmd_template)[:1]`,
   with no prompt substitution or transport check. Pin it with a test that
   builds a warmer over a batch-shim `{prompt}` row (the platform is
   injectable in `_windows_batch_executable`). This is a mechanical successor
   row, with no spine cell to change. To keep the queue small, WI-741 could
   draft it in its `## Dispositions`, since it already judges LLR-270's
   keep-warm clause at this merge.

## Observations

None of these is a gap in what the row asked for.

1. The reviewer's major, that the capability is inferred from the override
   rather than declared, is recorded and owned by WI-741's adjudication. I
   confirm its premise: all four shipped adapters classify correctly.
2. `tick`'s in-flight branch still calls `session_keep.due_routes` without
   the `routes` filter. So while a claude ping is in flight, a due
   non-bounding route can produce `keep-warm: skipped (a ping is in flight)`.
   Nothing is pinged. The line is only misleading, and a route missing from
   the registry already behaved this way before the squash. This rests on
   reading the code; I did not run it.
3. The commit bar's seconds read 72.4 s against the 60 s budget. The squash
   message says so and attributes it to contention. That is outside the one
   question here, and I did not re-measure it.

Three items were checked, and all were met: both registry edits are
verbatim, and nothing else moved in either registry. The twin test is in the
smoke tier and fails without the fix, and the three session modules ran 106
passed. The OUT OF SCOPE list held. What shipped answers the row. One side
effect of how the route set is built, a start-up failure under a non-default
dial on Windows, needs a small successor row.

VERDICT: FOLLOW-UP
