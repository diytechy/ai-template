## 2026-08-22 — WI-503: the re-attestation brief splits into CURRENT.md + immutable dated briefs

**Summary.** `trace.py --ratify modified --check` used to gate whichever
`docs/ratify/*.md` file was newest **by filename**, so a regeneration rewrote
a DATED file — read as the record of one sitting — in place; measured before
this WI, `docs/ratify/2026-08-13-wi444.md` carried ten rewrites, none about
WI-444. The split makes `docs/ratify/CURRENT.md` the one file a regeneration
ever touches and a dated `docs/ratify/<date>-<slug>.md` something MINTED once
and enforced immutable, per the queued spec's adopted design.

**Design decisions.**

- **Mint surface: `trace.py --mint-ratify-brief SLUG [--mint-date DATE]`**,
  not a new script or an `intake.py` flag. The mint is a plain file copy
  (`CURRENT.md` -> a dated name) over machinery `trace.py` already owns
  (`current_ratify_brief`, the fixed CURRENT.md path) — the smallest-total-
  code home. A sibling script would duplicate that path knowledge;
  `intake.py`'s writers are all registry-shaped (TOML cell mutation), not a
  byte copy of a rendered view, so it would be the wrong seam to extend.
- **Immutability enforcer: `check.py --ratify-immutable`**, the `staged_
  divergence` sibling — same read shape (`git diff --cached`, same
  degradation ladder off-git/outside-checkout/wrong-root) but the opposite
  question: not "did you forget to stage a regeneration" but "does this
  commit rewrite a dated brief that already exists". Reads `--name-status
  --no-renames` on the STAGED tree (what the commit is about to contain) and
  refuses anything other than a plain `A` (add) on an existing
  `docs/ratify/<date>-*.md` — `CURRENT.md`/`README.md` exempt. Fail-closed by
  default, no `--strict` switch: unlike `staged-divergence`, there is no
  honest partial-compliance state for "a sign-off record just got rewritten".
  Wired into `hooks/pre-commit`'s batched floor and `check.py`'s built-in
  `steps()`, at every bar (never stood down on a work branch — it reads the
  staged tree, not a regenerated artifact's freshness, matching the reasoning
  `staged-divergence` already states for the same non-membership in
  `_TRUNK_FRESHNESS_STEPS`).
- **`docs/stack.ini`'s `[generated]` row is UNCHANGED**: `docs/ratify/ =
  ratify` was already a directory prefix, so it already covers one
  regenerated file plus N immutable ones with no edit — only the comment
  block gained an explicit statement of the split.

**Deliverables.**

- `project-trajectory/scripts/trace.py`: `current_ratify_brief` (fixed
  `CURRENT.md` path) replaces `newest_ratify_brief` (newest-by-filename);
  `mint_ratify_brief` + `_cmd_mint_ratify_brief` + the `--mint-ratify-brief`/
  `--mint-date` flags; `ratify_check`'s default out-path now resolves to
  `CURRENT.md`.
- `project-trajectory/scripts/check.py`: `ratify_immutability`,
  `_is_dated_ratify_brief`, `_ratify_immutable_mode`, the `--ratify-immutable`
  flag, the `ratify-immutable` step (registered in `steps()` and
  `BUILTIN_STEP_NAMES`).
- `project-trajectory/hooks/pre-commit`: `ratify-immutable` added to the
  batched `--run-steps` floor, with its own explanatory block.
- `docs/ratify/CURRENT.md` regenerated and committed (window currently
  closed — "No spine row differs" — this seeds the live surface).
- `docs/ratify/README.md`, `docs/registry-machinery-reference.md`'s command
  reference, `docs/stack.ini`'s `[generated]` comment: updated to the new
  two-step (`--out CURRENT.md` then `--mint-ratify-brief`) workflow.
- `project-trajectory/skills/gate-advance/SKILL.md` (the neutral source):
  corrected — it recommended `--out docs/ratify/<date>-reattest.md` directly,
  the exact anti-pattern this WI fixes. Fan-out copies (`.claude/`,
  `.agents/`) refreshed via `bootstrap.py --sync` (`gen_skills_index.py
  --check-agents` confirmed fresh after).
- `project-trajectory/RESYNC_PACK.md`: new entry, `[since d08b5bd2]`, matching
  the newest entries' form.
- `tests/test_trace_briefs.py`: `newest_ratify_brief` test replaced with
  `current_ratify_brief` coverage; new tests for the CURRENT.md default-check
  path (a decoy dated file must never be read as live), `mint_ratify_brief`
  (copy, refuse-without-CURRENT, refuse-to-overwrite, slug validation) and its
  CLI body.
- `tests/test_check_harness.py`: `ratify_immutability` driven end to end —
  refuses a staged edit, refuses a staged delete, permits a brand-new dated
  add (the mint's shape), permits regenerating `CURRENT.md`/`README.md`,
  ignores an unstaged edit, silent on a clean tree, skips cleanly outside git,
  and the same refusal driven through `--run-steps` (the wiring the hook
  actually uses).
- `docs/work/complete/WI-503-ratify-brief-split.md`: closed spec, renamed from
  the queued 42-char stem (WARNed by `check_trajectory --strict`, ceiling 37)
  to the 25-char `WI-503-ratify-brief-split`.

**gen_open_items.py needed no change**: it derives the pending/attestation
summary from `trace.reattest_model` (registry state) directly, never from a
`docs/ratify/*.md` file path — confirmed by re-running `--check` and reading
the regenerated page.

**Scaffold surface: nothing to update.** `bootstrap.py` MAPPING ships nothing
under `docs/ratify/` (grepped, confirmed) — `tests/test_bootstrap.py`'s file
lists are untouched.

**Deviations from spec.** One incidental fix, load-bearing for driving the
mint CLI's failure path as a test: `trace.py main()`'s `_writer_mode`
dispatch used a bare `return` where `main()` is called bare (not
`sys.exit(main())`) at the bottom of the module, so a WRITER's failure exit
code (`--correct-mark`, `--bump-ids`, now `--mint-ratify-brief`) was silently
swallowed and the process always exited 0. Changed the one line to
`sys.exit(writer_code)` — the same posture the `--ratify --check` path three
lines above it already documents and follows.

**Ratchets re-stamped, reviewed, reason recorded at each entry (`tests/
test_module_size_ratchet.py`):** `check.py` 2176 -> 2326 (net +150 after
`ruff format` tightened two multi-line calls, the
immutability enforcer + its wiring); `trace.py` 5361 -> 5457 (+96, the mint
verb + the CURRENT.md rename + the writer-mode exit-code fix). Smoke
membership untouched: every new test lives in `test_trace_briefs.py` /
`test_check_harness.py`, both already in `conftest.SLOW_MODULES`.

**Gates.**

- `python -m pytest -q -n auto -m smoke`: **1397 passed, 5 skipped in
  61.20s** <!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=d08b5bd2-dirty -->
  (this box's own variance around the 60s budget, not this WI's doing — see
  `docs/stack.ini [smoke-budget]`'s standing notes on box jitter).
- `python project-trajectory/scripts/check_docs.py --root . --stale`: FAIL
  reported (4 broken links + 1 orphan) — confirmed PRE-EXISTING via `git
  stash` (all four reference the already-closed WI-390 program's old path;
  none touch a file this WI edited).
- `python project-trajectory/scripts/check_trajectory.py --root . --strict`:
  clean, exit 0 — the filename-stem WARN this WI's own queued spec carried
  (42 chars, ceiling 37) is resolved by this close's rename.
- `python project-trajectory/scripts/check.py --run-steps
  okf,trajectory-map,status-map,open-items,trajectory,registry-integrity,
  derived-stage,skills-sync,skills-index,prompt-catalog,ratify-fresh,
  ratify-immutable,staged-divergence`: all PASS on the staged tree.
- `python -m pytest -q -n auto --basetemp=D:\pytest-tmp` (full, unfiltered),
  clean single foreground run: **1 failed, 2890 passed, 14 skipped in
  1153.77s (0:19:13)** <!-- fig: cmd="python -m pytest -q -n auto --basetemp=D:\pytest-tmp" rev=d08b5bd2-dirty -->.
  The one failure, `tests/test_check_docs.py::test_meta_repo_has_zero_
  unexplained_orphans`, is PRE-EXISTING and unrelated: three broken links
  under `docs/archive/`/`docs/runtime-flows.md` naming the already-closed
  `docs/work/active/wi390-concurrency-v2-program-close/...` path. Confirmed
  by running the identical test against `git stash` (this WI's diff fully
  reverted): byte-identical three-link failure, same paths, same lines —
  this WI's diff touches none of them. (Two earlier full-suite attempts on
  this box produced noise from operator error, not this WI: a first run was
  launched backgrounded and mistakenly treated as still-live after the turn
  that started it ended, and a second concurrent run against the same
  `D:\pytest-tmp` basetemp collided with it, leaving stale git
  `index.lock` files and spurious rate-limit/contention failures in modules
  this WI never touches. Cleaned via `TaskStop` + a fresh basetemp; the run
  reported above is the single clean sequential execution.)

**Deferred open items: none** — every Done-when bullet is driven as a test,
both trunk-lane wiring points (`hooks/pre-commit`, `steps()`) are updated,
and the scaffold-surface / RESYNC-pack items the spec flagged as
"if bootstrap ships anything" resolved to "nothing to do", confirmed rather
than assumed.
