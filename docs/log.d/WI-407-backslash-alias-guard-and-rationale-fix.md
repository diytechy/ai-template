## 2026-08-02 — WI-407: the backslash alias is dead; report.html is declared residue

**Summary.** WI-400 REVIEW-A findings 1–3 (minted trunk-side at intake), all
three taken. The residue double-lock's one driven breach — on POSIX,
`ignored_files`' unconditional `\`→`/` replace let a git-ignored file
literally NAMED `x\__pycache__\evil.pyc` alias onto a declared cache path,
and the shed unlinked the TRACKED `x/__pycache__/evil.pyc` the lock exists to
protect — is closed at the shared site: the normalization is gated to
`os.name == "nt"`, where backslash is a separator and never a filename byte.
`docs/test/report.html` joins `_RESIDUE_FILES` on measurement. And the
directory sweep gains the ignored lock for one guard line.

**Deliverables.**

- **The guard** (`project-trajectory/scripts/integrate.py`, `ignored_files`):
  Windows-only normalization; POSIX passes the path through untouched. git
  emits `/` on every platform, so the replace was pure defense — and both
  sheds (`_shed_declared_residue` and `_shed_residue`) consume this one
  helper, so the single gate fixes both. The reviewer's fixture is pinned
  both ways: the literal-backslash file no longer aliases (unload refuses,
  tracked twin survives byte-identical, the alias file stands as undeclared
  dirt), and the `nt` arm still normalizes — unit-pinned on BOTH platforms by
  forcing `os.name` each way over a faked `ls-files` payload.
- **The widened declaration** (finding 2's judgment, taken WITH a test):
  `check.py` passes `--html` to its trace step at G2/G3, so the declared bar
  writes `docs/test/report.html` in whatever lane it runs in, and on
  2026-08-02 the wi-402 lane was measured holding exactly that file at unload
  (station measurement, relayed at WI-407 intake) — the WI-400 scope guard's
  own rule, "widen only on measurement", satisfied on both prongs. Same
  class as the markdown report: rebuilt by the next bar run, sole-copy
  evidence never. Driven: a residue-only lane plus report.html unloads clean,
  and the same test re-pins the repo-root `out/` boundary. The path now has a
  LIFECYCLE row in `docs/declared-absences` beside the markdown report's.
- **The ignored lock, directory half** (finding 3, the one-line rider):
  `_sweep_residue_dirs` asks `git check-ignore -q` before every rmdir, so
  emptiness git does not ignore survives the sweep (the reviewer's
  `x/__pycache__/keep/` shape, fixture-pinned). Fail direction stays closed:
  a check git cannot answer skips the rmdir and the husk re-refuses loudly.

**RECORD CORRECTION, disclosed loudly.** WI-400's completed Deliverable
(`docs/work/complete/WI-400-unload-sheds-declared-tool-residue.md`) justified
the report.html exclusion with "the bar never generates it" — FALSE
(REVIEW-A finding 2: `check.py` has passed `--html` at G2/G3 since
2026-06-28), and the false reason would have misdirected the future widen
decision. The rationale sentence is amended IN PLACE to the true reason (the
2026-08-01 drain lanes ran plain `trace.py`, which writes only the markdown
report, so the measured set never showed the html one), dated 2026-08-02 and
attributed to WI-407 — the WI-394 honest-dating shape: a record correction of
a completed row, never a silent rewrite. The stale inline `path-ok` comment
(which claimed the file's "EXCLUSION from the declared set") went with it;
the absence ledger is now the one home for that fact.

**Judgment calls / deviations.** (1) The `docs/declared-absences` LIFECYCLE
row is a small scope extension beyond the spec's named files, taken because
the ledger's own header rules it: a deliberate absence belongs there, not as
a scatter of per-line `path-ok` excuses — and the correction text plus this
fragment would have needed three of them. (2) Registration Class B (the
WI-400 precedent): internals of the LLR-140/SR-132 unload, no new rows owed;
the 4 new tests land beside TC-132's evidence module and one existing data
test widened. (3) `integrate.py` size ratchet re-stamped 2103 → 2125 (+22),
reason in the baseline comment — all but four lines are docstrings/comments
recording why each guard exists.
<!-- fig: derived="len(text.splitlines()) at bddc8e67, the ratchet's own metric (tests/test_module_size_ratchet.py)" -->

**Byte budgets:** AGENTS.template.md / PROCESS.md / PROCESS_OPTIONS.md all
untouched.

**Watched, measured on the build commit bddc8e67 (clean tree):** red first —
5 failed on the pre-implementation tree, the alias test failing exactly the
reviewer's way (FileNotFoundError: the tracked twin deleted through the
mangled path), plus the unit pin's POSIX arm, the html-lane unload, the
declared-set data test and the sweep lock — then green.
`tests/test_integrate.py` 122 passed in 41.17s
<!-- fig: cmd="python -m pytest -q tests/test_integrate.py" rev=bddc8e67 -->
smoke tier 621 passed / 6 skipped in 11.48s
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=bddc8e67 -->
full suite 1887 passed / 10 skipped in 0:04:57
<!-- fig: cmd="python -m pytest -q -n auto" rev=bddc8e67 -->
`check_trajectory` / `check_doc_refs` / `check_figures` all rc=0 under
`--strict` (the residual WARNs are the pre-existing connectivity and
WI-389/390 SpecRef-clock ones); `check_docs --stale` 0 broken links.
