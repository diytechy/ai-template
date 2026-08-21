# The gate compute-vs-read schedule map — when is `docs/gate` computed, and are its readers scheduled properly?

**Status:** verified analysis only. This document REPAIRS NOTHING and recommends
nothing. It answers one owner question and stops there.

> **The owner's question, verbatim:** "How / when is gate getting computed then?
> If multiple other functions are reading it, the question in my mind is when is
> the gate computed vs are other functions reading it and are they scheduled
> properly."

**Foundation, not redone here:**
[`docs/plans/2026-08-21-bar-vs-stage-census.md`](2026-08-21-bar-vs-stage-census.md)
and [`docs/plans/2026-08-21-stage-rekey-deep-check.md`](2026-08-21-stage-rekey-deep-check.md).
The deep-check's Q3 enumerated the readers and found `intake._gate_moved` broken;
this document takes that list as given and adds the **schedule** — when each
write happens, when each read happens, and which writes each read can see.

**As of:** branch `requirements/ears-and-quality-characteristics`, HEAD
`037b3e3f`, 2026-08-21. Nothing in the tree was modified; nothing was committed.
Every mutation below happened inside a scratch COPY inside the session
scratchpad.

**Method.** Every claim is a direct read at the cited `file:line` or a DRIVEN
result. Driven blocks are labelled **D1**–**D6** and their output is reproduced
verbatim.

---

# 1. The contract, in one paragraph

`docs/gate` is a **committed cache of a pure function of the working-tree
registries**. The function is `derive_gate.compute(docs)`
(`derive_gate.py:1449`), which reads `docs/requirements/*.toml` and
`docs/test/test-cases.toml` off the filesystem and returns both axes — the
runnable **bar** on the last line and the **stage** (plus counts and per-phase
bars) inside the `# basis:` comment. Exactly one function writes the file
(`derive_gate.py:1523`, reached only on the bare, no-flag path), and in
production it is invoked from exactly one place: `trunk_step.py:438`'s
`derived-gate` regen step. Freshness is enforced by `derive_gate.py --check`
(`derive_gate.py:1471–1516`), wired as check.py's `derived-gate` step
(`check.py:645–651`) at **all three bars**, which recomputes from the **live
registries** and byte-compares the whole `# basis:` line plus the value,
excluding only the volatile `# computed …(as-of …)` stamp. Every reader reads
the cached file, never the function. So the intended contract is: *writers
regenerate, no commit may land with the cache stale, therefore every reader is
fresh as of the last commit.* **That contract holds on the trunk and is
switched off, by design, on a claimed work branch** — `derived-gate` is a member
of `_TRUNK_FRESHNESS_STEPS` (`check.py:1550–1552`) and reports SKIP whenever
`docs/work/active/<branch>/` exists (`check.py:1816–1833`). That single fact is
the source of the largest real stale window below.

---

# 2. WRITES — every path that writes `docs/gate`

`derive_gate.py:1523` is the only line in the kit that writes the file's derived
content. `render_cache` (`derive_gate.py:1390`) is called only from it. The
three output modes return before it: `--next-phase` at `:1463`, `--print` at
`:1468`, `--check` at `:1516`.

| # | Writer | file:line | WHEN it runs in the real workflow | Tree state it reads |
|---|---|---|---|---|
| W1 | `trunk_step.py` `REGEN_STEPS` → `derive_gate.py --root .` | `trunk_step.py:436–440`; dispatch `:481` | **The only automated production writer.** Runs on the **trunk lane** only: at intake mint bookkeeping (`intake.py:1270–1283`), at the integrate **claim** commit (`integrate.py:770–779`, `--regen`), and in the lane **refresh** sequence (`integrate.py:1436` `_run_trunk_step`, called from `:2097`, no flags ⇒ compile + regen) | **Working tree** of the root it is given |
| W2 | Manual `python scripts/derive_gate.py` | documented at `skills/gate-advance/SKILL.md:68` ("Regenerate after a ratification"), `ADOPTING.md:198`, `PROCESS.md:945`, `RESYNC_PACK.md:499`/`:649`/`:1069` | **Per ratification, by a human or agent who remembers.** This is the path a mid-session approval actually takes — see §6 | Working tree |
| W3 | `bootstrap.py` template copy | `bootstrap.py:1555` — `("gate.template", "docs/gate")` | **Once, at scaffold.** Copies `project-trajectory/gate.template`, a single bare line `DevStg-Reqs` with **no `# basis:` line** | n/a (static copy) |
| W4 | Test fixtures | `tests/conftest.py:1038`, `tests/test_derive_gate.py:310`/`:325`/`:384`/`:827`, `tests/test_product_floor.py:284`, `tests/test_generated_newlines.py:334` | Per test | Scaffold tmp trees |

