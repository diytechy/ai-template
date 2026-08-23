## 2026-08-23 — WI-483 slice 5: the unattended loop's startup split, and `LoopContext` typed

**Summary.** Program shape item 5, the second of the three engines. `agent_loop.main`
— the entry point of the UNATTENDED operator — is decomposed OUTWARD into a
composer plus thirteen startup functions returning frozen records, and the
`LoopContext` attribute bag is split into a **frozen, total** config record plus
`LoopRun`, the explicit mutable half. Console, exit codes, prompts and resume
semantics are byte-identical across eighteen driven paths, proven by before/after
diff against HEAD's script rather than asserted.

Deferred open items: none — nothing here needed an owner ruling. No new module
ships (so no MAPPING/spine/RESYNC surface moved, and no `Approved` cell was
rewritten anywhere in the diff), and the one upward ratchet re-stamp is a
declaration bump with its reason in the baseline comment.

### Today's re-measurement, before designing anything

Slice 4's figures re-taken on this tree at `d6818b0b` — all three engines and
the bag are exactly where slice 4 left them, none had drifted:

| target | slice 4 recorded | today, before | after |
| --- | --- | --- | --- |
| `agent_loop.main` | 402 lines / C901 27 | **402 / 27** | **152 / under 10 (off the census)** |
| `agent_loop.session_bookkeeping` | 325 / 31 | **325 / 31** | untouched |
| `agent_loop.run_iteration` | 326 / 20 | **326 / 20** | untouched |
| `agent_loop.py` | — | **3,240 lines** | **3,455** |
| `tests/test_agent_loop.py` | 1,567 (review) | **1,640** | untouched |

fig: `wc -l` + `python -m ruff check --select C901 --config
"lint.mccabe.max-complexity=10"` over `project-trajectory/scripts/agent_loop.py`,
at `d6818b0b`.

### The boundary, in one sentence

**Everything that RESOLVES what this run is — the effective root, the five phase
maps, the enable-list, the declared dials, the reviewer/knob integers — is a
pure function returning a typed record; `main` keeps the EFFECTS (console,
coordinator lock, subprocess, banner) and the mode decisions between them.**

So, out of `main` and up to module level:

- **Resolution** — `_resolve_root`, `_parse_session_maps`, `resolve_routing_setup`
  (`RoutingSetup`), `resolve_session_setup` (`SessionSetup`, which also owns the
  three refusals: a malformed map, a failed preflight, an illegal worker
  assignment), `resolve_session_policies` (`SessionPolicies`),
  `possible_session_models`, `_clamped_review_rounds`, `_int_env`,
  `build_routing_state`, `_live_console`, `is_drive_launch`.
- **Effects with a decision in them** — `warn_on_inert_or_malformed_policies`
  (the three consent-surface warnings, in their original order),
  `announce_critique_budget`, `_dual_plan_entry` (the whole early path: one
  round, then exit), `run_loop` (the iteration budget and its exhaustion banner).

What is LEFT in `main` is the sequence a reader needs to see in one place: parse,
resolve, refuse-or-continue, take the lock, pick the mode, build the context, run.

**Decomposition is OUTWARD, and the recorded trap still applies** — ruff's C901
charges a nested def to its enclosing function, so every extraction here is a
module-level def and `test_main_stays_a_composer` asserts `main` nests none.

### The bags, typed

`LoopContext` is a **frozen** dataclass, 29 declared fields, constructed at
exactly one site — the tail of `main`, as a single expression. It was an EMPTY
class populated by 32 attribute assignments, and declaring it made three things
visible that the bag had hidden:

1. Nothing in the loop ever re-resolves a dial mid-run. `frozen=True` now says so.
2. `session_hold` was carried on the bag for **no reader at all** — dropped
   (`main` still builds the label for the banner and the dual-plan message).
3. `human_held` and `keep_nondependent` were read out of the bag as
   `getattr(ctx, "human_held", True)` / `getattr(ctx, "keep_nondependent", False)`.
   A field the constructor forgot would have become "human-held, don't keep
   going" **silently**. This one bit during the slice — a first cut dropped both
   fields on the strength of an attribute grep, and
   `test_per_wi_exhaustion_disposition_overrides_autonomous[move-on-6]` caught it
   at once, which is the defensive read's whole cost stated as a test failure.
   A total record cannot be missing a field, so both reads are now direct, and
   `test_no_defensive_getattr_reads_survive_on_the_context` (an AST check, not a
   substring one) keeps them that way.

`LoopRun` is the mutable half: `routing` (the `RoutingState` cluster, which
mutates across iterations by design), `state`, and `warned_no_core`. Three
fields, so "what a session may write" is a declaration rather than a convention.
`run_iteration` writes `ctx.run.state`; nothing else in the loop writes anything.

### Behaviour preserved byte-identically, and measured that way

