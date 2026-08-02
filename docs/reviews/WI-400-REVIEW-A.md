# WI-400 REVIEW-A — independent, hunt-to-break (branch wi-400-… @ cfca0cc2 vs ConcurrencyTrainRewrite)

Method: deletion safety was the whole review. Read `_RESIDUE_DIR_NAMES`/`_RESIDUE_FILES`,
`_is_declared_residue`, `_shed_declared_residue`/`_sweep_residue_dirs` and the
`_unload_branch` wiring against `ignored_files`/`_worktree_dirt`, then DROVE fifteen
scratch-lane scenarios through the real `_unload_branch` (fresh repo + merged `wi-401`
lane worktree per scenario): symlink escapes (link→outside file, link→outside dir, a
symlinked cache dir under both ignore-rule shapes, the declared FILE path itself a
symlink); double-lock integrity (tracked file force-added inside `__pycache__`, the
same file MODIFIED, ignored-undeclared `out/run-logs/` stream, a FILE named
`__pycache__`, deep `x/__pycache__/y/z` nesting, `x.pytest_cache/` substring segment,
`tests/docs/test/report.md` at the wrong relative path, plus a path-ALIAS attack on
the lock itself); scope geometry (repo-root `out/` beside a refusing lane); the cwd
fix (cwd deep inside the lane, cwd outside untouched); and the six measured drain
paths verbatim, alone and plus one `orphan.txt`. Then the module tests, smoke, strict
checks, figures, doc-refs, ratchet, ruff on this box.

1. [MINOR] project-trajectory/scripts/integrate.py:1479 (`ignored_files`, consumed at
   :1328-:1337) -> the double-lock can be bypassed by a PATH ALIAS: `ignored_files`
   returns `{p.replace("\\", "/") ...}` over `git ls-files -o -i -z`, so on POSIX a
   git-ignored file literally NAMED `x\__pycache__\evil.pyc` (backslashes in one
   filename) is reported as `x/__pycache__/evil.pyc`, `_is_declared_residue` matches
   the mangled segments, and `wt / rel` then points at a DIFFERENT file — the shed
   unlinks whatever sits at the aliased path, including a TRACKED file the lock
   exists to protect. Driven: lane with a force-added tracked `x/__pycache__/evil.pyc`
   plus the ignored backslash-named file — after `_unload_branch` the tracked twin is
   GONE and the refusal reads `D x/__pycache__/evil.pyc` / `!! "x\\__pycache__\\evil.pyc"`.
   Judged non-blocking: the alias cannot arise by accident (it needs a backslash
   filename whose slash-form collides with a declared cache path AND an ignore rule
   matching it), it crosses no privilege boundary (the lane owner can already delete
   the lane's files), the outcome stays fail-closed and loud (the unload still
   REFUSES, naming both the D and the alias; nothing is removed silently), and the
   deleted file is by construction recoverable (`git checkout --`) in the driven
   tracked shape. The mangle predates WI-400 — `_shed_residue` (:1529-:1533) has had
   the same alias shape since its own WI — but WI-400 widens its reach from
   "since-baseline names" to the whole declared set. -> git emits `/` separators on
   every platform, so the replace is never load-bearing: make it Windows-only (or
   drop it) in `ignored_files` and pin with a backslash-name test; a one-line
   follow-up WI on shared code, not rework of this WI. -> @owner

2. [MINOR] docs/work/complete/WI-400-…md:39-40 ("the bar never generates it") -> the
   recorded REASON for the `docs/test/report.html` exclusion is false: `check.py`
   always passes `--html` to the trace step at G2/G3 (check.py:449-455, in the bar
   since 2026-06-28, commit 9b43bb90) and `trace.py` then writes
   `docs/test/report.html` (trace.py:2882-2885) in whatever tree it runs in — this
   repo is G3, so the declared bar DOES generate it. What is true is narrower: the
   2026-08-01 lanes never SHOWED it (their `report.md` came from plain `trace.py`
   runs, which write report.md unconditionally and report.html only under `--html`),
   and a refresh-added report.html is covered by `_shed_residue`'s baseline diff. The
   gap the false reason hides: a worker who runs `check.py` in the lane leaves a
   PRE-baseline, git-ignored (root .gitignore:13), UNDECLARED report.html that
   neither shed covers — the exact strand-forever class this WI closes, recurring for
   that one path, and the wrong rationale would misdirect the future widen decision.
   The DECISION itself (enumerate only the measured set, widen only on measurement)
   honors the scope guard and is right. -> correct the recorded reason (or mint the
   one-name measurement follow-up); no code change owed. -> @owner

3. [NIT] project-trajectory/scripts/integrate.py:1345 (`_sweep_residue_dirs`) -> the
   directory half carries only the NAME lock, not the git-IGNORED lock: every
   now-empty directory whose relative path contains a declared segment is rmdir'd,
   including one git does not ignore (an empty untracked `x/__pycache__/keep/` in a
   repo with no `__pycache__/` rule). Bounded on every axis — git cannot track empty
   directories, `git status` does not report non-ignored empty ones, and a clean
   `git worktree remove` would delete them with the lane anyway — so the only loss
   shape is load-bearing EMPTINESS inside a cache-named tree in a lane that then
   refuses (the `_shed_residue` docstring's own `docs/work/deferred/` example, but
   inside `__pycache__`). Note only, no change requested. -> @owner