**Three facts about the write side that bear on the owner's question.**

1. **Nothing in the commit path writes the gate.** The pre-commit hook, `check.py`
   and CI only *verify*. The asymmetry is stated at `check.py:1543`. So a spine
   edit never self-heals the cache; a writer must be invoked.
2. **`bootstrap.py` never runs `derive_gate.py`** — no subprocess spawn of it
   exists in that file. A freshly scaffolded repo therefore ships a
   **basis-less, legacy-form** gate, which `--check` passes value-only via
   `derive_gate.py:1486–1495`. Consequence for the stage axis: a fresh scaffold
   has **no `stage=` field at all**, so `spine_stage_of` returns `None`, which
   `human_holds` treats as human-held — fail-safe, in the more-human direction.
3. **`trunk_step`'s regen step is guarded by `_has("docs/gate")`**
   (`trunk_step.py:437`, `.exists()`). If the file is deleted, the only
   automated writer silently no-ops; nothing but `bootstrap.py:1555` or a manual
   run ever creates it.

---

# 3. FRESHNESS ENFORCEMENT — where `--check` is wired

| # | Enforcement point | file:line | What it compares | Against WHICH tree | On mismatch |
|---|---|---|---|---|---|
| E1 | check.py step `derived-gate` | `check.py:645–651` — `[sys.executable, _SCRIPTS/"derive_gate.py", "--check"]`, tags `{BAR_REQS, BAR_TESTS, BAR_RELEASE}`, layer `process` | **Recomputes from the live registries** and compares (a) the value line and (b) the whole `# basis:` line. The `# computed … (as-of …)` stamp is deliberately excluded — it is emitted at `derive_gate.py:1395` and never read by `parse_cache` (`:1400–1411`) | **Working tree.** `compute()` loads the registries off the filesystem; the cache is read from `root/GATE_FILE` on disk. No index or HEAD read | **FAIL** → exit 1 |
| E2 | pre-commit hook | `hooks/pre-commit:269` → `check.py --run-steps …,derived-gate,…`; meta-repo wrapper `.githooks/pre-commit:23` | via E1 | **WORKING TREE** — stated by the hook itself at `:246–252` ("*every step above reads the WORKING TREE*") and `:264–266` | **Blocks the commit** (`set -e`, `:20`; the line is not `\|\| true`-guarded) |
| E3 | `staged-divergence` | `check.py:962–968`; `docs/gate` is a declared `[generated]` row at `docs/stack.ini:581` | Worktree **vs the git INDEX** — which generated artifact is modified on disk but not `git add`ed. **Not** a regeneration | Index | **WARN-ONLY**, never blocks (`check.py:951–955`; OI-31 ruled option (b)). Explicitly does **not** catch an artifact *staged while stale* (`hooks/pre-commit:255–258`) |
| E4 | Kit CI | `.github/workflows/test.yml:163` — `check.py --jobs 0`, no `--gate` | via E1 | The **CI checkout** = the committed tree | Red build |
| E5 | Adopter CI (shipped) | `ci/check.yml:80` (`--tier smoke`), `:84` (`--tier full`), `:89` (`--gate all --tier release`) | via E1; `derived-gate` is tagged at all three bars so every invocation includes it | CI checkout | Red build |
| **E0** | **THE STAND-DOWN** | `check.py:1550–1552` `_TRUNK_FRESHNESS_STEPS`, applied by `_work_branch_skip` (`:1816–1833`) at `:1945`/`:1965` | — | — | **`derived-gate` reports SKIP on any claimed work branch, and "a skipped step never affects the exit code" (`check.py:1822–1823`)** |

**E1 recomputes from the LIVE registries, not from a cached input — verified, D2.**
This is the half of the owner's sub-question that comes out clean: the guard
cannot be fooled by a spine TOML edit, because it re-runs the whole derivation
over the edited files.

---

# 4. READS — the reader table, with P / W / X

Classification: **P** = protected (always runs after a freshness-enforced point,
cannot see a stale value); **W** = windowed (a real interval exists where it
reads a value stale relative to the live spine); **X** = broken.

Every reader below reads the file **fresh per call** — none memoizes the file
contents. Where a value is nonetheless reused, it is the *caller* that reads once
and threads the result down; that is called out explicitly.

