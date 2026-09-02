### REVIEW-A — WI-569 + WI-575 — Round 003 — 2026-09-02 — supervisor-drawn verification (independent Opus)

**Subject:** the round-002 rework, `git diff 4566ca27..9f8cab1a` (2 commits;
`368703d5` lands round 002 itself, `9f8cab1a` is the rework: 4 files,
+78/−8 excluding the round file). Round 002's finding 3 is treated as
pending-by-design, per the coordinator: the rollup that makes its citation true
is compiled immediately after this round. Read-only; nothing but this file was
written.

## What I verified

**Finding 1 — CLOSED, driven.** The declaration now opens the top matter at
line 3, above the first `### ` heading (line 17), and carries no `OI-78` token:
`Deferred open items: none — nothing in this fragment is owed to the owner; …`.
```
$ .venv/bin/python project-trajectory/scripts/gen_open_items.py --root . --check
gen_open_items: docs/open-items.html STALE — run `python scripts/gen_open_items.py`
```
That is the ONLY line, and it is the pre-existing trunk advisory I isolated in
round 002 by re-running the check on a `git archive` of the base — both
lane-introduced findings (the per-section one and the `declares OI-78 deferred,
but that row reads 'ruled'` one) are gone. The exit code is still 1, on the
trunk-owned stale surface alone, exactly as at the base. The rework also added a
FIFTH `### ` section and the declaration still speaks for the file, so the widen
was real and not an artifact of section count. `WI-575`'s fragment is unchanged
and still declares at line 3.

**Finding 2 — CLOSED, and the re-tensed sentence is true cell-for-cell.**
Loading `low-level-requirements.toml` and `test-cases.toml` out of each of
`b8d57e9f`, `2f660cb7` and `9f8cab1a` with `tomllib` and diffing the four rows:
```
vs b8d57e9f at 2f660cb7ad59 : LLR-203 IDENTICAL  LLR-204 IDENTICAL  TC-199 IDENTICAL  TC-200 IDENTICAL
vs b8d57e9f at 9f8cab1a     : LLR-203 ['detail','rationale','title']  LLR-204 ['detail']
                              TC-199 IDENTICAL  TC-200 IDENTICAL
status at all three revs    : LLR-203 Approved  LLR-204 Approved  TC-199 Drafted  TC-200 Drafted
```
Every clause of the replacement matches: "at the lane base `2f660cb7` all four
rows WERE cell-for-cell identical", the named drift cells (`title`, `detail`,
`rationale` on LLR-203; `detail` on LLR-204), the attribution to `33aee707`,
"`TC-199`/`TC-200` are still identical to `b8d57e9f` at the tip", and "`status`
unmoved on all four". Nothing overstated.

**MINOR (grammar) — CLOSED, matches the parser's literal.**
```
CELL:   one `<source> — <reason>` row per kit-only file, the separator a literal spaced
        EM DASH the parser partitions on — a hyphen row is silently skipped, excludes
        nothing, and its source resurfaces as a gate-class missing-file finding.
PARSER: bootstrap._mapping_source_exclusions -> raw.partition(" — ")      (bootstrap.py:2335)
CARRIER HEADER: "# One `<source> — <reason>` per line."
cell contains the exact parser literal ' — ' : True
```
The consequence is stated correctly too: the parser's guard is
`if sep and source.strip() and reason.strip()`, so a hyphen row yields no `sep`,
excludes nothing, and the source falls to `_delivery_source_findings`'
`missing_file`, which `MAPPING_FINDING_POLICY` grades `gate`.

**The constraint, re-driven at the new tip.**
```
>>> acceptance_record.lane_approval_refusal('.', '2f660cb7ad59', '9f8cab1a')   -> None
>>> acceptance_record.approval_delta(...)                                      -> ([], [], None)
>>> acceptance_record.merge_approval_refusal('.', base, '9f8cab1a', [], False) -> None
>>> staged_spine_amendments -> LLR-158, LLR-203, LLR-204   |   staged_drafted_rows -> []
```
No act, no snapshot file, no `Status` moved — so the new Deliverable paragraph's
"no `Status` moved on this lane and nothing under the snapshot was written, so
that judgement is unprejudiced" is true, and the rework's own "No `status` cell
moved, no `intake.py snapshot` ran, nothing under `docs/archive/last_approved/`
was written" is true.

**No citation frame in a spine cell.** Regexing `WI-###`/`OI-###`/`D-#` over
`title`/`detail`/`rationale`/`code_symbol` of all three amended rows
(`LLR-158`, `LLR-203`, `LLR-204`) returns nothing; `trace.py --strict-integrity`
still reports `provenance-findings=1`, the pre-existing LLR-197 finding.

**Records and bar at `9f8cab1a`.** `## Deliverable` precedes `## Context` in
both closed specs (WI-569 14/97, WI-575 12/58) and `specref = ""` in both.
`docs/ratify/CURRENT.md` regenerated to a scratch path with `trace.py --approve
modified --out <scratch>` diffs EMPTY against the committed file.
```
$ .venv/bin/python -m pytest -q -n auto -m smoke      1463 passed, 4 skipped in 21.96s
$ check_docs.py --root . --stale                      OK - 1235 doc(s), 1595 link(s), 0 broken
$ check_trajectory.py --root .                        clean (574 work item(s), 531 done (93%) …)
$ trace.py --root . --strict-integrity                integrity=0 … provenance-findings=1
```

## Findings

- [MAJOR] docs/log.d/WI-569-wi508-spine-reseal.md:149,187 -> the new Rework section misstates its own scope in two places: "Three of the five findings were reworked in-lane", and "Finding 5 asks for one sentence in the Deliverable recording the scope extension knowingly; it is not in this rework's scope" -> FOUR were reworked, and finding 5 among them: the same commit `9f8cab1a` adds `docs/archive/work/complete/WI-569-wi-508-spine-reseal-one-clean.md:16-26`, the paragraph "**A third act, taken knowingly.** … Amending two `Approved` rows is a third, recorded here rather than left implicit …", which is finding 5's remedy verbatim in substance — so the fragment and the Deliverable it describes contradict each other inside one commit, and a reader auditing which findings were answered gets the wrong answer from the log -> change the count to four, replace the closing paragraph's finding-5 sentence with the disposition that actually happened (recorded in the Deliverable, naming the paragraph), and keep the finding-3 sentence as it stands; no guard is proposed because a hand-written rework tally is prose about a diff and nothing can derive it — the durable habit is to write the tally last, from the staged diff, rather than from the plan -> WI-569 close, before merge.

VERDICT: CHANGES-REQUESTED findings=1
