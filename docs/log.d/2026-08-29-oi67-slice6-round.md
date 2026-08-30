## 2026-08-29 — review: the OI-67 slice-6 cross-family round — eleven findings, nine folded at the root

Deferred open items: none — the two decisions this round forced (6.7, 6.8)
are filed for review in
[../decisions-for-review-2026-08-29-slices-4-6.md](../decisions-for-review-2026-08-29-slices-4-6.md),
not as rulings owed.

**First act — the smoke budget re-measured, still not on a quiet box:**
`check_smoke_budget.py --mode enforce` read **112.7 s vs 60 s → OVER** at
`8599f2b0` (1348 passed, 30 skipped — 24 posix-shell-gated under a PowerShell
PATH without `sh.exe`), with the box at 52–54 % from three other sessions'
`claude`/`codex` processes; recorded, not waived, the budget not moved, the
quiet re-measure still owed.
<!-- fig: cmd="python scripts/check_smoke_budget.py --mode enforce" rev=8599f2b0 -->

**Summary.** The round the WI-533 close owed ran: the slice-4 adversarial
prompt re-targeted at the slice-6 build (prompt, raw verdict and dispositions
at [../reviews/2026-08-29-oi67-slice6/](../reviews/2026-08-29-oi67-slice6/README.md)),
gpt-5.6-sol at medium effort, read-only in a worktree at `8599f2b0`:
`VERDICT: CHANGES-REQUESTED findings=11` — one CRITICAL, seven MAJOR, three
MINOR. Every finding was reproduced before it was acted on; nine are folded
here, two kept on record with reasons.

**What was wrong, and the root causes.** (1) CRITICAL — one malformed body
disarmed the whole definition gate: `_declaration_sites` caught the
harvester's grammar error and returned "no surface", so an empty
`Contract IF-069:` opener passed `check_trajectory --strict` (exit 0, output
byte-identical to a clean tree). `gen_arch_map.scan_contracts` now takes an
opt-in `grammar_errors` list — one refusal per source, the walk continues —
and the gate emits its FOURTH shape, "declares seams but its header is refused
by the contract grammar", at the same severity; the reference generator's
path still raises. (2) A row owned by an external party whose far side is all
external owed no body anywhere: `trace.interface_findings` fails a row with
no in-tree endpoint (decision 6.8). (3) "Every kit reader goes through" the
one CSV reader was false by three sites — `agent_route._rows_from_csv`,
`intake._locate_spine_rows`' legacy carrier read, and `spine_carrier.columns`
(the CSV-carrier reader WI-533 missed) — plus an unused fourth
(`check_flows.col`), routed or deleted, and a census test now holds the claim:
every `csv.reader`/`DictReader` call under the kit carries `csv_body` on its
line, `migrate_carrier` the one argued exception. (4) `csv_body` kept a blank
line after the comment block, which `DictReader` took as the header — blank
lines are preamble now. (5) The retired-cell rule read VALUES per row where
the retired shape is a KEY's presence in the registry: a legacy CSV header
still declaring `Contract` was silent while its cells were empty, and a test
pinned that as correct; `_retired_cell_findings` reads `spine_carrier.columns`
— one finding per retired key naming its rows, or the header column. (The
reviewer's `provider = ""` and nested-table plants were in fact refused by the
carrier on stderr; pinned by tests as the mechanism that owns them.)
(6) `gen_okf._doc_title_and_summary` dropped the text after a comment's `-->`
on the same line — comment spans are stripped and the remainder read.
(7) Six shipped and live texts said an owner that declares nothing is a
strict finding, where decision 6.2 keeps it a warn: the registry header, the
template header, `INTERFACES.template.md`, `PROCESS.md` §8, the RESYNC entry
and `docs/enforcement-audit.md` now say warn, and name the fourth shape.
(8) `EXAMPLE.md` §9 and §10 still taught `provider`/`contract`/`req_refs`
rows with an SR-id owner — rewritten to the ruled shape: the header body
beside the code, the TC citing the seam, and the coordinator rows as
`external:`-owned rows with an in-tree far side. (9) The WI-533 fragment's
"sixteen reason cells" reads fourteen when derived (the prompt had
mis-located the cells; the record now carries the derivation).

**Kept on record.** The harness promotes `check_trajectory` to `--strict`
only at `DevStg-Impl`, so on this `DevStg-LLReqs` tree the gate errors when
run by hand — decision 6.7 keeps the ladder (header-first makes "declared,
not stated" a sanctioned transient; the reference freshness step is the floor
that catches a deleted or malformed body today). `trace --strict`'s three
standing reds (`SR-181`'s orphan pair, `LLR-197`) predate the program and are
named in the WI-531 record.

**Ratchets.** `trace.py` 5912 → 5998 (`_far_endpoints`,
`_retired_cell_findings`; `_cell_present` deleted), `check_trajectory.py`
4638 → 4653, `gen_arch_map.py` 2193 → 2223, `intake.py` 1977 → 1984;
complexity: `gen_okf._doc_title_and_summary` 18 → 14 and
`trace.interface_findings`'s entry deleted (both DOWN, re-stamped as that
file requires), `gen_arch_map.scan_contracts` kept under the limit by
extracting `_grammar_refusal`. The smoke membership stamp holds (1383
collected against 1390).

**Downstream, stated in the RESYNC entry:** an un-migrated `interfaces.csv`
whose header still declares a retired column now reds `trace --strict` until
the column is deleted.

**Deviations from spec:** none — a correction commit; the arms worklist
starts in the next commit as `WI-534`.

**Byte deltas on budgeted files:** `PROCESS.md` +54 (87,782 → 87,836;
watched, flagged in the guard's table); `AGENTS.template.md` untouched; the
guard skill 4,792 → 4,795 (cap 5,000).

**pytest totals:** the two fix workers' targeted runs: 188 passed, 1 skipped
(`test_trajectory_arch` + `test_trace`); 139 passed (the reader, route, okf,
intake, carrier and flows units); 109, 144 (+1 skipped) and 76 over the
consumers of `columns()` / `agent_route` and the import layers; the
coordinator's 196 passed, 1 skipped over the ratchets, dogfood sync, byte
caps and the touched units; the smoke tier under Git Bash **1377 passed, 6
skipped in 102.82 s** — the budget read **103.5 s vs 60 s → OVER** (123.6 s
under PowerShell with 24 posix-gated skips) on a box at 57–63 % from other
sessions' processes: environmental, recorded, not waived.
`check_trajectory --strict`: exit 0; `trace --strict`: the three standing
reds only, `interface-findings=0`; `check_docs --stale`: 0 broken; both
generated references current under the kit's scan root. The full unfiltered
suite runs on this tree after the commit; its totals are recorded at the
`WI-534` close.
