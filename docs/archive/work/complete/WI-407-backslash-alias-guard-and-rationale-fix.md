+++
id = "WI-407"
title = "Backslash-alias guard in the residue double-lock + correct the report.html rationale (WI-400 REVIEW-A findings 1-2, minted trunk-side at intake per the R3 invariant). FINDING 1, DRIVEN by the reviewer: ignored_files' replace of backslashes with forward slashes lets a git-ignored POSIX file literally NAMED x-backslash-__pycache__-backslash-evil.pyc alias to a declared residue path, and the shed then deleted a genuinely TRACKED x/__pycache__/evil.pyc (the D line is quoted in docs/reviews/WI-400-REVIEW-A.md). Non-blocking at review because it is adversarially contrived, crosses no privilege boundary, fails closed (the unload still refuses loudly), is recoverable from git, and the mangle PRE-DATES WI-400 (_shed_residue shares it) - but the fix is one line: apply the backslash normalization ONLY on Windows (os.name gate or equivalent), where backslash is a separator and never a filename byte; on POSIX pass the path through untouched. Drive the reviewer's fixture both ways: the POSIX literal-backslash file must no longer alias (shed refuses, tracked twin survives), and a real Windows-style path keeps normalizing (existing tests stay green - check _shed_residue's sharing of the helper and fix at the shared site). FINDING 2, record correction owed: WI-400's Deliverable states report.html is excluded from the residue set because the bar never generates it - FALSE: check.py passes --html at G2/G3 (check.py:449-455) and trace.py:2884 writes it; the true reason (recorded in the review) is that the drain lanes only ran plain trace.py. Amend the Deliverable's rationale sentence in docs/work/complete/WI-400-unload-sheds-declared-tool-residue.md to the true reason and, while there, JUDGE (do not silently take) whether report.html now belongs in _RESIDUE_FILES under the same double-lock - if the bar can write it in a lane, it is the same class as report.md; take it only with a test, else record why not. FINDING 3 rides along as a note: _sweep_residue_dirs applies only the name lock to now-empty dirs - bounded; add the ignored-lock there only if it costs one line. Scope: integrate.py one-line guard (+ the judged report.html line), the Deliverable rationale sentence, tests."
workstream = "scripts"
buildtier = "quick"
safety_class = "ordinary"
+++

## Deliverable

**Built 2026-08-02 (commit bddc8e67).** All three REVIEW-A findings taken.

**Finding 1 — the guard, at the shared site.** `integrate.py`'s
`ignored_files` (the one helper BOTH sheds consume, so one gate fixes both)
now applies the backslash-to-slash normalization only when
`os.name == "nt"`; on POSIX the path passes through untouched. git itself
emits `/` on every platform, so the replace was never load-bearing — and on
POSIX `\` is an ordinary filename byte, so the unconditional replace MINTED
an alias: the reviewer's driven fixture (a git-ignored file literally named
`x\__pycache__\evil.pyc` beside a force-added TRACKED
`x/__pycache__/evil.pyc`) ended with the tracked twin unlinked through the
mangled path. Re-driven both ways: on the pre-fix tree the new alias test
fails exactly the reviewer's way (FileNotFoundError on the twin — deleted);
post-fix the shed refuses loudly, the tracked twin survives byte-identical,
and the alias file itself stands as undeclared dirt. The Windows arm is
unit-pinned on both platforms by forcing `os.name` each way over a faked
`ls-files` payload, so POSIX CI drives the `nt` arm and Windows CI drives
the POSIX arm.

**Finding 2 — the judgment, taken WITH a test.** `docs/test/report.html`
joins `_RESIDUE_FILES` under the same double-lock. Grounds: the declared
bar CAN write it in a lane (`check.py` passes `--html` to its trace step at
G2/G3), and on 2026-08-02 the wi-402 lane was measured holding exactly that
file at unload (station measurement, relayed at WI-407 intake) — so the
WI-400 scope guard's own widening rule, "only on measurement", is
satisfied, and the file is the same class as the markdown report: rebuilt
by the next bar run, sole-copy evidence never. Driven: a residue-only lane
plus report.html unloads clean through the integrator's arm, and the same
test re-pins the repo-root `out/` boundary (the refresh-refused log outside
the lane survives untouched). The absence ledger (`docs/declared-absences`)
carries the path beside the markdown report's row (LIFECYCLE), so prose may
name it without per-line excuses.

**The record correction, disclosed loudly:** WI-400's completed Deliverable
justified the exclusion with "the bar never generates it" — FALSE, and a
false reason would have misdirected the future widen decision. The
rationale sentence in
`docs/work/complete/WI-400-unload-sheds-declared-tool-residue.md` is
amended IN PLACE to the true reason (the 2026-08-01 drain lanes ran plain
`trace.py`, which writes only the markdown report, so the measured set
never showed the html one), with the correction dated 2026-08-02 and
attributed to WI-407/REVIEW-A finding 2 — the WI-394 honest-dating shape: a
record correction of a completed row's Deliverable, never a silent rewrite.
The decision the record captured (enumerate only the measured set) stood;
only its stated reason was wrong.

**Finding 3 — the one-line rider, taken.** `_sweep_residue_dirs` now
carries the ignored lock too: `git check-ignore -q` must claim a candidate
directory before it is rmdir'd, so an empty untracked `x/__pycache__/keep/`
in a repo whose rules do not ignore `__pycache__` survives the sweep
(emptiness can be load-bearing). One guard line; the fail direction stays
closed — a check git cannot answer skips the rmdir, and an ignored husk
left behind re-refuses loudly.

Registration judgment (Class B, the WI-400 precedent): internals of the
LLR-140/SR-132 unload, no new rows owed; the 4 new tests land beside that
row's evidence module (`tests/test_integrate.py`, TC-132) and one existing
data test widened. `integrate.py` size ratchet re-stamped 2103 → 2125 with
the reason in the baseline comment. Watched red first on the
pre-implementation tree — 5 failed (the alias test on the deleted twin, the
unit pin's POSIX arm, the html-lane unload, the declared-set data test, the
sweep lock) — then green. Totals on the build commit, 2026-08-02:
`tests/test_integrate.py` 122 passed in 41.17s, smoke tier 621 passed / 6
skipped in 11.48s, full suite 1887 passed / 10 skipped in 0:04:57.
<!-- fig: cmd="python -m pytest -q tests/test_integrate.py" rev=bddc8e67 -->
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=bddc8e67 -->
<!-- fig: cmd="python -m pytest -q -n auto" rev=bddc8e67 -->
Session record: the log fragment `docs/log.d/` (compiled into `docs/log.md`
at merge).