A temporary capture harness (built on `tests/test_agent_loop.py`'s
`FAKE_AGENT`/`loop_repo` idiom, run against HEAD's `agent_loop.py` and then
against the slice's, deleted before commit) drove **18 paths** and diffed the
normalized stdout + stderr + exit code + the last session PROMPT of each: DONE,
BLOCKED, noop-to-budget, error-stall, missing `--worktree`, malformed
`--model-map`, malformed `--cmd-map`, unknown `--dual-plan`, non-dual
`--dual-plan`, malformed blackout + reviewer dial together, interactive, empty
`AGENT_CMD`, junk `AGENT_COOLDOWN_SECONDS`/`AGENT_CRITIQUE_MAX`, managed-routing
DONE, managed guardrails-inert, unresolvable enable-list token, malformed
draw-weight annotation, and `--help`. **Empty diff**, six distinct exit codes
covered (0/2/3/4/6 and the preflight refusals).

fig: the harness ran twice over the same fixture, once with
`git show HEAD:project-trajectory/scripts/agent_loop.py` in place; `diff -u`
between the two capture files was empty.

**Covered vs reasoned, honestly.** Test-covered end to end: everything above,
plus the six `test_agent_loop*` modules (166 passed, 1 skipped) which drive the
loop, the critique rounds, managed routing and the worker end-state through the
fake agent. **Reasoned, not driven:** the paths that need a live agent CLI or a
real clock — a genuine rate-limit reset sleep, a TTY with VT enabled (so
`_live_console`'s `and` chain is only ever exercised returning False here), a
real blackout wait, and the drive mode's `dispatch.run`. For those the argument
is textual: `_live_console` and `_int_env` are pure lifts of the expressions they
replace, and `is_drive_launch` short-circuits in the same order as the `if not
(...)` it came from.

### Ratchets: one entry DELETED, one declaration bump

- **Complexity:** `("agent_loop.py", "main"): 27` **DELETED** — under the limit.
  The comment that bumped it for the M-20 malformed-policy warnings is retired
  with it; those warnings now live in `warn_on_inert_or_malformed_policies`,
  unchanged.
- **Module size:** `agent_loop.py` 3,240 → **3,455**, a reviewed **+215**
  declaration bump. `main` itself shed 250 lines; what replaced it is 54 bare
  field declarations across five records plus thirteen defs carrying the comments
  that used to sit inline. This is precisely the `bootstrap.py` shape the size
  ratchet's own header records as the owner's `OI-16` counterexample — the file
  grew while the module got structurally simpler, and the axis the program pays
  down (complexity) went down by a whole entry.

### M-06 rides nothing here

`tests/test_agent_loop.py` (1,640 lines) is untouched: this split needed no
monolith split, and a standalone one is out of scope. The eight new boundary
tests went to `tests/test_agent_loop_policy.py` (482 → 617), which the WI-277
split already made the home of "the ungated Slice D/E `main()` seams" — the right
existing module, not a new one. They guard the BOUNDARY rather than re-asserting
rules already covered through the engine: the S8 knob idiom surviving extraction,
the lenient reviewer-dial parse, the drive-launch predicate, the managed
inert-check model set, `LoopContext` frozen + total (no field carries a default,
so a forgotten one is a `TypeError` at the one construction site), `LoopRun`'s
per-instance list default, the no-`getattr(ctx, …)` rule, and that `main` stays a
composer (< 200 lines, no nested def).

### Deviations from the slice brief

- **`session_bookkeeping` and `run_iteration` NOT taken.** The brief allowed them
  only if the main/bag split left them trivially better homes, and it did not:
  both are per-session consequence ladders whose branches are genuinely about
  routing state, not about configuration. They gained exactly two lines each from
  this slice (`ctx.run.routing` / `ctx.run.state` in place of `ctx.st` /
  `ctx.state`). They remain item 3's honest remainder.
- **One non-obvious mechanical constraint recorded at the call site:**
  `LoopRun.routing` carries an UNQUOTED annotation. A string annotation sends
  `dataclasses`' `KW_ONLY` probe through `sys.modules`, which the suite's
  `load_script` import does not populate — it fails collection for every module
  that loads `agent_loop`, and the comment above the field says so.

### What remains of item 3, and of the row

`agent_loop.session_bookkeeping` (325 / 31 — now the kit's most complex single
function) and `run_iteration` (326 / 20) are the remainder of this engine, and
`check.steps` still needs a DECISION rather than a technique: 628 lines of flat
step declaration, under the complexity limit, so its split is a question about
the carrier for a declaration and may reasonably end in "leave it". Items 1 (the
`integrate -> intake` layering) and 4 (M-06) are unchanged.

### Gates

```
python -m pytest -q -n auto            -> 2968 passed, 14 skipped in 982.93s
python -m pytest -q -n auto -m smoke   -> 1301 passed, 5 skipped in 38.97s
python scripts/check_smoke_budget.py --mode enforce
                                       -> 19.0s vs 60s budget -> within
python project-trajectory/scripts/check_docs.py --root . --stale
                                       -> OK, 1040 docs, 0 broken
python project-trajectory/scripts/check_trajectory.py --root . --strict
                                       -> clean (507 WIs, graph acyclic)
python project-trajectory/scripts/gen_trajectory.py --root . --check
                                       -> dashboard up to date
```

**A FIRST full run failed one test and it is worth recording, because it was a
rule the split had no business breaking.** `test_gate_policy.py`'s WI-437 /
OI-25 guard reads this module's SOURCE for the exact spelling
`session_hold = "human-held" if human_held else "loop-held"`, and folding that
ternary into a dataclass keyword argument made the derived hold unfindable to
the one check that keeps the name meaning one thing. Fixed in the code, not in
the guard: the value is computed as its own statement inside
`resolve_session_policies` and passed by name, with the reason at the site. (The
same guard forbids the retired enum's name appearing in the module at all, which
is why the comment there does not spell the test module either.) The second full
run — the totals above — is green.

**One honesty note on the capture.** The 18-path diff was measured on the tree as
of the `getattr` fix. The two edits after it are this comment block's cause — a
hoisted local passed to the same keyword — and comment text; the six
`test_agent_loop*` modules (174 passed, 1 skipped) were re-run after them.
