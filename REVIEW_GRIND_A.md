# Grind Review A — Adversarial Correctness (Reviewer A)

**Reviewer:** Claude (Opus 4.8), REVIEWER A — method / risk / corner-case
charter (bugs, unsound methods, failure modes, robustness). · **Date:**
2026-07-10 · **Branch:** `MultiRepoSupport` (not pushed).

**Scope:** commit range `513939e..HEAD` (11 commits landed 2026-07-10):
`check_dupes.py`, `check_doc_refs.py`, `gen_okf.py`, the `agent_loop.py`
`AGENT_CMD_MAP` / `review-policy` / `status_size_warning` additions,
`gen_trajectory.py` (root `PROJECT_STATE.html` + How-SW view + git as-of stamp
+ ASOF_RE), the iterative `_dag_ranks` / `check_trajectory._cycles` rewrites,
`trace.py` TC `Evidence` schema rule, the `okf` / `trajectory-map` pre-commit
steps, and `check.py`. Process / traceability / prose issues are **out of
charter** (sibling reviewer B) and are not reported here.

Every finding was verified against the tree — code read and the failing input
constructed and run read-only (no generator run in write mode, no commit, no
file touched except this report). Nothing here is fixed.

---

## Severity index

| ID | Sev | One-liner |
|----|-----|-----------|
| A1 | MEDIUM | `check_dupes.py` crashes with an uncaught `TokenError`/`IndentationError` on any un-tokenizable `.py` — against the kit's own convention (`gen_arch_map` catches `SyntaxError`). |
| A2 | MEDIUM | `check_doc_refs.py` false-positives on pytest node ids (`f.py::test`) and `;`-joined path lists, and scans the *generated* `docs/okf/` — so OKF `Evidence` cells self-flag; `--strict` fails CI on legitimate references. |
| A3 | MEDIUM | `agent_loop.seconds_until_reset` mis-computes a same-weekday reset (`"Mon …"` on a Monday → *tomorrow*, not next week); wrong `--wait-on-limit` nap. |
| A4 | LOW | `gen_okf.py` builds output paths from **unvalidated** registry ids — a crafted id with `/` + `..` escapes `docs/okf/` on write (repro below). Backstopped by `trace.py --strict-integrity` on the floor. |
| A5 | LOW | `AGENT_STATUS_WARN_BYTES` is parsed with an unguarded `int()` — a non-integer value crashes the coordinator at startup with a traceback. |
| A6 | LOW/nit | `check_dupes.find_duplicates` merges two *distinct* same-offset duplicate blocks into one finding — inflated `~tokens` length, second block's location hidden. |
| A7 | nit | `gen_okf` write-mode prune removes files but leaves empty tier directories behind (harmless; no false-stale). |

No HIGH findings. The two graph rewrites (`_dag_ranks`, `_cycles`), the ASOF_RE
freshness exclusion, and the `--check` byte-determinism of the new floor gates
were specifically attacked and are sound — see "Verified clean".

---

## A1 — MEDIUM · `check_dupes.py` crashes on un-tokenizable source

**What.** `significant_tokens()` iterates `tokenize.tokenize(handle.readline)`
inside a list comprehension with no guard. `tokenize` raises `TokenError`
(EOF in a multi-line statement / string) and `IndentationError` (a subclass of
`SyntaxError`) on malformed input, and those propagate out of `find_duplicates`
→ `main`, killing the check with a raw traceback instead of a clean finding or
skip.

**Evidence** (`project-trajectory/scripts/check_dupes.py:57-64`, `74-97`,
`120-159`). Verified read-only:

```
$ # bad.py = 'def f(:\n    x = "unterminated\n'
significant_tokens(bad)  -> EXCEPTION: TokenError ('EOF in multi-line statement', (3, 0))
# and through the entry point, over a --src tree containing 'x = (1, 2\n':
check_dupes.main(['--src', d]) -> main EXCEPTION: TokenError ('EOF in multi-line statement', (2, 0))
```

This violates the kit's *own* established convention: the sibling Python-parsing
script `gen_arch_map.py` wraps `ast.parse` in `except SyntaxError: # surface,
don't crash the whole run` (lines 195-196, 370-371, 485-486). `check_dupes` is
the outlier.

**Failure scenario.** A downstream repo wires the documented opt-in step
(`[step:dupes] command = {py} scripts/check_dupes.py --src {src}`). Any single
work-in-progress file with an unterminated string, an unbalanced bracket, a
lingering Python-2 `print` statement, or a non-UTF-8/bad-coding-cookie file
under `src/` turns the whole harness step into a traceback — a *lint* that
aborts on invalid syntax rather than reporting it. Ruff/black in the same repo
would flag such a file gracefully; this one dies.

