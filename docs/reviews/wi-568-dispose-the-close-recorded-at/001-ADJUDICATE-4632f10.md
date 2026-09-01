# 001 — ADJUDICATE (independent) — WI-568 disposition of the WI-508 close

Close under judgement: lane `wi508-architectural-remap` closed **WI-508** as
`partial` (reason "OI-71 RULED (c)"), range `ff29fef8f9..6ba2711078`, split
`keep=[] discard=[]` decided-by-adjudicator, suggested tier `strong`.

**Re-issued in place after REVIEW-A round 002**
(`002-REVIEW-A-8b75283-supervisor.md`, CHANGES-REQUESTED findings=7). The FIRST
`OUTCOME:` line governs and `docs/reviews/` carries no immutability convention
(the WI-566 precedent), so the corrections are made in the text rather than
appended as a contradiction. Three claims below are corrected outright — the
decision-9 citation, the "governing round-10 APPROVE" state, and the
"not owner-owed" finding — and the successor's tier is raised.
**The `## Dispositions` block that stood here has been REMOVED**: a successor's
one home is the adjudicating row's OWN SPEC
(`docs/work/active/wi-568-dispose-the-close-recorded-at/WI-568-dispose-the-close-recorded-at.md`),
which is the only file `handback.close_adjudication` and
`intake._disposition_drafts` read; a block in a verdict file cannot mint.

## Basis (read, not trusted)

- The range **is already on trunk** (`git merge-base --is-ancestor 6ba2711078 HEAD`
  → yes; it arrived via the sanctioned manual partial-close that WI-555 merged at
  `77270030`). This is the special case OI-71 named — the reviewed content stays
  on trunk and a successor re-seals it, rather than a HELD branch being
  cherry-picked at merge.
