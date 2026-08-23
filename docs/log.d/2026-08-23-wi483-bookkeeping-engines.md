## 2026-08-23 — WI-483 slice 6: the loop's two consequence ladders, and one page rule instead of two

**Summary.** Program shape item 5, finishing the `agent_loop.py` engine slice 5
left half-done. `session_bookkeeping` (325 lines / C901 **31**, the kit's most
complex surviving function) and `run_iteration` (326 / 20) are decomposed
OUTWARD into twenty module-level functions plus three frozen decision records;
both are OFF the complexity census and both baseline entries are DELETED. The
two S8 page-the-human ladders that had been written twice — a review escalation
and an exhausted critique budget — collapse to ONE rule. Console, exit codes and
telemetry are byte-identical across **31 driven paths**, proven by a
twice-run capture diff against HEAD's script rather than asserted.

Deferred open items: none — nothing here needed an owner ruling. No new module
ships (so no MAPPING/spine/RESYNC surface moved, no seam changed, and no
`Approved` cell was rewritten anywhere in the diff), and the one upward ratchet
re-stamp is a declaration bump with its reason in the baseline comment.

### Today's re-measurement, before designing anything

Slice 5's figures re-taken on this tree at `fce44490`. Nothing had drifted; the
pair is exactly where slice 5 left it.

| target | slice 5 recorded | today, before | after |
| --- | --- | --- | --- |
| `agent_loop.session_bookkeeping` | 325 lines / C901 31 | **325 / 31** | **28 / under 10 (off the census)** |
| `agent_loop.run_iteration` | 326 / 20 | **326 / 20** | **120 / under 10 (off the census)** |
| `agent_loop.main` | 152 / under 10 | **154 / under 10** | untouched |
| `agent_loop.py` | 3,455 | **3,462 lines** | **3,614** |
| `tests/test_agent_loop.py` | 1,640 | **1,640** | untouched |

fig: `wc -l` + `python -m ruff check --select C901 --config
"lint.mccabe.max-complexity=10"` over `project-trajectory/scripts/agent_loop.py`,
at `fce44490`. (`main`'s 154 vs slice 5's recorded 152 is `inspect.getsourcelines`
counting the two lines slice 5's own final comment edit added, not drift.)

After this slice the module's whole complexity census is `critique_brief` 11,
`route_intent` 12 and `map_preflight` 19 — three small entries where there were
five, and the two largest are gone.

### The boundary, in one sentence

**What a session's outcome MEANS — which consequence arm applies, whether a page
stops the run, what a reset hint buys, how two verdicts compare — is a named
function over routing state, several of them returning frozen records; the arms
keep the EFFECTS (console, `RoutingState` mutation, telemetry commits, stop
banners, the subprocess) and apply what the decision returned.**

So, out of the two ladders and up to module level:

- **`session_bookkeeping` -> the four arms and their decisions** —
  `reroute_rate_limited`, `review_bookkeeping` (`absorb_review_verdict`,
  `complete_review_round`, `round_substance`, `impl_changed_paths`,
  `apply_rework_scope`), `critique_bookkeeping` (`critique_budget_page`),
  `build_bookkeeping` (`report_cooled_model`, `schedule_review_round`,
  `schedule_critique_round`), and the shared `page_consequence` /
  `apply_page_consequence`.
- **`run_iteration` -> the session's own stages** — `wait_out_blackout`,
  `current_assignment_wi`, `launch_session`, `write_raw_stream`, `session_meta`,
  and `after_session` (with `rate_limit_wait` and `stall_stop` under it).

What is LEFT in each is the ladder itself. `session_bookkeeping` is 28 lines
naming which consequence applies before a reader reads what it does;
`run_iteration` is 120 lines of the sequence one session takes — guard, claim,
route, launch, record, bookkeep, and what the outcome means.

**Decomposition is OUTWARD, and the recorded trap still applies** — ruff's C901
charges a nested def to its enclosing function, so every extraction here is a
module-level def and a parametrized `test_the_session_ladders_stay_composers`
asserts neither ladder nests one.

### The duplication the split exposed: two page ladders, one rule

Both S8 page paths had been written out in full, seven lines apart in style and
about thirty apart in the file:

```
fa = agent_route.failure_action(human_held, keep_going)
print(<its own message>)
if fa["mode"] == "human-held" and not fa["keep_nondependent"] [or block]:
    stop_banner(...); return EXIT_NEEDS_HUMAN
if fa.get("design_check"):
    st.set_design_check()
```

That is one rule with one declared asymmetry (the critique arm's
`exhaustion = block` stops whatever the hold says), so it is now
`page_consequence(fa, force_block=False) -> PageConsequence(stop, design_check)`
— pure — plus `apply_page_consequence`, the banner/exit/re-arm effect. Writing
it once made an implicit ordering explicit: the original never reached the
design-check arm on a stopping path because it had already returned, and
`design_check` is now `(not stop) and …` as a FIELD, with a test that pins it.
This is PROCESS.md §3's "consolidate, don't duplicate" applied to the thing the
decomposition uncovered, not a second scope.

### The typed records

Three, each because a caller had been keeping several locals in step by hand:

- **`PageConsequence(stop, design_check)`** — above.
- **`RoundSubstance(family_substance, margin, primary)`** — `margin` and
  `primary` are only meaningful ACROSS a pair, and were three locals computed in
  one loop and then read four lines apart. `primary` is annotated `object`, not
  a lying `str`: it is None for a solo round, this module carries no `typing`
  import, and slice 5's recorded trap forbids a STRING annotation (it sends
  `dataclasses`' `KW_ONLY` probe through `sys.modules`, which the suite's
  `load_script` import does not populate).
