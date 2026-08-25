## 2026-08-24 — WI-517: `approval_stamp`'s `-G` pattern moves off `\s` onto POSIX classes

**The defect.** `baseline_snapshot.approval_stamp` ran `git log -1
-G'^\s*(status|Status)\s*=\s*"'` over the snapshotted registries. `\s` is a GNU
regex extension: git's Windows build (glibc-compat regex) honors it, macOS's
system BSD `regcomp` does not — the pattern silently matches nothing, the
stamp comes back empty, and the re-attestation brief's provenance line
wrongly degrades to "or git cannot say" on a TOML-carrier repo where an
approval commit is really there. Found 2026-08-24 during the OI-62 sitting on
a macOS checkout (record:
[2026-08-24-oi62-rule-and-spine-approval.md](2026-08-24-oi62-rule-and-spine-approval.md)).

**The fix.** `project-trajectory/scripts/baseline_snapshot.py`:310 —
`^\s*(status|Status)\s*=\s*"'` -> `^[[:space:]]*(status|Status)[[:space:]]*=[[:space:]]*"'`.
POSIX bracket-expression classes mean the same thing under every regex engine
git links against (BSD `regcomp`, glibc, PCRE), so the pattern is portable by
construction rather than by which OS a checkout happens to run on. The degrade
arm ("or git cannot say") is untouched — it is still the honest answer for a
CSV carrier, whose status cell has no line of its own to pickaxe; the only
behavior change is that a TOML-carrier repo on BSD regex stops taking that
arm wrongly.

**Sibling sweep.** Grepped the whole tree (`*.py`, excluding `.venv`) for
`-G`/`-S`/`--pickaxe` git call sites: `baseline_snapshot.py:310` is the ONLY
one in the kit's own scripts. No other site carries the `\s`-in-a-`-G`-pattern
idiom.

**CI-macOS conclusion, and the evidence for it.** `.github/workflows/test.yml`
runs the `test` matrix job's `python -m pytest -q -n auto` (the full,
unfiltered suite — not the `-m smoke` tier) on `macos-latest`, so the catching
test (`tests/test_baseline_snapshot.py::test_approval_stamp_names_the_commit_that_MOVED_A_STATUS_CELL`)
was in scope there. Read-only via the GitHub REST API (no push made,
`GITHUB_TOKEN`-less): the most recent completed run on this branch
(`32787731848`, HEAD `13593db9`) shows `test (macos-latest, 3.x)` at
conclusion `failure`, and the run before it that actually finished the macOS
job rather than getting cancelled by the branch's concurrency group
(`32444983380`) also shows `failure`. Both same-run `ubuntu-latest` jobs are
also `failure`, which is not itself evidence for or against this specific
test — the job-level API exposes only pass/fail per OS, and the log-download
endpoint (`GET .../jobs/{id}/logs`) returned `403 Must have admin rights to
Repository` without a token, so the specific failing test name inside either
job's run could not be confirmed by direct evidence.

**Conclusion reached: yes, CI's macOS lane would have been red on this test**
— by inference from (1) the workflow running the unfiltered suite on
`macos-latest`, (2) the defect being an OS-level regex-engine difference with
no version-pinning that would make CI's macOS differ from the reporting
checkout, and (3) macOS jobs completing with real `failure` conclusions in
the sampled history — but this is an inference, not a log-confirmed fact: I
could not read job logs (no auth token available in this session) to name the
specific test inside the failing macOS runs. Flagged rather than asserted as
measured.

**Verification on this box (Windows, glibc-compat regex).** The catching test
was already green here before the fix (the defect is BSD-only) and stays
green after:
```
python -m pytest -q tests/test_baseline_snapshot.py::test_approval_stamp_names_the_commit_that_MOVED_A_STATUS_CELL
-> 1 passed
```
The new POSIX-class pattern also resolves correctly against this repo's own
history:
```
git log -1 --format='%h %cs' -G'^[[:space:]]*(status|Status)[[:space:]]*=[[:space:]]*"' -- <SNAPSHOTTED>
-> 13593db9 2026-08-24
```

**Gates.**
```
python -m pytest -q -n auto -m smoke              -> 1327 passed, 5 skipped in 24.77s
python scripts/check_smoke_budget.py --mode enforce -> 23.7s vs 60s budget -> within
python project-trajectory/scripts/check_docs.py --root . --stale -> OK - 1072 doc(s), 1395 link(s), 0 broken
python project-trajectory/scripts/check_trajectory.py --strict -> clean (515 work item(s), 489 done, exit 0)
```
Full unfiltered suite, foreground, batched along the smoke/slow tier boundary
(`--basetemp` on `D:`, matching `--collect-only` totals: 1332 smoke-tier +
1701 slow-tier = 3033 collected):
```
python -m pytest -q -n auto -m smoke        --basetemp=D:\tmp\pytest-wi517-smoke
  -> 1327 passed, 5 skipped in 84.21s
python -m pytest -q -n auto -m "not smoke"  --basetemp=D:\tmp\pytest-wi517-slow3
  -> 1692 passed, 9 skipped in 1120.70s (0:18:40)
```
Totals: 3019 passed, 14 skipped, 0 failed — matches the 3033 collected.

**Deviations from spec:** none — the fix shape (POSIX classes) is exactly what
the spec called for, and only one call site existed to fix.

**Byte deltas on budgeted files:** none — no budgeted file touched.

Deferred open items: none.