## 4.1 Readers of the VALUE line (the bar)

| Id | Reader | file:line | WHEN it executes | Which write it last saw | Class |
|---|---|---|---|---|---|
| A | `check.resolve_gate` | `check.py:1472–1500`; reads module-level `GATE_FILE` (`:1055`) | **Per `check.py` run**, at plan-selection time — i.e. *before* the `derived-gate` step in the same run executes | The last committed/manual write | **W** — self-correcting on trunk (see below), **unprotected on a work branch** |
| B | `derive_gate.parse_cache` | `derive_gate.py:1400–1411` | Per `--check` run | — | **P** — it *is* the enforcer |
| C | `traj_parse._gate_value` | `traj_parse.py:450–462` | Dashboard regen (`gen_trajectory.py`), i.e. `trunk_step` regen or manual | The cache as it stands at regen | **W** (display) |
| D | `intake._gate_moved` → `tier_signal` | `intake.py:480–487`, `:242` | **Merge/integrate time**, inside the held merge slot right after the merge lands (`integrate.py:2353–2362`), plus manual `intake.py sweep`. Reads **two git revisions via `git show`** (`:485`), not the worktree — so it is immune to a stale working-tree file but blind to uncommitted gate edits | **None — it never sees any write** | **X — BROKEN** |
| E | `agent_common.read_declared` | `agent_common.py:139` → `kitlib/config.py:67–80` | **Never invoked on `docs/gate` at all** — see the correction below | — | **DEAD (not a reader)** |
| — | CI / hook | `ci/check.yml:80`,`:84`; `test.yml:163`; `hooks/pre-commit:269` | pass **no `--gate`**; the hook's `_step_gate` (`check.py:1503–1509`) forces `"all"` | — | **P** for the hook (always `all`) |

> **CORRECTION to the deep-check's Q3 reader table — reader E is not a live
> reader.** `read_declared` is a generic declared-policy reader whose call sites
> go through `declared_policy` (`agent_common.py:431`), keyed by `PROCESS_KEYS`;
> `docs/gate` is listed there as a deliberate **non-row**, with the reason given
> in the source at `agent_common.py:149–151` — *"NOT here, deliberately …
> `docs/gate` (a generated cache)"*. The docstrings at `agent_common.py:130–138`
> and `kitlib/config.py:70–72` still describe it as "the reader for `docs/gate`",
> but that is stale prose: every live gate reader (A, B, C, H, I) spells the
> one-line parse out locally under the F5 rule. The function *works* if called on
> the file — D4 below calls it directly and it returns the right value — but **no
> production call site does.** One fewer reader to schedule, and one more
> docstring describing a mechanism that is not there.

**Why A is "self-correcting on trunk."** `resolve_gate` chooses the step plan
from the cached value *before* `derived-gate` runs. So a stale cache really does
select the wrong plan for that run — but the `derived-gate` step then FAILs and
the whole run exits 1. **No green check.py run is possible over a stale gate on
the trunk.** The decision is made inside the window but is never *acted on
green*, which is the difference between a defect and a design. On a claimed work
branch E0 removes the failure, and a green run over a stale gate becomes
reachable — that is W-1 below.

`resolve_gate`'s own docstring asserts the contract: *"the `derived-gate` step
guards the cache against drift, so a --gate resolved here is a fresh computed
value"* (`check.py:1480–1481`). True on the trunk; false on a claimed branch.

## 4.2 Readers of the `# basis:` COMMENT