- **Live reviewed spine content, confirmed on trunk:** `LLR-203`/`LLR-204`
  `Approved`; `TC-199`/`TC-200` `Drafted` with `verifies = ["LLR-203"]` /
  `["LLR-204"]` (the direct `SR-163` target removed at round 013) and `Expected`
  scoped to the LLR arm. **The lane's STANDING verdict is round 019
  CHANGES-REQUESTED, not an APPROVE:** the round-010 APPROVE (`899352b7`, 05:47)
  was followed by `209773cf` (08:46, findings=1) and `fa3c99c4` (08:59,
  findings=3 — the HELD tip, WI-554's "Round 019"), all three MAJORs of which are
  externally discharged (below). The narrower row-level claim is what survives
  and it holds on evidence: `git diff --stat b8d57e9f 6ba2711078 --
  docs/requirements/low-level-requirements.toml docs/test/test-cases.toml`
  touches only three unrelated `evidence` cells (TC-050/TC-186/TC-193 re-pointed
  to `tests/test_trace_interfaces.py` by the WI-521 split), so **the four rows
  are byte-identical to the round-010-approved tree**.
- **The three round-019 MAJORs are all externally discharged:** the two
  `trace.py --approve modified` renderer defects → `WI-554`
  (`docs/archive/work/complete/WI-554-approval-brief-defects.md`, complete); the
  `SR-163` shape → `OI-72` ruled 2026-08-31 and owned by re-scoped `WI-543`
  (`docs/archive/work/complete/WI-543-sr163-verification-tc.md`, complete —
  ships the tolerant reference cell + four-class checker + direct TC).
- **What OI-71 decision 9 actually measured — and what it does not cover.**
  `docs/decisions-for-review-2026-08-31.md:203` measured `intake.py --root .
  snapshot` **on the lane**, against the **lane's own pre-merge live state**,
  and found the tree byte-identical. That is branch-local self-consistency and it
  predates the merge; it says **nothing** about trunk's pre-merge
  `docs/archive/last_approved` baseline or the off-spine rows the merge absorbed
  into it. The measurement that does bear on trunk points the other way: live
  vs. baseline drift for the off-spine registries was **2269 / 14 / 4** diff
  lines (`interfaces.toml` / `external.toml` / `components.toml`) at the
  pre-merge anchor `6d3d9db4`, and is **16 / 0 / 0** now. Trunk's live registries
  ARE the absorbed content, so a regeneration at the successor's approval commit
  **re-seals** the absorption; it does not review or re-open it. The loss is the
  AUTHORITY and the VISIBILITY of those rows' approval, not the content (WI-555
  round 005 said this in the same terms). Correspondingly
  `docs/ratify/CURRENT.md`'s off-spine census collapsed from "132 changed, 30
  added, 3 removed … OI-64, OI-65, OI-67, WI-522, WI-528, WI-530, WI-531,
  WI-533, WI-534, WI-553" at `6d3d9db4` to "1 changed, 0 added, 1 removed …
  WI-553" now, under `_Baseline: docs/archive/last_approved — copied 2026-08-30
  (4824c0ba)_`.
- **Authority is not in question.** `docs/process.toml` sets
  `human_approval_through = "DevStg-Needs"`, below `agent_common.APPROVAL_RUNGS`
  for `external`/`interfaces`/`components`, so both the `LLR-203`/`LLR-204` flip
  and the baseline absorption were loop-legal. The defect is DISCLOSURE and
  JUDGEMENT, not permission.
- **No inbound hard `needs` edge points at WI-508** (grep of queued/active), so the
  supersede re-point strands nothing.
- **Two BLOCKERs of `docs/reviews/wi508-architectural-remap/010-REVIEW-A-5175065.md`
  fall outside this close's range and were on no queue** — they target
  `docs/plans/2026-08-25-blind-minimal-map-{brief,derivation}.md`, both on trunk,
  named nowhere in `docs/requirements`, `docs/work` or `docs/status.md` outside
  the archived WI-508 spec. They are not silently closed over: they are routed as
  named items in the successor's scope. Its Team-A census MINOR is left
  explicitly out of scope.

## Findings

- [MINOR] The claimed outcome **PARTIAL is correct** -> the program delivered slices 1–5 in full (SR-163 decomposed, the two-axis blind derivation, the eighteen-family alignment survey, `WI-519`/`WI-520`/`WI-521` filed, `OI-64` raised-and-ruled, the ratchet debt re-owned) and blessed-then-reviewed the four slice-1 rows, but `SR-163`'s full file→requirement join was honestly unscheduled at close and the lane never landed a clean confirming reviewer round on current trunk (round 019 stalled with three MAJORs). It is neither `complete` (a genuine arm was owed) nor a half-close; PARTIAL matches the owner's OI-71 (c) ruling -> keep the outcome PARTIAL; the byte-identical spec moves to `complete/` and the report stays on record as its claim -> @owner
- [MINOR] The `keep=[] / discard=[]` split, punted to the adjudicator, **is honest — resolved KEEP-all on the whole `ff29fef8f9..6ba2711078` range** -> the range is already merged to trunk via the sanctioned manual partial-close; the four spine rows are byte-identical to the round-010-approved tree (diff verified above) and are the honest final state; nothing shippable is quietly left on trunk that should be reverted. **The `580df781` `Drafted` -> `Approved` flips of `LLR-203`/`LLR-204` are KEPT — an explicit, named keep decision, not a default**: loop-permitted at this repo's `DevStg-Needs` dial and unchanged since the approving review. `TC-199`/`TC-200` stay `Drafted` -> no commit reversion; the successor confirms the four rows on current trunk rather than re-litigating the flip -> @owner
- [MAJOR] The `docs/archive/last_approved` **restore-or-stand question IS owner-owed and is minted as an open item** -> this row's own `## Context` named it so, and the first pass of this verdict decided it as "stand" BY OMISSION — never mentioning `last_approved`, the 132→1 census collapse, or the nine rulings — while drafting a successor whose reseal makes the absorption permanent. The judgement is: the CONTENT is fine and no reversion of the range is owed, but whether the approved BASELINE keeps the 132 changed / 30 added / 3 removed off-spine rows it absorbed, or gives them back to the re-attestation brief for an explicit act, is a disclosure decision above a lane -> drafted as the `open_item` cell of the successor's block in THIS ROW'S SPEC; `intake._inject_open_item` mints a `pending` OI at the merge and lands its id in the successor's `needs`, parking it `waiting:open-item-pending` until the owner rules. A lane may not allocate an OI id -> @owner
- [MINOR] The successor's tier is **`strong`, not `quick`** -> `agent_loop.claim_routing` pins the BUILD phase's model tier from `BuildTier`, and a `safety_class = "spine"` row that re-confirms four spine rows and rewrites the approval baseline is exactly the shape where a bottom-tier worker rubber-stamps. The predecessor consumed nineteen rounds at `strong`, its handback suggested `strong`, and WI-568 itself is `strong` -> `buildtier = "strong"`, `planmode = "single"` (a reseal under a ruling, not a design fork) -> @owner

## Disposition reasoning

*(The successor's executable scope is authored in the prose AFTER the fenced
block in this row's spec — that is the text `parse_dispositions` captures and
`_disposition_drafts` rides verbatim into the minted `## Context`. It is not
restated here.)*

The successor's substantive predecessors (`WI-543` SR-163 verification, `WI-554`
renderer defects) are complete and the reviewed spine content is already on
trunk, so the remaining scope is narrow but not thin: draw the one clean
cross-family reviewer round the lane never got on the current tree — the "fresh
reviewer round on a refreshed tree" the report itself lists under *Not
delivered* — confirming the four rows stand in their reviewed state; then apply
the owner's ruling on the baseline. Under "stand", regenerate
`docs/archive/last_approved` via `intake.py snapshot` at the successor's own
approval commit (never copied from the branch's snapshot bytes, per OI-71 (c)),
recording that this RE-SEALS the absorption rather than reviewing it. Under
"restore", re-copy the `6d3d9db4` off-spine snapshot files in a reviewed commit
and let the brief re-list the rows. It inherits OI-72's SR-163 ruling and carries
the two unrouted `5175065` BLOCKERs as named items.

OUTCOME: PARTIAL successors=1
