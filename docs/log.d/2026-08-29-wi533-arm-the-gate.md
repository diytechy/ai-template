## 2026-08-29 — WI-533: the gate is armed (OI-67 slice 6)

Deferred open items: none — the decisions this slice took alone are filed for
review in [../decisions-for-review-2026-08-29-slices-4-6.md](../decisions-for-review-2026-08-29-slices-4-6.md)
§6, and the split's own cross-family round is dispositioned in
[../reviews/2026-08-29-oi67-slice4/README.md](../reviews/2026-08-29-oi67-slice4/README.md);
this slice's own cross-family round is OWED (below), not deferred.

**Summary.** The definition gate is armed and the program's shape is whole:
**every one of the 154 rows is stated** — the reference reads **74 sources
declare 154 seams; 154 carry a stated contract** — and the tree that state
rests on is enforced rather than claimed. `check_trajectory --strict` fails a
row its owner declares but does not state, an `external:`-owned row no
far-side kit module states, and a source declaring another owner's row;
`trace.py --strict` fails a row still carrying any of the five retired cells
(`contract` included — the legacy advisory is gone); the four rows slice 3
could not place are placed.

**The four legacy rows, placed.** `IF-031`'s owner
(`performance-budgets.csv`) declares in its own `#` header, because the kit
now has ONE comment-skipping CSV reader — `kitlib.spine.csv_body` /
`csv_reader` / `csv_rows` — and every kit reader goes through it:
`load_csv`, `check_perf.load_budgets`, `gen_release_checklist.load_csv`,
`wi_convert.load_csv` (its header check now sees the real header),
`spine_carrier`'s two CSV-carrier readers, `migrate_carrier`'s legacy source
read, `check_trajectory.read_rows`, `gen_okf.read_rows`, `schedule.load_rows`,
`agent_common._read_csv_rows`, `plan_artifacts`' id scan, and
`trace.structure_findings` — the raw-line column counter that would otherwise
have read the header's sixteen comment lines as ten one-column rows against a
one-column "header" (found when the header landed; the reported line number
still counts the file's own lines). The three `external:`-owned rows are
stated by their FAR SIDE — **the rule this slice sets:** an external party's
header is not ours to write, so our READING of its surface lives in the header
of the kit module that faces it (`IF-032` in `check_privacy`, `IF-036` in
`check_vendored`, `IF-041` in `agent_session`), and a module that is not the
far side may not state it.

**The gate.** `check_trajectory.contract_body_findings` — WARN plain, ERROR
under `--strict`, the seam-TC promotion's idiom and its `[checks]
interfaces_check` opt-out, vacuous in files-mode or with no scan root: one
rule, three shapes (declared-not-stated; an external-owned row no far-side
module states; a stray declaration on a source that is not the owner). **What
stays a warn, on record:** an owner that declares NOTHING is the owner-exact
reverse check's warn, not the gate's error — the ruled rule is "a DECLARED
seam with no body", and promoting the undeclared case reds every fixture and
adopter row whose owner has not been headed at all (the migration list, not a
defect in a stated definition). The dodge that leaves — never declare, never
owe a body — is visible in that warn and in the reference's summary line, and
is the owner's to promote (decision 6.2). Retired cells are
`trace.interface_findings`' strict findings, both spellings (a carrier that
still maps the column, one that hands the key back as itself); `contract`
left `kitlib.spine.SPINE_TIER_KEYS`, the carrier map, the template, the
INTERFACES table, `PROCESS.md` §8 and the OKF description fallback; the
converter reports every row still carrying it and never drops the cell.
Proved by tests on scaffolds and by planting on the kit's own tree (a
`contract` cell on `IF-069` reds `trace --strict`; `IF-069`'s body deleted
from `check_coverage` reds `check_trajectory --strict`; both restored
byte-exact).

**Also closed.** `gen_okf._doc_title_and_summary` skips a leading HTML
comment WHOLE (slice 3's latent defect, live for `docs/status.md` since slice
4 — a seam definition was one dial away from becoming a process-guide
summary); sixteen half-moot reason cells trimmed by a worker (the ownership
and nearest-seam arguments the owner-as-path made moot; the honesty valves and
the measured reader sets kept; zero IF citation-frame warnings remain); the
slice-4 Sol round's six cheap findings applied (`IF-159`/`IF-160` bodies made
true, `IF-102`'s `rows_seq_from_text` clause removed — it is `IF-119`'s —
`IF-163` narrowed to the hand-authored bytes so it no longer overlaps
`IF-164`, the README exemption case-folded, the fragment's count corrected
to nine).

**Ratchets.** `check_trajectory.py` +158 (4480 → 4638, the gate and its
docstring), `trace.py` +14 net (5898 → 5912; the legacy advisory's 19 lines
deleted), `agent_common.py` +1; `kitlib/spine.py` 676 (under threshold).
`PROCESS.md` **+131** bytes (87,651 → 87,782), flagged in the byte-budget
guard's table.

**Owed, stated.** (1) This slice's own cross-family adversarial round has NOT
run — the sitting closed at the commit bar plus the full suite; the prompt
to run is the slice-4 one re-targeted (`docs/reviews/2026-08-29-oi67-slice4/PROMPT-ADVERSARIAL.md`,
the build list swapped for this fragment's), and the slice-4 round's five
deferred findings ride with it: `IF-156`'s deletion arm (trunk_step deletes
each compiled fragment — a requestor row to mint), `IF-020`'s stdout JSON and
log-file kinds (two rows to mint), three tracked fragments that open with `#`
or `###` and would refuse `trunk_step --compile-log` (the trunk lane's, not a
row's), `TC-161`'s approved `method` prose naming `IF-127` (the owner's).
(2) The arms slice 4 surfaced stay the next worklist (`derive_stage --check`'s
exit code, `schedule.py`'s CLI, `integrate`'s in-process surface,
`report.html` / `perf-report.md`), and `gen_arch_map.py` still processes only
the first of `--cli-doc` / `--contracts-doc` on one invocation.

**Deviations from spec:** the undeclared-owner case stays a warn (above, with
the reason); the `gen_okf` fix and the slice-4 verdict corrections were folded
into this slice rather than filed — each was a few lines with a test, and a
correction the verdict demanded costs a round either way.

**Byte deltas on budgeted files:** `PROCESS.md` +131 (watched, flagged);
`AGENTS.template.md` untouched.

**pytest totals:** full suite `python -m pytest -q -n auto`: 3086 passed, 15 skipped, 6 failed in 2321.98s (0:38:41) on a box other sessions held at 60-76% CPU — all six were bookkeeping the build owed and each was fixed at its root and re-run green: the C901 census (the gate decomposed into two helpers, 18 -> 11, and three reviewed entries), the byte-budget guard's own 5,000-byte cap (a row shortened, the skill's row re-stamped at 4,792), the converter's writer map still carrying `Contract` (dropped, the reader's inverse), the smoke membership stamp (1377 -> 1390, eleven in-process tests joined the tier), and the forward-only guard (two closed ids scrubbed from status.md prose); smoke tier: 1372 passed, 6 skipped. **The smoke budget read OVER at close — 85.8 s against 60 s — on the same loaded box (14 other-session processes, 60-76% CPU) that read 23.3 s at this session's first act; recorded, not waived, the budget not moved, the quiet re-measure owed.** `check_trajectory --strict`: 0 errors; `trace --strict-integrity`: integrity=0; `check_docs --stale`: 0 broken; every freshness check current; the planted violations fire (above).
