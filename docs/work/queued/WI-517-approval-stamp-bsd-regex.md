+++
id = "WI-517"
title = "approval_stamp's -G regex uses \\s, silently empty on BSD regcomp — the provenance line reads 'git cannot say' on macOS"
specref = "tests/test_baseline_snapshot.py"
workstream = "tooling"
needs = []
buildtier = "quick"
safety_class = "ordinary"
priority = 3
+++

## Deliverable


## Context

Found 2026-08-24, during the OI-62 sitting, on a macOS checkout (record:
[../../log.d/2026-08-24-oi62-rule-and-spine-approval.md](../../log.d/2026-08-24-oi62-rule-and-spine-approval.md)).
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