| Id | Reader | file:line | WHEN it executes | Class |
|---|---|---|---|---|
| F | `agent_common.spine_stage_of` — regex-scrapes `stage=` | `agent_common.py:760–784`, regex at `:783` | **Session start.** Exactly three callers: `agent_loop.py:2952` (main's preamble, before the tick loop at `:3223–3226`), `dispatch.py:1290` (before the `while True:` at `:1297`), `intake.py:1443` (manual `intake.py adjudicate`, one-shot). **The first two are long-lived and read it ONCE** — see W-2 | **W — the sharpest** |
| G | `check.window_open` / `check.product_floor` | defs at `check.py:1139` / `check.py:1233`; reads at `:1204–1206` / `:1289–1291` | **Full `check.py` runs ONLY** — merge bar (`integrate.py:1410–1414`), CI, manual. **Structurally unreachable from the pre-commit hook**: `--run-steps` exits at `check.py:2264`, before `resolve_plan` at `:2266` | **W** (same self-correction as A) |
| H | `check_trajectory.read_derived_phases` | `check_trajectory.py:1814–1839`, path read at `:1825` | Per full `check_trajectory` run, reached via check.py's `trajectory` step (`check.py:766–772`, DevStg-Tests+) — **not** via the hook's `--staged` pass, which returns early at `check_trajectory.py:4181` | **W** |
| I | `traj_status._gate_facts` → `_stage_line` | read at `traj_status.py:82–107` (`:93`); `_stage_line` at `:371` takes the parsed values | `docs/status.md` regen (`gen_trajectory.py --status`): WI claim, merge, the `status-map` step, pre-commit, manual | **W** (display) |

> **Two further corrections to the deep-check's Q3 table.** (i) `plan_round.py:319`
> is **not** a caller of `spine_stage_of` — it is the *docstring* of
> `page_action(human_held, …)` (`plan_round.py:315–329`), which explicitly says it
> "takes a bool rather than re-deriving one" (`:322–323`); `plan_round.py`
> contains zero references to `spine_stage_of`. There are three call sites, not
> four. (ii) `window_open`/`product_floor`'s `def`s are at `check.py:1139`/`:1233`;
> the line numbers cited in the deep-check land mid-docstring.

**Note on H.** Its docstring says *"read the committed value, never recompute
here"* (`check_trajectory.py:1816`), but mechanically it reads `root / GATE_FILE`
off the **filesystem** (`:1823`) — the working tree, not the index. The intent
("consume the cache, don't recompute") is honoured; the word "committed" is
loose. It also silently drops unparseable bars (`:1836`), so a cache carrying a
retired vocabulary makes the phase-drop detector go **vacuous** rather than red.

## 4.3 Tally

| Class | Count | Ids |
|---|---|---|
| **P** protected | 2 | B (`parse_cache` — the enforcer itself), the hook's `_step_gate` (always `"all"`) |
| **W** windowed | 6 | A, C, F, G, H, I |
| **X** broken | 1 | D (`intake._gate_moved`) |
| **DEAD** — documented but never invoked on `docs/gate` | 1 | E (`read_declared`) |

**So of the nine readers the deep-check named, one is broken, one is not a
reader at all, two are protected, and six are windowed** — every windowed one
self-correcting on the trunk **except F**, which is both windowed *and* hoisted
out of the loop it governs.

---

# 5. THE STALE WINDOWS, RANKED BY CONSEQUENCE

## W-1 — A CLAIMED WORK BRANCH HAS NO GATE FRESHNESS ENFORCEMENT AT ALL

**The window.** From the moment a branch has `docs/work/active/<branch>/` until
its work merges to trunk, `derived-gate` reports SKIP on every `check.py` run,
including the pre-commit hook. A spine edit on that branch leaves `docs/gate`
stale for the branch's entire life, and every commit on it is honestly green.

**Verified — D3.** On a scratch repo whose branch matches an active claim dir:

```
_TRUNK_FRESHNESS_STEPS: ['derived-gate', 'okf', 'open-items', 'ratify-fresh', 'status-map', 'trajectory-map']
_work_branch(root)     : wi999-demo
  _work_branch_skip(derived-gate      ) -> ('SKIP', "work branch 'wi999-demo' — generated freshness is the trunk lane's, concurrency-restructure §5.2", ...)
  _work_branch_skip(registry-integrity) -> None
  _work_branch_skip(trajectory        ) -> None
```

**Is it a defect?** **No — it is a declared design**, and the rationale is
stated at `check.py:1538–1549`: a work branch must never commit a generated
artifact, so freshness "is the trunk lane's". The window is closed at merge by
W1 (`integrate.py:1436` → `trunk_step` → regen, and the claim commit at `:773`).

**But it voids a safety argument that is written down elsewhere as if it were
unconditional.** `spine_stage_of`'s docstring (`agent_common.py:764–767`) says:

> "Read rather than recomputed: `docs/gate` is a freshness-gated generated
> artifact, so **the cached value is either current or the `derived-gate` step is
> already red**."

On a claimed work branch the `derived-gate` step **cannot** be red — it is
skipped. So the premise that licenses reader F to trust the cache is false in
exactly the lane where agents do their work. This is the one finding in this
document that is a genuine mismatch between a stated invariant and the
mechanism, rather than a designed handoff.

**Does anything material get decided inside it?** Yes, structurally:
`human_held` ← `human_holds(docs, spine_stage_of(root))` drives dispatch
admission (`dispatch.py:370`), escalation stops (`agent_loop.py:2324`/`:2378`),
and intake's `recommend`-vs-`flip` (`intake.py:1402`). **But at THIS repo's dial
it is inert** — see §5.6.

## W-2 — READ-ONCE-PER-RUN: a mid-session flip is invisible for the rest of the run

**The window.** `spine_stage_of` is called **once per run**, and the derived
`human_held` is frozen and threaded down:

- **`agent_loop`** — read at `agent_loop.py:2952` in `main()`'s preamble, frozen
  onto the context at `agent_loop.py:3200–3202` (`ctx.session_hold`,
  `ctx.human_held`, `ctx.keep_nondependent`), then consumed per tick without
  re-reading: `session_bookkeeping` at `:2166` (`getattr(ctx, "human_held", True)`),
  used at `:2324` and `:2378`; `page_action` at `:3068`. The tick loop is
  `for i in range(1, args.max_iterations + 1)` at `:3223–3226`.
- **`dispatch`** — read at `dispatch.py:1290`, the comment stating it outright
  (`:1286–1288`): *"one ordinal comparison, made once per run, threaded down
  exactly as the enum was."* Passed into `_admit` on every tick (`:1345`) and
  thence `_claim_lanes` (`:1164`). The loop is `while True:` at `:1297`.

**What makes this more than theoretical: the file is regenerated *inside* that
same run.** `trunk_step.regen` runs `derive_gate.py` on **every claim**
(`integrate.py:773`) and **every merge** (`integrate.py:1436`) — and those merges
are driven by the very dispatcher that hoisted the value (`dispatch.py:231`
`_drain`, `:658` the merge slot). So a long-lived run demonstrably regenerates
the gate it is no longer reading. Regeneration cannot fix this window; only
process exit can.

**Contrast within the same loop:** `ac.tracked_pause` **is** re-read at the top of
every tick (`dispatch.py:1301`), as is `ac.working_tree_dirty` (`:1314`). The
pause dial is live; the gate stage is not. That asymmetry is the clearest
statement of the defect: two policy inputs to the same loop, one polled and one
hoisted, with no recorded reason for the difference.

**Consequence:** same decision set as W-1, same dial-dependence (§5.6).

## W-3 — STAGED-WHILE-STALE: the hook compares the working tree

**The window.** E2 reads the tree **on disk**; the index is compared only by E3,
which is **warn-only** and, by its own comment, does not catch an artifact
*staged while stale* (`hooks/pre-commit:255–258`). Two shapes land a stale gate
in history over a green hook:

- regenerate but forget `git add` → the disk is fresh, the hook is green, the
  commit carries the old bytes. E3 warns; nothing blocks.
- stage a stale `docs/gate` while the working copy is fresh → same outcome.

**Closed by:** CI (E4/E5), which checks out the committed tree. So the window is
one push long, and its consequence is a red build rather than a bad decision.
This is already recorded as **OI-31**, whose option (a) — gates reading the
staged tree — is the named destination.

## W-4 — DISPLAY SURFACES REGENERATE *FROM* THE STALE CACHE, SO THEIR OWN FRESHNESS CHECKS PASS

`docs/status.md` (reader I) and `PROJECT_STATE.html` (reader C) are generated
**from** `docs/gate`. Their freshness steps (`status-map`, `trajectory-map`)
regenerate and byte-compare. If the gate is stale, the surfaces regenerate
*consistently with* the stale gate and both steps go **green**. Only
`derived-gate` detects the underlying rot — and `status-map`/`trajectory-map` are
in `_TRUNK_FRESHNESS_STEPS` too, so on a work branch all three are off together.
Consequence: cosmetic (a wrong stage sentence in a tracked file), but it means
**no second, independent detector exists**; the whole stage axis rests on E1
alone.

## W-5 — `intake._gate_moved` IS BROKEN (X): it can never see any write

Confirmed independently of the deep-check. `intake.py:486` takes
`out.splitlines()[0].strip()` — the **first** line of `docs/gate`, which since
the derived model is the static header comment (`derive_gate.py:1360`), not the
first *non-comment* line every other reader takes.

**Verified — D5:**

```
=== line 0 of docs/gate at several revs (what _gate_moved compares) ===
HEAD         line0 = # DERIVED BAR — generated by scripts/derive_gate.py (do not hand-edit).
HEAD~5       line0 = # DERIVED BAR — generated by scripts/derive_gate.py (do not hand-edit).
08c985cb     line0 = # DERIVED BAR — generated by scripts/derive_gate.py (do not hand-edit).

=== what the VALUE actually was at those revs (last non-comment line) ===
HEAD         value = DevStg-Reqs
HEAD~5       value = DevStg-Reqs
08c985cb     value = DevBar-Reqs
```

The header is byte-identical across the whole derived-gate era, so `values[0] !=
values[1]` is always `False` and `tier_signal` (`intake.py:242`) can never mint
its `strong` adjudication row. Note the third row: at `08c985cb` the value
genuinely **was** different (`DevBar-Reqs` vs `DevStg-Reqs`) — a real move this
reader would have missed. This is not a window; it is a permanently blind
reader.

## W-6 — no new *broken* reader, but two scheduling surprises

No second reader is broken in `_gate_moved`'s sense. Two facts about *when*
readers run were not in the census or the deep-check, and both cut the same way —
**less enforcement at commit time than the file's header implies**:

1. **`product_floor` and `window_open` never run at pre-commit.** `main()` exits
   at `check.py:2264` (`--run-steps`) and `:2239` (`--run-step`) *before*
   `resolve_plan` at `:2266`, and both functions are reachable only through it
   (`:1350`, `:1353`→`:1429`). The hook uses `--run-steps` exclusively
   (`hooks/pre-commit:269`, `:304`). So the WI-473 product floor and the entire
   advisory tier are **structurally absent from the commit boundary** and fire
   only at the merge bar, in CI, and on manual full runs.
2. **`read_declared` is a dead gate reader** (§4.1 correction) — the kit
   documents a reader for `docs/gate` that no call site uses.

Neither is a stale-value bug; both mean the *commit-time* enforcement surface is
narrower than the reader inventory suggests. `derived-gate` itself **is** at the
commit boundary, which is what matters for the owner's question.

## 5.6 The de-escalation: at THIS repo's dial, W-1 and W-2 are INERT

`docs/process.toml:69` declares `human_ratification_through = 4`, and
`DIAL_HOLDS[4]` is `None` — the "holds everything" short-circuit
(`agent_common.py:583–586`). **Verified — D4:**

```
  --- human_holds: CACHED DevStg-Reqs  vs  LIVE DevStg-Arch ---
     dial 0: cached=False live=False
     dial 1: cached=False live=False
     dial 2: cached=True  live=True
     dial 3: cached=True  live=True
     dial 4: cached=True  live=True
```

At dial 4 every rung is human-held, so **no value of `spine_stage_of` — fresh,
stale, or `None` — can change a single decision in this repo.** The stage axis's
staleness is today a latent property, not a live one.

It becomes live for an adopter at dial 1, 2 or 3, and only across specific rung
boundaries, since `DIAL_HOLDS` is `{0: {}, 1: {Needs, Boundary}, 2: {…, Reqs,
Arch}, 3: {…, LLReqs}, 4: None}`:

| Dial | The crossing where a stale stage flips `human_holds` |
|---|---|
| 1 | `DevStg-Boundary` → `DevStg-Reqs` |
| 2 | `DevStg-Arch` → `DevStg-LLReqs` |
| 3 | `DevStg-LLReqs` → `DevStg-Tests` |

Note the direction of the error: a **stale-low** cached stage (the common case,
since regeneration lags ratification) reports a *lower* rung, which is *more*
likely to be held — i.e. **more human involvement, not less**. That is the
fail-honest direction, and it is the same direction `spine_stage_of`'s
`None` fallback takes.

---

# 6. THE IMPLICIT SUB-QUESTION — a spine status flips mid-session: who regenerates, and can the flip commit without it?

**Who regenerates.** There is no automatic regeneration on the commit path. In
order of how the flip actually reaches the cache:

1. **A human or agent runs `python scripts/derive_gate.py`** — the documented
   ratification follow-up (`skills/gate-advance/SKILL.md:68`: *"Regenerate after
   a ratification"*). This is W2, and it is the normal path for an approval
   commit.
2. **`trunk_step.py --regen`** at intake mint (`intake.py:1273`), integrate claim
   (`integrate.py:773`) or lane refresh (`integrate.py:1436`) — trunk lane only.
3. **Nothing else.** The hook, `check.py` and CI verify but never write.

**Can the flip commit WITHOUT the regen?** The `--check` step is designed to
refuse exactly this, and it does refuse — **on the trunk**. Two paths get past
it:

- **On a claimed work branch: YES, always.** E0 skips the step (D3). The flip
  commits, the branch stays green, the cache stays stale until merge.
- **On the trunk, via the index: YES, narrowly.** E2 compares the working tree,
  so a regenerated-but-unstaged (or staged-stale) gate lands in history over a
  green hook; E3 only warns (W-3). Caught by CI one push later.

**Does the check recompute from the LIVE registries, or from a cached input?**
**From the live registries — verified.** D2 flipped one cell in
`docs/requirements/system-requirements.toml` and `--check` immediately went red,
which is only possible if it re-derived from the edited file:

```
=== (a) derive_gate.py --check, cache NOT regenerated ===
derive_gate: docs/gate STALE — the derived gate moved but the cache did not.
  cached: gate=DevStg-Reqs basis='# basis: … drafted=9 … stage=DevStg-Reqs stage-ord=2 stage-of=8'
  now:    gate=DevStg-Reqs basis='# basis: … drafted=8 … stage=DevStg-Arch stage-ord=3 stage-of=8'
  run `python scripts/derive_gate.py` and commit the result.
EXIT=1
```

**One structural detail this exposes, and it matters.** Look at the two `gate=`
fields: **`DevStg-Reqs` on both sides. The bar line did not move at all.** A
single SR going `Drafted`→`Approved` moved `drafted=9→8` and the stage two
rungs (`DevStg-Reqs` ord 2 → `DevStg-Arch` ord 3) while the runnable bar stayed
put, because the raw level is still `DevStg-Below` (other drafts remain) and the
floor pins it at `DevStg-Reqs`. **So the entire detection of this approval rests
on `--check` comparing the `# basis:` line whole.** A `--check` that compared
only the value line — which is what the file's own header describes as "the
value" (`docs/gate:5–6`, `:26`) and what five of the readers take — would have
passed this commit silently. The whole-line comparison is documented as
deliberate at `derive_gate.py:1296–1299`, and this is the case that shows why.

---

# 7. VERDICT — is the scheduling sound?

**Largely yes, with one real hole and one broken reader.**

**The design is coherent and the ordering is right.** Writes are concentrated in
one function with one production caller; enforcement recomputes from live state
rather than trusting any cached input; the enforcement step is tagged at every
bar so no bar setting can drop it; and it blocks at the commit boundary rather
than only in CI. The readers all read fresh per call. Crucially, the one
structural risk — that `check.resolve_gate` selects a plan from a possibly-stale
value *before* the freshness step runs — is neutralized on the trunk by the fact
that the run cannot go green: the wrong plan is selected, then the run fails. A
window in which a decision is made but never acted on green is a design, not a
defect.

**The hole is the lane stand-down (W-1).** `derived-gate` is skipped on every
claimed work branch. That is deliberate and reasoned (`check.py:1538–1549`), and
the window is closed at merge — so as a *cache-freshness* policy it is
defensible. What is not defensible is that `agent_common.spine_stage_of`
(`:764–767`) justifies trusting the cache with the claim that the step "is
already red" if it were stale, which is precisely false in that lane. Either the
reader's premise or the stand-down's scope is wrong; today they contradict each
other in writing.

**The stacked consumer cache (W-2) is the part that regeneration cannot fix.**
Reading the stage once per run and threading it down means a correctly-executed
mid-session ratification *still* does not reach the running loop.

**But nothing material is decided inside any of these windows in this repo
today.** At `human_ratification_through = 4` every rung is human-held, so the
stage value cannot change a dispatch, an admission, an escalation or an
adjudication (D4). W-1 and W-2 are latent here and become live only for an
adopter at dial 1–3, and then only across three specific rung boundaries — and
the error direction is toward *more* human involvement, which is the safe one.

**The one thing that is simply broken is `intake._gate_moved` (W-5)** — not a
window but a permanently blind reader, one of the four clearance-needing
behaviours the deep-check's Q2(iii) enumerated, currently not running at all.

**Ranked:**

| Rank | Window | Real? | Decided inside it? | Closed by |
|---|---|---|---|---|
| 1 | W-1 work-branch stand-down | **yes, verified D3** | structurally yes; **inert at dial 4** | merge-time `trunk_step` regen |
| 2 | W-2 read-once-per-run | **yes** | same set; **inert at dial 4** | nothing — next process exit only |
| 3 | W-5 `_gate_moved` (X) | **yes, verified D5** | the `strong` adjudication row is never minted | nothing |
| 4 | W-3 staged-while-stale | **yes** | no — costs a red CI build | CI, one push later |
| 5 | W-4 display consistent-with-stale | **yes** | no — cosmetic | `derived-gate` only |
| 6 | W-6a `product_floor`/`window_open` absent at pre-commit | **yes** | no — the floor applies at the merge bar instead | merge bar / CI |
| 6 | W-6b `read_declared` documented as a gate reader, never invoked | **yes** | no — dead path | nothing (docstring only) |

**Two things the owner may want to weigh, stated as findings and not as
recommendations.** First, W-1 and reader F's docstring cannot both be right; one
of them should move. Second, W-2 is a one-line-shaped difference — `dispatch`
already re-reads `tracked_pause` per tick — but changing it would alter when a
running loop's ratification authority can flip mid-session, which is a policy
question, not a refactor.

---

# 8. THE DEMONSTRATION

A scratch COPY of this repo's `docs/` tree was made in the session scratchpad.
Nothing in the repo was modified.

**D1 — baseline: the copy is fresh, and the as-of line is excluded.**

```
# basis: SN=27 SR=73 LLR=165 TC=161 drafted=9 uncovered=0 computed=DevStg-Below ex-draft=DevStg-Reqs phase=5 per-phase=… stage=DevStg-Reqs stage-ord=2 stage-of=8
# computed 2026-08-21 (as-of 2bd0ed61)
DevStg-Reqs
--- baseline --check against the COPY ---
derive_gate: docs/gate up to date (DevStg-Reqs).
exit=0
```

Note the cache records `as-of 2bd0ed61` while HEAD is `037b3e3f`, and `--check`
is still green — the compute stamp is genuinely excluded from the comparison.

**D2 — flip one cell, do not regenerate.** `SR-180` `status = "Drafted"` →
`"Approved"` (the repo's only Drafted SR), simulating an approval commit. Output
reproduced in §6. `--check` exits **1**; the bar is unchanged; the basis line
moved on `drafted=` and `stage=`.

**D3 — the trunk-lane stand-down.** Output reproduced in §5 W-1. A scratch git
repo on branch `wi999-demo` with `docs/work/active/wi999-demo/` present:
`derived-gate` → SKIP, `registry-integrity` → runs.

**D4 — the readers inside the live stale window** (after D2's flip, before
regeneration):

```
  CACHED bar (last line)          : DevStg-Reqs
  CACHED stage (basis scrape)     : DevStg-Reqs
  CACHED drafted                  : 9
  LIVE   bar (recomputed)         : DevStg-Reqs
  LIVE   stage (recomputed)       : DevStg-Arch ord 3
  LIVE   drafted                  : 8

  READER A  check.resolve_gate(None)      -> DevStg-Reqs
  READER F  ac.spine_stage_of(root)       -> DevStg-Reqs      <-- STALE (live is DevStg-Arch)
  READER E  ac.read_declared(gate,'all')  -> DevStg-Reqs
  READER G  check.window_open(gate)       -> False
  READER G  check.product_floor(gate)     -> DevStg-Reqs
```

Reader F is demonstrably stale by two rungs. Readers A/G are unaffected only
because the bar did not move — the coincidence §6 explains. (Reader E was called
directly here to show what it *would* return; per §4.1 no production call site
invokes it on this file.)

**D5 — `_gate_moved` is blind.** Output reproduced in §5 W-5.

**D6 — regenerate and the window closes.**

```
=== REGENERATE the scratch gate (the write path) ===
derive_gate: wrote docs/gate -> DevStg-Reqs (# basis: … drafted=8 … stage=DevStg-Arch stage-ord=3 stage-of=8).
--- then --check ---
derive_gate: docs/gate up to date (DevStg-Reqs).
EXIT=0
```

**Live-repo control.** On the real repo, on this branch, the step runs and is
green — the branch name matches no `docs/work/active/` entry, so E0 does not
fire:

```
=== derived-gate : …\derive_gate.py --check ===
derive_gate: docs/gate up to date (DevStg-Reqs).
  PASS  derived-gate     0.2s
EXIT=0
```

---

## Method note

`derive_gate.py` was run as a subprocess against a scratch COPY of `docs/`;
`check.py` / `agent_common.py` functions were driven in-process from throwaway
scripts in the session scratchpad, with `check.GATE_FILE` repointed at the copy.
The trunk-lane demonstration used a throwaway `git init` repo in the scratchpad.
The only command run against the real repo was
`python project-trajectory/scripts/check.py --run-step derived-gate`, which is
read-only, plus `git show` reads. Nothing in the tree was modified and nothing
was committed.
