# WI-568 — REVIEW-A rollup

Compiled by the supervising session (2026-09-01) from the round files under
`docs/reviews/wi-568-dispose-the-close-recorded-at/`, time-ordered, governing
line last. No mechanized round exists for an adjudication lane (the queued
WI-559 defect: the loop schedules a round only after a committing BUILD);
both rounds were drawn by the supervisor through an independent Opus reviewer
with a hostile brief. `001-ADJUDICATE-4632f10.md` is the adjudicator's own
verdict (re-issued in place at the rework), not a review round.

### Supervisor note — NOT a round, does not govern

The loop stopped on this lane before any round: the ADJUDICATE session had
put its `## Dispositions` block in the verdict file, so
`handback.close_adjudication` refused the mechanical close ("drafted NO
successor in its ## Dispositions section"). The rework moved the block to its
one home, the spec, and the loop's resume performs the close. Two kit
findings ride to the session record: the adjudication template's placement
rule is stated in prose the session missed, and the row's minted 184-char
Title warns on every check.

### REVIEW-A — Round 2 — supervisor-drawn, independent Opus, hostile brief — tip 8b75283

Two BLOCKERs: the `## Dispositions` block sat in the verdict file where the
kit's close cannot read it (`intake.parse_dispositions` on the spec returned
no draft while `owes_successor` was true); the owner-owed restore-or-stand
question on the absorbed off-spine baseline — named in the row's own Context
by WI-555's round 005 — was decided by omission ("not owner-owed, no
`open_item`"). Two MAJORs: OI-71's decision 9 miscited (it measured
`intake.py snapshot` on the lane against the lane's own pre-merge live
state; live-vs-baseline drift was 2269/14/4 lines at `6d3d9db4` and 16/0/0
after the merge, so "regenerate at the successor's approval commit" would
re-seal the absorption rather than review it); the successor's captured
scope was literally the OUTCOME line because the reasoning preceded the
fence. Three MINORs: "governing round-10 APPROVE" is wrong (rounds 011–019
re-opened it), `quick` under-tiers a spine reseal, and round `5175065`'s two
BLOCKERs against on-trunk blind-map plans were unrouted.
(Full text: `002-REVIEW-A-8b75283-supervisor.md`.)

VERDICT: CHANGES-REQUESTED findings=7

### REVIEW-A — Round 3 — supervisor-drawn verification, independent Opus — tip ba54f6a

All four BLOCKER/MAJOR findings fixed and verified mechanically:
`parse_dispositions` on the spec returns one draft with no refusal,
`owes_successor` true, `_mint_shape_refusal` none, so the mechanical close
falls through; the captured scope (3027 chars) names the four rows with
live statuses, the LLR-203/LLR-204 flips as a named KEEP with TC-199/TC-200
held Drafted, both ruling-conditional baseline branches with the command,
OI-72 inheritance, the two `5175065` BLOCKERs routed with file:line, and a
not-in-scope clause; the `open_item` is one rulable question whose
`_inject_open_item` → `needs` → `waiting:open-item-pending` parking is
confirmed in `schedule._waiting_reasons`; the decision-9 correction
re-measured (2269/14/4 vs 16/0/0); the verdict file carries exactly one
`OUTCOME:` line; the fragment's file-level `Deferred open items:` line is
read by `gen_open_items --check` (exit 0) and its links resolve. One MINOR:
the `open_item` cell attaches interfaces.toml's 132/30/3 census to all three
off-spine registries and omits WI-520 behind components.toml's own 1/0/0
line — lane's to tidy, not blocking.
(Full text: `003-REVIEW-A-ba54f6a-supervisor.md`.)

VERDICT: APPROVE findings=1