- **`LimitWait(nap, seconds, message)`** — the rate-limit arithmetic, lifted out
  of `run_iteration` whole. `nap` is an explicit discriminator rather than
  `seconds is not None`, because a zero-second wait is still a wait; a test pins
  that.

**One thing deliberately NOT made a record.** The session telemetry projection
stayed a dict (`session_meta`): it IS `write_session_log`'s column set, so a
typed record would only be splatted straight back into one. Its key ORDER is
pinned by a test instead, which is the property that could silently break.

### Behaviour preserved byte-identically, and measured that way

A temporary capture harness (built on the `loop_repo` / `managed_repo` /
`critique_repo` fixtures the suite already has, run against HEAD's
`agent_loop.py` and then against the slice's, deleted before commit) drove **31
paths** and diffed the normalized stdout + stderr + exit code of each:

- **legacy (16)** — DONE, BLOCKED, noop-to-budget, error-stall, mixed stall,
  commit-then-done, rate-limit WAITING and the unrecognized-reset WAITING,
  session timeout, an inactive blackout declaration, plain-text error stall,
  stream-json result, missing `--worktree`, malformed `--model-map`,
  interactive, `--help`.
- **managed review (10)** — policy 1 / 2 / 0, CHANGES-REQUESTED rework, an
  unparseable verdict, a reviewer that writes none, a managed ERROR cool, a
  managed rate-limit re-route, a strong-tier build, and the full escalation
  ladder to **page-human** (continue -> swap-implementer -> tier-up ->
  page-human, with the stop banner).
- **critique (5)** — APPROVE, the budget exhausted under `move-on` and under
  `block`, an unparseable verdict, and an unbounded `inf` budget.

**Empty diff**, seven distinct exit codes covered (0/2/3/4/5/6/7).

fig: `capture483f.py` ran twice over the same fixtures, once with `git show
HEAD:project-trajectory/scripts/agent_loop.py` in place; `diff -u` between the
two capture files was empty. The harness was first run twice against HEAD alone
and self-diffed empty, so the comparison rests on a determinism check rather
than on hope.

**Covered vs reasoned, honestly.** Test-covered end to end: everything above,
plus the seven `test_agent_loop*` modules (197 passed, 1 skipped) which drive the
loop, the review rounds, the critique loop, managed routing and the worker
end-state through fake agents. **Reasoned, not driven:** the paths needing a real
clock or a live CLI — an actual rate-limit reset sleep inside the ceiling (the
nap ARITHMETIC is driven directly in `test_rate_limit_wait_naps_only_within_the_
consented_ceiling`, the `time.sleep` is not), a real blackout wait, a live
`LiveStatus` console (`launch_session`'s `live is not None` arms only ever run
False here), and the `design_check` re-arm, which no shipped `failure_action`
mode returns today — its rule is driven directly against a synthetic `fa` dict
instead. For those the argument is textual: each is a pure lift of the
expression it replaces, in the same order.

**One honesty note on the capture.** The 31-path diff was measured on the tree
as of the `report_cooled_model` rename. The one edit after it re-points a
comment's "below" at `complete_review_round`, the function the review
scoreboard's commit moved into — comment text only, no executable change.

### Ratchets: two entries DELETED, one declaration bump

- **Complexity:** `("agent_loop.py", "run_iteration"): 20` and
  `("agent_loop.py", "session_bookkeeping"): 31` **both DELETED** — under the
  limit. The 2026-07-21 review bump the pair carried (H-1's unparseable-verdict
  fail-closed branches) is unchanged behaviour, now living in
  `absorb_review_verdict` and `critique_bookkeeping`; the baseline comment says
  so, since the entry that recorded it is gone.
- **Module size:** `agent_loop.py` 3,462 -> **3,614**, a reviewed **+152**
  declaration bump — the same `bootstrap.py` shape the size ratchet's own header
  records as the owner's `OI-16` counterexample, and smaller than slice 5's +222
  on the same module. The two functions shed 651 -> 148 lines between them;
  what replaced them is twenty signatures plus the docstrings that used to be
  inline comment blocks. The axis this program pays down went down by two whole
  entries.

### M-06 rides nothing here

`tests/test_agent_loop.py` (1,640 lines) is untouched: this split needed no
monolith split, and a standalone one is out of scope. The nine new boundary
tests (ten cases) went to `tests/test_agent_loop_policy.py` (617 -> 798), already the home of
"the ungated Slice D/E `main()` seams" and now of slice 5's record tests — the
right existing module, not a new one. They guard the BOUNDARY: the one page
rule and its two callers' asymmetry, that a stopping page never also re-arms the
design check, the rate-limit ceiling arithmetic, `LimitWait`'s explicit
discriminator, `impl_changed_paths`' own-bookkeeping exclusion (both slash
flavours), `RoundSubstance` frozen with no winner in a solo round, the log's
column ORDER, and that both ladders stay composers with no nested def.

