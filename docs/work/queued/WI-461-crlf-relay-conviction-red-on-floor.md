+++
id = "WI-461"
title = "The CRLF-relay conviction is red on the declared floor: tests/test_integrate.py::test_a_whole_file_crlf_relay_in_a_claim_shape_convicts fails on Windows + Python 3.11 (the repo's own .venv) — integ._abandoned_claim returns True, the claim reads as excusable, where the WI-403 contract requires a whole-file CRLF relay to CONVICT as a real content change. Measured at the pre-sweep build commit as well as after it (log 2026-08-15n), so the 2026-08-15 sweep did not cause it; the earlier full-suite greens that included this test were produced by an interpreter the record does not name. Scope: diagnose which side is wrong on the floor interpreter — the oracle's byte-compare chain (integrate._relinked_exactly / _blob_bytes / spec_move.expected_relink) or the fixture's forged relay write — fix that side only, and record the 3.11-vs-3.13 mechanism in the fix's comment. The conviction contract itself is ruled (WI-393 REVIEW-A finding 1, WI-400, WI-403: the bytes are load-bearing at the EOL margin) and must not be weakened to green the test."
specref = "docs/log.md"
workstream = "process"
sr_refs = ["SR-156"]
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Context

Found at the 2026-08-15 sitting sweep (log `2026-08-15n`), the first full-suite
run the record can show on the repo's own `.venv` 3.11.9. The failure:

```
forged_relink_claim(root, lambda log: log.write_bytes(
    log.read_bytes().replace(b"\n", b"\r\n")))
assert not integ._abandoned_claim(root, "WI-401", "wi-401")
E   AssertionError: assert not True
```

The relay must make the claim-shaped commit read as a REAL content change
(convict), and instead it is excused. Two sibling floor defects found the same
day were 3.13-only signatures (`Path.read_text(newline=)`) and 3.13-removed
errors (`PosixPath` on Windows) — start by checking whether the oracle's
compare path has the same vintage before assuming the oracle logic itself is
wrong. `_relinked_exactly` reads both sides as raw bytes via `git cat-file`
and re-encodes `spec_move.expected_relink` — the suspect surface is anything
between those bytes and the verdict that folds or strips EOLs on one
interpreter and not the other, including the fixture helper's own writes.

Do NOT: weaken the conviction to a warn, skip the test on Windows, or "fix"
by normalizing EOLs in the compare — the compare being byte-literal is the
whole point (WI-403).