**Suggested fix.** Wrap the tokenize loop and skip-with-warning on failure, e.g.
in `significant_tokens` catch `(tokenize.TokenError, SyntaxError,
UnicodeDecodeError)` and return `None`; have `find_duplicates` skip files that
return `None` and print one `check_dupes: WARN - <path>: could not tokenize
(<err>); skipped` to stderr. Matches `gen_arch_map`'s "surface, don't crash".

---

## A2 — MEDIUM · `check_doc_refs.py` false-positives on node ids / joined lists, and lints the generated OKF bundle

**What.** `is_path_shaped()` treats a backticked token as a disk path when it
contains `/` and either ends in a known extension **or** starts with a
conventional top-level prefix. Two legitimate, common shapes slip through as
false positives:

1. **pytest node ids** — `tests/test_x.py::test_name` starts with `tests/`, so
   it is path-shaped; `(root / token).exists()` is false → flagged, even though
   `tests/test_x.py` is real. Node ids are the kit's *sanctioned* Evidence form
   (see `trace.py` A-note: "a pytest node, a script path, or a procedure-doc
   link").
2. **delimiter-joined path lists** — `tests/a.py;tests/b.py` (semicolon, no
   space) is one token ending in `.py` → path-shaped → one nonexistent path.
   (A comma-*space* list is correctly rejected by the space rule; a bare
   `;`-list is not.)

Compounding this, `doc_files()` scans `docs/**/*.md`, which includes the
**generated** `docs/okf/` bundle. Whole generated files carry no `<!-- BEGIN
GENERATED -->` markers, so the `in_generated` skip never engages, and every
`**Evidence.** \`…\`` line the OKF exporter emits is linted as hand-authored
prose.

**Evidence** (`check_doc_refs.py:74-80`, `83-85`, `109-130`). Verified:

```
is_path_shaped('tests/test_x.py::test_name') = True     # pytest node id
is_path_shaped('tests/a.py;tests/b.py')      = True     # ;-joined list
```

Running the tool against this repo emits 210 warnings, including its own OKF
output feeding straight back in:

```
docs/okf/test-cases/TC-033.md:15: `tests/test_check_perf.py::test_release_checklist_lists_perf_budgets` does not exist
docs/okf/test-cases/TC-021.md:15: `tests/test_pre_commit_hook.py;tests/test_pre_push_hook.py` does not exist
```

The source cell is a valid node id (`test-cases.csv:34`), rendered to backticks
by `gen_okf.py:264-266`, then re-flagged by `check_doc_refs`. The Thread-48
(OKF) and Thread-49 (doc-refs) features collide.

**Failure scenario.** A repo adopts both features and opts doc-refs into its
gate with the documented `--strict` (`command = {py} scripts/check_doc_refs.py
--strict`). CI now fails on every TC that cites a pytest node id — legitimate
references the tool's own docstring calls "the design center: false-positive
control". Warn-first spares the *default*, but `--strict` is the advertised
gating mode.

**Suggested fix.** (a) In `is_path_shaped`, reject tokens containing `::` (node
id) and split on `;`/`,` before shaping each part — or exclude the `Evidence`
shape from the path tier. (b) Exclude the generated tree: skip any doc whose
path is under `docs/okf/` (and any dir marked `linguist-generated` in
`.gitattributes`), the same "don't lint generated output" logic the marker-block
skip already encodes.

---

## A3 — MEDIUM · `seconds_until_reset` mis-handles a same-weekday reset

**What.** After aligning the target to the named weekday, the code does
`while target <= now: target += timedelta(days=1)`. When the hint's weekday is
*today* and its time has already passed, `ahead == 0` so `target` is today, then
the `+= 1 day` loop bumps it to **tomorrow** — a different weekday — instead of
+7 days to next week's same weekday.

**Evidence** (`agent_loop.py:511-542`). Verified with `now = Mon 2026-07-13
15:00`:

```
'Mon 12:00am' -> 32400s -> 2026-07-14 00:00 (Tuesday)   # should be next Monday
'Mon 3:00pm'  -> 86400s -> 2026-07-14 15:00 (Tuesday)   # reset == now, bumped a day
'Tue 12:00am' -> 32400s -> 2026-07-14 00:00 (Tuesday)   # correct
```

For a weekly-limit message "…weekly limit · resets Mon 12:00am" seen on a Monday
afternoon, the true reset is the *following* Monday; the function returns ~9h
(next midnight) instead of ~6 days.

**Failure scenario.** Only reachable with `--wait-on-limit` set high enough to
cover the (wrong, short) nap: the loop sleeps to Tuesday 00:00, wakes, re-hits
the still-active weekly limit, burns one session. It then self-corrects (now on
Tuesday, `ahead` computes to the real next Monday), so blast radius is **one
premature wake + one wasted session** at the same-weekday boundary. With the
default `--wait-on-limit 0` the wrong value is never used for sleeping (the loop
exits WAITING with the correct raw hint text), so this is bounded — but it is a
clear wrong-answer in the feature's core date math.

**Suggested fix.** When a weekday is named, advance by whole weeks past `now`:
`while target <= now: target += timedelta(days=7)` in the weekday branch (keep
the 1-day step only for the no-weekday case).

---

## A4 — LOW · `gen_okf.py` derives output paths from unvalidated ids (write-mode traversal)

**What.** `real_rows()` accepts any id that `startswith(prefix)` and does not
end in `-000`; `emit()` then uses that id verbatim as a path component
(`"system-requirements/{}.md".format(cid)`), and write-mode does
`(out_root / rel).open("w")` after `mkdir(parents=True)`. No id-shape guard, so
a crafted id containing `/` and `..` writes **outside** `docs/okf/`.

**Evidence** (`gen_okf.py:67-73`, `214`, `418-425`). Path-resolution verified
read-only (no write performed):

```
cid='SR-/../../../evil'  -> C:\Projects\ai-template\docs\evil.md   INSIDE_okf=False
cid='SR-001'             -> ...\docs\okf\system-requirements\SR-001.md  INSIDE_okf=True
```

The prune half is **safe** — `on_disk()` keys come from
`p.relative_to(out_root)` of real files, so `unlink` targets never escape
`out_root`. `--check` never writes (a bad key just reports STALE and exits 1).
The exposure is write-mode only.

**Practical severity is LOW:** the pre-commit floor runs `trace.py
--strict-integrity`, which enforces `SR-ID` = `^SR-\d+$` (trace.py:244-246) and
blocks such an id from ever committing; registries are trusted, human-reviewed
input. But `gen_okf` is run standalone (manual write) and does not itself apply
the id discipline the rest of the kit does — defense-in-depth gap that
path-safety was in scope to flag.

**Suggested fix.** Validate ids against the same `^PREFIX-\d+$` shape (or reject
any id containing `/`, `\`, or `..`) in `real_rows`/`sn_rows` before using them
as path components — cheap, and consistent with `trace.py`.

---

## A5 — LOW · Unguarded `int()` on `AGENT_STATUS_WARN_BYTES` crashes startup

**What.** `int(os.environ.get("AGENT_STATUS_WARN_BYTES", "8192"))` runs
unguarded at coordinator startup; a non-integer env value raises `ValueError`
before the loop begins.

**Evidence** (`agent_loop.py:990-991`). Verified: `AGENT_STATUS_WARN_BYTES=8k`
→ `ValueError: invalid literal for int() with base 10: '8k'`. (Contrast the
integer args routed through argparse `type=int`, which fail with a clean usage
message.)

**Failure scenario.** An operator sets `AGENT_STATUS_WARN_BYTES=8k` (or `8192 `
with a stray char) in the launcher environment; the whole walk-away run dies at
launch with a traceback rather than warning or falling back to the default —
a poor failure for a "warn-only, advisory" tripwire.

**Suggested fix.** Parse defensively: `try: limit = int(env)` / `except
ValueError: limit = 8192` (the same default), or fold the size warning behind a
`try` so a misconfig never blocks the run the warning is meant to help.

---

## A6 — LOW/nit · `check_dupes` offset-merge conflates distinct same-offset blocks

**What.** `find_duplicates` groups sliding-window hits by `first_line - line`
offset, then reports `min(hits)` with `length = min_tokens + len(hits) - 1`.
Two *separate* duplicated regions between the same file pair that happen to
share the same line offset are merged into one finding: the reported length is
inflated (as if one contiguous block), and the second region's location is
hidden.

**Evidence** (`check_dupes.py:98-106`). Verified with two identical ~59-token
blocks separated by a gap, duplicated across `a.py`/`b.py` at offset 0:

```
(a.py:1) == (b.py:1)  length ~= 141   # reports one 141-tok block; it is two blocks + a gap
```

Still fails (exit 1) and points at the pair, so the duplication is *not* missed
— only its extent/second-location is mis-described. Reporting-accuracy nit.

**Suggested fix.** Key the merge on offset *and* window-contiguity (break a group
where the hit line numbers are non-adjacent), or simply report each contiguous
run separately.

---

## A7 — nit · `gen_okf` write-prune leaves empty directories

`main()` prunes stale *files* (`unlink`) but never removes the now-empty tier
directory (e.g. `docs/okf/interfaces/` after the last IF row is deleted).
`on_disk()` enumerates only `p.is_file()`, so the empty dir is not counted as
stale and `--check` stays green — harmless filesystem cruft, noted for
completeness. Optionally `rmdir` empty parents after pruning.

---

## Verified clean (attacked, found sound)

- **`_dag_ranks` iterative longest-path rewrite** (`gen_trajectory.py:394-426`).
  Traced diamond and reverse-order inputs by hand; post-order guarantees a node
  is ranked only after all non-cyclic predecessors, so rank = 1 + max(pred
  ranks) is correct. Duplicate stack pushes are absorbed by the `if n in rank`
  top-of-loop guard; the `on_path` exclusion is provably inert for DAGs (a pred
  on the path would be a cycle) and degrades a stray back-edge to "no
  constraint" rather than spinning. Terminates on any input.
- **`check_trajectory._cycles` iterative DFS** (`check_trajectory.py:146-181`).
  Standard WHITE/GREY/BLACK back-edge detection; `path` stays in lock-step with
  the GREY stack (push/pop together, `found.append` doesn't touch either).
  `pred_map` values are pre-filtered to known ids, so `colour[p]` is always
  defined; shared nodes go BLACK and are correctly not re-reported as cycles.
  O(V+E), terminates.
- **ASOF_RE freshness exclusion** (`gen_trajectory.py:76`, `1068-1080`). The
  excluded `<p class="asof">…</p>` contains only git-derived commit/date text
  (never user content, no nested `</p>`), and `re.sub` strips it from *both*
  sides of the compare. No real content can hide behind it; a stale artifact
  still fails the byte-compare on everything else.
- **`--check` byte-determinism of the new floor gates** (`gen_okf`,
  `gen_trajectory`). Content is derived purely from the registry/README/arch
  files — no clock (OKF omits the optional `timestamp`; the dashboard's only
  clock is the excluded asof), no locale, no git state. `links()` sorts via
  `sorted(set(...))`, `real_rows` sorts by id, DAG barycentres are integer-index
  sums (exact), JSON blobs preserve deterministic insertion order. Ran both
  `--check` on this repo: "up to date". `.gitattributes` `* text=auto eol=lf`
  plus `gen_okf`'s explicit `newline="\n"` keep it CRLF-proof; `read_text`
  normalizes newlines on compare so autocrlf checkouts don't false-stale.
- **`build_argv` / `split_cmd` command-template safety** (`agent_loop.py:380-403`).
  shlex with `escape=""` preserves Windows `C:\` paths; `{model}`/`{prompt}` are
  substituted per-token *after* splitting and never pass through a shell
  (`subprocess.run(list)`), so a multi-line prompt injects no args. The
  `AGENT_CMD_MAP` comma/semicolon limitation is documented and fails safe at
  preflight (`=`-inside-template survives via `partition`; a comma-split
  fragment without `=` raises, or a spurious phase's missing exe is caught).
- **`gen_okf` prune traversal** — safe (keys are real relpaths under
  `out_root`); the write-path gap is A4.
- **arch_icicle recursion** (`gen_trajectory.py:232-298`). `link()` only ever
  connects SN→SR→LLR→TC (+SR→TC), each child gets exactly one parent, so `kids`
  is a depth-≤4 forest — `wt`/`collect`/`draw` cannot recurse unbounded or cycle.
  Division-by-zero guarded throughout (`def_pct`, `wi_pct`).
- **Python 3.8 floor.** Scanned the five new/changed scripts for 3.9+ APIs
  (`removeprefix`, `graphlib`, `zoneinfo`, `dict|dict`, `str|None` annotations,
  walrus) — none. `gen_okf` explicitly uses `open(newline=)` over the 3.10-only
  `write_text(newline=)` (documented at line 422-423).
- **`trace.py` TC `Evidence` rule** (`trace.py:485-499`). Conditional on
  `Automated==yes`; a legacy CSV lacking the column reads `None`→empty and is
  flagged only when the claim is present. Lives in `schema_findings` (gate-scoped),
  not `--strict-integrity`, so it does not block early-stage floor commits.
