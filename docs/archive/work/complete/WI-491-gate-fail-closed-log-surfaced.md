+++
id = "WI-491"
title = "Align the subagent gate's present-but-unparseable arm fail-closed and surface the fail-open log in the session banner (OI-46 ruled (1a)+(2a), 2026-08-20)"
specref = ""
workstream = "scripts"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

Executed both ruled halves in one commit (`f3cb9801`), plus a RESYNC entry.

**(1a) The parse asymmetry aligns.** `subagent_gate.read_process_policy`
gains a new `UNPARSEABLE` sentinel (a plain `object()`, never a `str`, so it
can never collide with a real — however garbled — policy token) returned when
`docs/process.toml` is PRESENT but does not parse/read. `decide()` gives it
its own branch resolving to `ask` (fail-closed), and `main()` treats it as
terminal — not a `None` — so a broken `process.toml` no longer falls through
to the legacy `docs/subagent-gate` file. Genuine absence is untouched (still
`None` → still falls through → still `allow`, the ruled opt-in posture), and
the tool-error/malformed-payload fail-open arm in `main()`'s outer
`try/except` is untouched (SN-006's relaxed posture keeps it). Aligned
against the concrete, tested precedent — `tests/test_rule_sync.py`'s D-7 pin
of `check_trajectory.py`/`gen_okf.py`, which have always read the same state
as ON rather than undeclared — rather than the ruling's own looser prose
("the hook's grep reader, the loop's tomllib reader"); see the adjacent
finding banked below on that naming gap. The module header, `decide()`'s and
`read_process_policy`'s docstrings, and the module-level constants comment
all updated to state the new behavior, not just the code.

**(2a) The fail-open log becomes auditable.** `agent_loop.py` gains
`_subagent_gate_log_count(root)` (a plain line count of
`out/subagent-gate.log`, 0 if absent/unreadable) and `print_run_banner` now
prints a `subagent-gate: N decision(s) recorded …` line whenever that count
is non-zero — silent on the common case (the gate never fired), so the
banner does not grow noise for every repo that never enabled the dial. The
helper reads the LITERAL filename rather than importing `subagent_gate` for
its `LOG_NAME` constant: a first pass did import it, but that created a new
`CMP-008 -> CMP-007` cross-component edge with no declared `IF-###` seam —
`check_trajectory.py --strict` caught it as a real ERROR (not a WARN), and
declaring a seam for one shared string constant would have widened this
row past its ruled scope. The literal is pinned against the constant it
mirrors by a new drift-guard test
(`test_subagent_gate_log_filename_matches_the_writer`), so a rename on
either side reds a test instead of drifting silently.

**Tests.** `tests/test_subagent_gate.py`'s two M-13 corruption tests rewired
for the new reading: `test_corrupt_process_toml_reads_unparseable_not_undeclared`
now asserts `UNPARSEABLE` + `ask`, and
`test_corruption_no_longer_falls_through_to_the_legacy_file` (renamed from
"…falls through…", since that is now exactly backwards) asserts the corrupt
file's `ask` wins over the legacy file's `deny` — corruption is terminal, not
deferred. `tests/test_rule_sync.py`'s D-7 pin
(`test_the_subagent_copy_diverges_only_where_its_module_says_it_does`,
renamed `…now_agrees_in_direction_with_its_twins`) now guards the aligned
direction instead of the retired divergence. `tests/test_agent_loop.py`
gains three tests: the log populated (count surfaced), the log absent (no
line, no noise), and the filename drift guard above.

**Ratchet.** `agent_loop.py`'s module-size baseline re-stamped 3202 → 3231
(+29: the log-count helper — including its longer docstring explaining the
literal-not-import choice — and the banner line) with the reason inline in
`tests/test_module_size_ratchet.py`, per the standing never-revert-a-real-edit
rule. `subagent_gate.py` grew to 261 lines, well under the 1500-line ratchet
threshold — no baseline entry needed.

**RESYNC entry.** `project-trajectory/RESYNC_PACK.md` §4 gained an entry
(`[since f3cb9801]`) naming both kit-owned files, the behavior change (a
present-but-broken `process.toml` now defers spawns instead of silently
allowing them when the dial is opted in), and the new banner line.

**Verified against a real scaffold, not just the unit suite.** Bootstrapped
a fresh scaffold (`bootstrap.py --dest <tmp> --agents claude`) and drove
`scripts/subagent_gate.py` as the real `PreToolUse` hook would (JSON
`{"tool_name": "Task"}` on stdin, `CLAUDE_PROJECT_DIR` set to the scaffold):
(1) a syntactically-broken `docs/process.toml`
(`"[checks\nsubagent_gate = \"deny\"\n"`) → `permissionDecision: "ask"`, exit
0 (never 2 — `ask` is not `deny`), logged with the new "present but did not
parse" reason text; (2) the same broken `process.toml` PLUS a legacy
`docs/subagent-gate` file set to `deny` → still `ask` — the corrupt file does
not fall through to the legacy dial in the real scaffold either; (3) both
files removed (genuine absence) → back to `allow` ("gate off"), confirming
the ruled opt-in posture survives untouched. `out/subagent-gate.log`
accumulated the three decisions across the run, and a direct call to the new
`agent_loop._subagent_gate_log_count(scaffold_root)` against that same real
log file read back `3` — the banner's reader, exercised against a real
scaffold's on-disk log, not a synthetic fixture.

**Gates.** Line endings checked before trusting any count
(`git ls-files --eol | grep 'w/crlf'`): none of this session's touched files
are new entries in the pre-existing CRLF residue list.

- smoke (final, post-restamp): `1278 passed, 5 skipped in 57.60s`
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=70b43f50 -->
  (An earlier run against the code commit alone, before the import was
  swapped for a literal, read `1278 passed, 5 skipped in 58.08s` —
  byte-identical count, confirming the swap changed no test collection.)
- `check_docs.py --root . --stale`: `OK - 961 doc(s), 1335 intra-repo link(s),
  0 broken (1 orphan warning(s))` — unchanged from the WI-490 baseline (no
  doc added or removed).
- `check_trajectory.py --root . --strict`: **first run, against the initial
  `agent_loop → subagent_gate` sibling import, caught a real ERROR** — a
  cross-component seam (`CMP-008 -> CMP-007`) with no declared `IF-###` row,
  never merely advisory under `--strict`. Fixed by dropping the import for a
  pinned literal (see (2a) above) rather than minting a registry row, which
  would have widened this row past OI-46's ruled scope. Final run: `clean
  (490 work item(s), 460 done (94%), 21 cancelled, graph acyclic)` — 459 → 460
  is exactly this row's own close.
- **full unfiltered suite, run to completion in the FOREGROUND**: `2726
  passed, 14 skipped in 500.96s (0:08:20)`, exit 0
  <!-- fig: cmd="python -m pytest -q -n auto" rev=70b43f50 -->
  2723 (the WI-490 close's own total) → 2726 is exactly this session's three
  net-new tests (the two banner tests plus the filename drift guard); the
  four renamed M-13/D-7 tests each replaced an existing one, so they add no
  count. (An interim run mid-session, taken while the import-vs-literal
  question above was still open, read `2725 passed, 14 skipped in 503.88s` —
  +2, the two banner tests before the drift-guard test existed; superseded by
  the total above.)

Deferred open items: none — OI-46 is fully executed by this row; no new
open item surfaced. (The Hat-Refs/OI-48 mechanism note in `docs/status.md`
is a different lane's residue, untouched here.)

## Context

Executes OI-46's ruling — (1a) + (2a) as recommended, both halves in this
one WI.

- **(1a) The parse asymmetry aligns.** `subagent_gate.py` currently maps an
  unreadable OR unparseable `docs/process.toml` to undeclared-therefore-
  allow, while its two twin readers (the hook's grep reader, the loop's
  tomllib reader) read a PRESENT-but-broken file as fail-closed. After this
  WI: present-but-unparseable = ask/hold (fail-closed), ABSENCE stays allow
  — the ruled opt-in posture is untouched, and the change can only NARROW
  the fail-open window. The tool-error fail-open arm stays (SN-006's
  relaxed posture keeps it).
- **(2a) The fail-open log becomes auditable.** Every allow-on-error
  appends to `out/subagent-gate.log` and nothing reads it. After this WI
  the session banner surfaces its tail count, and a test pins that the
  surface exists — the cheapest form in which the record becomes a record.
- **Tests:** WI-477's M-13 contract tests pin the CURRENT divergence
  honestly; extend them to pin the new fail-closed arm and the banner
  count. Three readers, one answer, one test surface.
- **RESYNC entry owed:** this is a behavior change in shipped supervision
  machinery (the gate holds where it used to allow, on a corrupted policy
  file).