### Deviations from the slice brief

- **Both functions taken, not one.** The brief allowed the second only if it
  fell cleanly out of the first's design, and it did: they share the
  routing-state vocabulary, `after_session` is the natural other end of
  `session_bookkeeping`'s return contract, and the WAITING outcome is handled
  across both (a managed re-route in one, the nap-or-stop in the other) — so
  splitting them across two slices would have drawn the boundary through the
  middle of one decision.
- **`build_bookkeeping` takes `now` as an explicit parameter** rather than
  reading it off the context: the cool timestamp is the SESSION's clock reading,
  taken once in `run_iteration` before the launch and threaded through, and
  hiding it on the frozen context would have made a per-session value look
  resolved-once.

### What remains of item 3, and of the row

**Item 3 is struck for the whole `agent_loop.py` engine.** What remains of it is
`check.steps` alone — 628 lines of flat step declaration, UNDER the complexity
limit — and it still needs a DECISION rather than a technique: its split is a
question about the carrier for a declaration and may reasonably end in "leave
it". That is an owner-ish call about `check.py`'s shape, deliberately not taken
here. Items 1 (the `integrate -> intake` layering, which needs its own decision
about what `integrate.py merge` does on its own) and 4 (M-06's monolith splits)
are unchanged.

### Gates

```
python -m pytest -q -n auto            -> 2977 passed, 14 skipped in 1142.66s
python -m pytest -q -n auto -m smoke   -> 1301 passed, 5 skipped in 49.55s
python scripts/check_smoke_budget.py --mode enforce
                                       -> 22.2s vs 60s budget -> within
python project-trajectory/scripts/check_docs.py --root . --stale
                                       -> OK, 1041 docs, 0 broken
python project-trajectory/scripts/check_trajectory.py --root . --strict
                                       -> clean (507 WIs, graph acyclic)
python project-trajectory/scripts/gen_trajectory.py --root . --check
                                       -> dashboard up to date
python project-trajectory/scripts/gen_open_items.py --root . --check
                                       -> open-items view up to date
```

The full run is green FIRST TIME, unlike slice 5's — its recorded failure was
the WI-437/OI-25 source-grep guard in `tests/test_gate_policy.py`, and this
slice grepped that guard's two pinned literals (`session_hold = "human-held" if
human_held else "loop-held"` and the `session-hold:` banner label) before moving
a line. Both live in `resolve_session_policies` and `print_run_banner`, neither
of which this slice touches.