Held under attack (no finding). SYMLINK ESCAPE, the review's whole point, holds on
this platform (macOS/APFS) and in the code's semantics: a symlink planted inside a
declared cache dir pointing at an outside file or outside directory is removed AS THE
LINK (`unlink` never follows; the `is_file() or is_symlink()` guard exists exactly to
catch dir-links), the victims survive byte-identical, and the unload completes —
driven both ways ("[S1a] victim survives=True", "[S1b] victim dir+file survive=True",
victim planted outside the lane beside the repo, the "into the main repo" shape).
There is no `rmtree` anywhere in the path: deletion is per-file `unlink` plus `rmdir`
of empty dirs, and `os.walk(followlinks=False)` never yields a symlinked dir as a
walked parent, so `rmdir` can never land on a link target. A cache dir that IS a
symlink: under the kit's own trailing-slash rules (`.pytest_cache/`) git classes the
link untracked, the first lock refuses, and the unload refuses naming it (driven,
link and target intact); under a no-slash rule it is ignored but `_is_declared_residue`
refuses on the name-never-matches rule (`rel.split("/")[:-1]`), refusal again, target
intact (driven). `docs/test/report.md` as a symlink: link unlinked, outside target
survives (driven). DOUBLE-LOCK: a tracked file inside `__pycache__` is invisible to
`ls-files -o` and survives the shed (its dir survives too — `rmdir` refuses non-empty);
modified, it refuses naming `tracked.txt` with the only-copy content intact (driven);
the ignored-undeclared `out/run-logs/session.md` survives and is refused over; a FILE
named `__pycache__` survives and is named; `x.pytest_cache/` does not match the
segment rule; `tests/docs/test/report.md` survives while the root-relative
`docs/test/report.md` is shed (all driven). SCOPE GEOMETRY holds by construction, not
luck: every deletion target is `wt / rel` with `rel` a repo-relative `ls-files` path
(never `..`, never absolute) under the holder worktree, and `_sweep_residue_dirs`
walks `wt` only — the repo-root `out/run-logs/refresh-refused-*.log` survived beside
a refusing lane (driven). THE CWD FIX: driven from deep inside the lane, the process
ends standing in the resolved repo root (exists), and an outside cwd is left
untouched; `root` is `Path(args.root).resolve()` at main (integrate.py:2067) so the
chdir target is absolute; the concurrency argument is that `_unload_branch` is
reached only via `integrate_one` inside `integrate()`'s `_slot` exclusive lock
(:1876, :1906-:1916, the stated one acquisition site) in a single-threaded process
(no threading imports), so the process-global chdir has no concurrent observer — the
argument holds. TOCTOU between the `ls-files` enumeration and each `unlink` (parent
swapped for a symlink mid-shed) is accepted for the same reason: serial under the
slot, same-privilege actor only, and the fail direction on any race is an OSError
caught into "left behind and re-refused". The refusal path stays byte-honest: the
orphan lane's message names `?? orphan.txt` ONLY — no shed cache name appears
(quoted in full during the drive). END-TO-END: the six measured paths verbatim →
`unloaded=True`, "unloaded wi-401 (branch deleted; GC'd clean worker worktree …)",
worker gone, branch gone, one worktree left, and no `--force` exists anywhere in
integrate.py (grepped).

Mechanical re-runs on this box (HEAD cfca0cc2): `tests/test_integrate.py` 113 passed
in 20.36s (Deliverable: 113 in 20.34s — matches); smoke 619 passed / 2 skipped in
10.74s (Deliverable stamped 615/6 at b9faefd3 — same 621 total, the same
environment-variant skip split the WI-399 review recorded); `check_trajectory
--strict` rc=0 (no WI-400 finding; residual WARNs are the pre-existing connectivity
and WI-389/390 SpecRef-clock ones); `check_doc_refs --strict` rc=0; `check_figures`
OK — 21 declared figure(s), every one carrying command and revision, the two WI-400
drain-count figures included (cmd + rev=b9faefd3 visible in the spec); size ratchet
2079 == `wc -l` 2079 with a dated, reasoned +102 stamp; ruff lint + format clean on
the three touched files. R-A: Deliverable dated (Built 2026-08-02, commit b9faefd3)
and its claims re-driven here; the 5 new tests are present and the 4-watched-red
claim is consistent (the boundaries test is the one that passes pre-implementation).
R-F: the terminal spec carries no `specref` key and strict rc=0. docs/work delta is
WI-400-only (active spec → complete/ + fragment, the exact WI-399 close-commit
shape); status.md's WI-400 token sits inside the GENERATED ready-frontier block that
regenerates at integrate, not a stale hand-written mention. The report.html exclusion
judgment IS recorded in the Deliverable (finding 2 is about its stated reason, not
its absence).

I hunted the deletion path with symlinks, tracked plants, name games and geometry
and it held everywhere the attack could occur by accident; the one breach found
(finding 1) requires an adversarially constructed ignored filename, stays fail-closed
and loud, and lives in pre-WI-400 shared code — recorded for a one-line follow-up,
not rework. Findings 2 and 3 are record-accuracy and a bounded note.

VERDICT: APPROVE findings=3
