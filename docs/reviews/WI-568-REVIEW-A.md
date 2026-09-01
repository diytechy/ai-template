# WI-568 — REVIEW-A rollup

Compiled by the supervising session (2026-09-01) from the round files under
`docs/reviews/wi-568-dispose-the-close-recorded-at/`, time-ordered, governing
line last. One round was mechanized (Terra, after the loop resumed the lane and
saw the rework commits); four were drawn by the supervisor through an
independent Opus reviewer with a hostile brief, because an adjudication lane
gets no mechanized round before its close (the queued WI-559 defect). The
ADJUDICATE files (`001-ADJUDICATE-4632f10.md`, re-issued in place at the
round-002 rework; `003-ADJUDICATE-9d4fc41.md` and `004-ADJUDICATE-9d4fc41.md`,
two Sol sessions the loop's resume cycle ran under the tripwire's family
shift, both concurring) are the adjudicators' own verdicts, not review rounds.

### Supervisor note — NOT a round, does not govern

The loop stopped on this lane twice. First, the ADJUDICATE session put its
`## Dispositions` block in the verdict file, so `handback.close_adjudication`
refused the mechanical close. Second, after the rework the resumed dispatcher
re-adjudicated the finished lane in a cycle (sessions 003–007: two concurring
verdicts, then NO-COMMIT / ERROR / a rate-limit WAIT) without ever closing —
the C6 shape OI-70 named — until the supervisor stopped the loop and performed
the close through `handback.close_adjudication` by hand (`4d9dba7f`). Kit
findings ride to the session record: the template's placement rule is prose
the session missed; the `open_item` mint writes a thin row; a refused close
must be the stop, not a resume; the minted 184-char Title warns on every
check.

### REVIEW-A — Round 2 — supervisor-drawn, independent Opus, hostile brief — tip 8b75283

Two BLOCKERs: the `## Dispositions` block sat in the verdict file where the
kit's close cannot read it; the owner-owed restore-or-stand question on the
absorbed off-spine baseline — named in the row's own Context by WI-555's round
005 — was decided by omission. Two MAJORs: OI-71's decision 9 miscited
(measured on the lane against its own pre-merge live state; drift 2269/14/4 at
`6d3d9db4` vs 16/0/0 after the merge); the successor's captured scope was the
OUTCOME line. Three MINORs (round-10 "governing" claim; `quick` under-tiers a
spine reseal; round `5175065`'s two BLOCKERs unrouted).
(Full text: `002-REVIEW-A-8b75283-supervisor.md`.)

VERDICT: CHANGES-REQUESTED findings=7

### REVIEW-A — Round 3 — supervisor-drawn verification — tip ba54f6a

All four BLOCKER/MAJOR findings fixed and verified mechanically
(`parse_dispositions` one draft, no refusal; `owes_successor` true; scope
names the four rows, the named KEEP of the LLR-203/204 flips, both
ruling-conditional branches, OI-72 inheritance, the two `5175065` BLOCKERs
routed). One MINOR: the census attribution in the `open_item` text.
(Full text: `003-REVIEW-A-ba54f6a-supervisor.md`.)

VERDICT: APPROVE findings=1

### REVIEW-A — Round 2 (mechanized) — OPENAI-TERRA (medium) — tip 9d4fc41

One MAJOR: the disposition's scalar `open_item` mints a row carrying only
title/status/raised/one_line/wi_refs, so the owner would be handed a bare
question without blast radius, options or a recommendation. Tripwire
`implementer-touched-review-path` fired on the in-place re-issue of the
verdict file (the WI-566 precedent), shifting the resume's routing.
(Full text: `002-REVIEW-A-9d4fc41.md`.)

VERDICT: CHANGES-REQUESTED findings=1

### REVIEW-A — Round 4 — supervisor-drawn verification at the closed tip — tip 4d9dba7

The mechanical close verified sound (spec in `docs/work/complete/`,
Deliverable before Context, the block intact, the mint-shape check clean); the
Terra MAJOR honestly answered (the brief carried in the successor's captured
scope; a construction-first kit finding for a typed `[open_item]` table). One
MAJOR in the supervisor's own brief: "external.toml is unaffected" was false
(8+/4− from `580df781`, a header-comment correction), and the RESTORE option
as written would both re-land that stale comment and red the mirror invariant
permanently (`committed_snapshot_findings`; the lane's decision 10). One
MINOR: the reversal-cost line omitted that red.
(Full text: `004-REVIEW-A-4d9dba7-supervisor.md`.)

VERDICT: CHANGES-REQUESTED findings=2

### REVIEW-A — Round 5 — supervisor-drawn verification — tip 6dd4b77

The brief and the `open_item` question re-issued as STAND versus
REVIEW-THEN-STAND with a byte-level RESTORE stated unavailable by
construction: the mirror-invariant citation verified against the function and
decision 10; the 809-char question is passed whole to `one_line` (title
clipped to 100 with a marker) and rendered whole by the brief; every fact in
the corrected brief checked against the record; `gen_open_items --check`,
`check_trajectory` and `trace --strict-integrity` exit 0. Two MINORs, neither
blocking: "for an explicit act" overstates the off-spine census, which is a
disclosure surface at file grain (the owner's read of the diff IS the act);
the owner's diff command over-selects (it also lists
low-level-requirements.toml) — name the three off-spine paths.
(Full text: `005-REVIEW-A-6dd4b77-supervisor.md`.)

VERDICT: APPROVE findings=2
