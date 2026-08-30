+++
id = "WI-517"
title = "approval_stamp's -G regex uses \\s, silently empty on BSD regcomp — the provenance line reads 'git cannot say' on macOS"
specref = ""
workstream = "tooling"
needs = []
buildtier = "quick"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

`baseline_snapshot.approval_stamp`'s `-G` pattern moved from `\s` (a GNU regex
extension BSD `regcomp` silently ignores) onto POSIX `[[:space:]]` classes,
which mean the same thing under every regex engine git links against. Sweep
of the whole tree (`*.py`, excluding `.venv`) for `-G`/`-S`/`--pickaxe` call
sites found exactly one: `baseline_snapshot.py:310`, now fixed — no siblings
existed. Record:
[../../../log.d/2026-08-24-wi517-approval-stamp-bsd-regex.md](../../../log.md#2026-08-24--wi-517-s--pattern-moves-off--onto-posix-classes).

**CI-macOS open question, answered:** yes, inferred red on that test —
`.github/workflows/test.yml`'s `test` matrix job runs the full unfiltered
`pytest -q -n auto` (not `-m smoke`) on `macos-latest`, and read-only GitHub
API history shows the macOS job completing with a real `failure` conclusion
on two sampled runs. The specific failing test name inside those jobs could
not be confirmed directly — the job-logs endpoint returned `403` without an
auth token this session did not have — so this is evidence-based inference,
not a log-read fact; the log fragment states exactly what is direct evidence
versus inference.

## Context

Found 2026-08-24, during the OI-62 sitting, on a macOS checkout (record:
[../../../log.d/2026-08-24-oi62-rule-and-spine-approval.md](../../../log.md#2026-08-24--oi-62-ruled-e-and-the-nineteen-are-approved-from-the-corrected-brief)).
`baseline_snapshot.approval_stamp` runs `git log -1 -G'^\s*(status|Status)\s*=\s*"'`
over the snapshotted registries. `\s` is a GNU-regex extension: git's Windows
build (glibc compat regex) honors it, while macOS's system BSD `regcomp` does
not — the pattern silently matches nothing, `approval_stamp` returns the empty
stamp, and the re-attestation brief's provenance line degrades to *"no commit
in this checkout moved a `Status` cell in a snapshotted registry (or git cannot
say)"* on a tree where `git log -1 -G'^[[:space:]]*(status|Status)[[:space:]]*=[[:space:]]*"'`
names `2b7be11a` — measured both ways on the same checkout, same HEAD. One
machine is one data point: this is a Darwin observation; Linux (glibc) likely
matches Windows, unverified.

**The fix shape:** POSIX character classes (`[[:space:]]`) in the `-G` pattern,
which mean the same thing on every regex engine git links against. Check the
tree for sibling `-G`/`-S`/`--pickaxe` call sites with the same idiom while
there. **The test that catches it ALREADY EXISTS and is RED on this machine:**
`tests/test_baseline_snapshot.py::test_approval_stamp_names_the_commit_that_MOVED_A_STATUS_CELL`
fails here (`assert seeded` → `assert ''`) — it drives `approval_stamp`
against a fixture repo exactly as designed, and the empty stamp IS the
defect firing, not test rot. The full unfiltered suite on this Mac reads
3003 passed / **1 failed** on precisely this test. Open question for the
executor: `.github/workflows/test.yml` runs macOS — establish whether CI's
macOS lane is red on it too (expected: yes, same BSD regcomp) or whether
something in the runner differs, and say which in the close.

**Not a behavior change:** the degrade arm ("or git cannot say") stays — it is
the honest CSV-carrier answer; the fix is only that TOML-carrier repos on BSD
regex stop taking that arm wrongly.
