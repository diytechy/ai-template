### REVIEW-A — WI-573 — Round 003 — 2026-09-02 — supervisor-drawn verification (independent Opus)

Verification of the round-002 rework at tip `f784b09a` (rework) over `ad395441`
(round-002 record), branch `wi-573-adjudicate-llr-136-llr-158`. Read-only: no
file but this one was written. Every claim below was re-derived from the tree,
not taken from the rework's commit message.

## What I verified

**Record-only delta — no registry, no snapshot path.** `git diff --stat
446e19ea..HEAD` touches exactly four files: the new fragment
`docs/log.d/WI-573-adjudicate-llr-136-llr-158.md` (+63), the verdict
`001-ADJUDICATE-07cbabb.md` (9 lines, the re-issued sentence), the round-002
record `002-REVIEW-A-446e19e-supervisor.md` (+145, my file, committed verbatim),
and the closed spec (+41/−14, the `## Dispositions` prose and its `title`).
`git diff --name-only 446e19ea..HEAD -- docs/requirements docs/test
docs/archive/last_approved` is EMPTY. No `Status` cell, no registry cell, no
`SNAPSHOT_DIR` file.

**Round 002 finding 1 (MAJOR) — closed, and closed correctly.** The successor's
scope no longer instructs the lane to anchor. `IN SCOPE` now reads "one cell's
last clause and one `code_symbol` cell"; the `ALSO IN SCOPE — the anchor`
paragraph is gone (`scope.count("ALSO IN SCOPE") == 0`) and is replaced by two
paragraphs I checked against the code they cite:

- *"NOT ON THIS LANE"* states the lane runs no `intake.py snapshot` **in any
  form** and writes nothing under `docs/archive/last_approved/`, citing both
  authorities correctly: the plan's §2a (the act is a trunk-side adjudication
  session's) and `lane_approval_refusal`, which does refuse on any lane delta
  touching `SNAPSHOT_DIR` (`acceptance_record.py:694`, the delta walked at
  :733-737 and the refusal worded at :745-760). The prose's warning that taking
  the anchor there "would hard-refuse this very row's merge" is exactly what the
  guard does, and the classification premise still holds — the row mints
  `safety_class = "spine"`, so `integrate._adjudication_lane` (:1120-1124) routes
  it to the lane arm.
- *"WHERE THE RE-ANCHOR HAPPENS INSTEAD"* names the route round 002 identified
  and it is mechanically real: correcting an `Approved` row's `Detail` with
  `Status` unmoved is precisely what `staged_spine_amendments` reports, so the
  amendment adjudication mints at that merge; that adjudicator is trunk-side and
  released (LLR maps to `STAGE_LLREQS` in `agent_common.SPINE_APPROVAL_RUNGS:809-813`,
  above the `human_approval_through = "DevStg-Needs"` dial at
  `docs/process.toml:116`), and the released-rung arm of
  `adjudicate-amendment.template.md` is the one it acts under. The two residual
  mentions of `intake.py snapshot`/`--approves` in the scope are the negative
  prohibition and this description of the trunk-side act — neither is an
  instruction to the lane. Correct.
- The `title` no longer asserts a lane act: "…state the shipped
  `APPROVAL_ACT_CSVS` partition in the Detail and code_symbol cells" (was
  "…then re-anchor the LLR registry"). The carried-forward whole-file paragraph
  ("`copy_live` mirrors whole registry files, so that one act also re-anchors
  `LLR-136`…") now attaches to the trunk-side act rather than the lane's, which
  is where it was always true.

**Dispositions still parse, keys still valid.** `intake.parse_dispositions`
returns refusal `None` and exactly ONE draft:
`kind=spine`, `workstream=process`, `buildtier=medium`, `priority=2`,
`bar=DevStg-Reqs`, `specref=docs/requirements/low-level-requirements.toml`, plus
the new title. Every key is one the parser recognises; nothing was dropped and no
key changed but `title`.

**Round 002 finding 3 (MINOR) — closed, and the replacement is accurate.** The
verdict's sentence now says the drift "keeps surfacing — visibly, not silently —
in the re-attestation section of `docs/ratify/CURRENT.md` and of the generated
`open-items.html` (`trace.reattest_model` feeding `gen_open_items.py`)… a
LOOP-side surface, not the owner's brief". Both surfaces exist and both are fed
as stated: `docs/ratify/CURRENT.md` is present and is the one file the live
re-attestation brief path rewrites (`trace.py:3743-3761`,
`CURRENT_APPROVAL_BRIEF`), and `docs/open-items.html` is `gen_open_items.OUT_REL`
(:96) built from `tr.reattest_model` (:855). The verdict file still ends in
exactly one machine line — `grep -c '^VERDICT: '` returns **1**, and `tail`
shows `VERDICT: MEANING rows=2` as the final line, unchanged.

**Round 002 finding 2 (MINOR) — closed; the checker accepts it.** The fragment
exists, opens with its `## 2026-09-02 — …` heading, and carries a FILE-LEVEL
declaration: `gen_open_items.fragment_declarations` returns one entry for it with
`scope: None` (line 9) and `none: True`, and `fragment_scope_findings` returns
`[]`. `python project-trajectory/scripts/gen_open_items.py --root . --check`
exits **0** ("open-items view up to date"). The `none — …` justification is true
of the session: the correction is drafted as this row's `## Dispositions`
successor and mints at merge; nothing is owner-owed, since the rung is released.

**The fragment's substantive claims match the round files and the tree.** I
checked each against its source rather than against the other narrative: the two
MEANING rulings and their evidence (`read_specs`/`spec_paths`, the
`COLUMNS`/`WI_COLUMNS` pin; `_spine_row_sides` and its four consumers); the
withhold's defect (`acceptance_record.py:144`, `:162`, `:165` — the
`APPROVAL_ACT_CSVS` walk, the pinned identity, the three-entry
`OUTSIDE_THE_APPROVAL_ACT`); the archaeology `d5b3e124` → `94b77a26`; the
twenty-five excluded rows as WI-566's and WI-547's; "no registry cell, no
`Status`, no file under `docs/archive/last_approved/`" (verified by diff at both
tips); and its account of round 002 (CHANGES-REQUESTED, three findings, the MAJOR
as stated). I found no sentence in the fragment, the verdict or the spec that
misstates a fact.

**One observation, not a finding.** The re-anchor the successor's merge mints
will take `--approves` over the whole LLR registry, so it blesses rows that
adjudicator's own brief did not show it (`LLR-136`, and the WI-566 set). That is
`copy_live`'s per-FILE granularity, not a defect in this rework — the scope says
so explicitly and the original verdict reasoned from it — and no refusal applies
(an amendment adjudication carries no `first_approval_scope`, and the delta
performs no flip, so `merge_approval_refusal` returns none). Recording it only so
the next reader is not surprised by it.

## Findings

None. All three round-002 findings are closed by corrections that are themselves
accurate, and the rework introduced no new claim I could falsify.

VERDICT: APPROVE findings=0
