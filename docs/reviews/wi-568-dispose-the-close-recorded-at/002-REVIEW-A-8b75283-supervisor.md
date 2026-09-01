### REVIEW-A — WI-568 — Round 002 — 2026-09-01 — supervisor-drawn (independent Opus, hostile brief)

Tree: `/Users/diytechy/Documents/ai-template-drive/wi-568-dispose-the-close-recorded-at`,
branch `wi-568-dispose-the-close-recorded-at` @ `4f1590d9`; adjudication commit
`8b752831`. Python `/Users/diytechy/Documents/ai-template/.venv/bin/python`.
Worst failure classes hunted: a disposition that cannot mint, an owner-owed
question silently decided as "stand", and a successor a worker cannot execute.

## What I verified

**The `## Dispositions` block is in the verdict file, and the spec has none.**
The machinery reads the SPEC:

```
intake.parse_dispositions(<WI-568 spec>)   -> ([], None)          # no section at all
intake.owes_successor(<spec meta>)         -> True
intake.parse_dispositions(<001-ADJUDICATE-4632f10.md>)
  -> ([{'buildtier':'quick','planmode':'single','priority':2,
        'supersedes':'WI-508',
        'title':'WI-508 spine reseal: one clean reviewer round on current trunk,
                 regenerate last_approved at the approval commit',
        'workstream':'process','kind':'spine',
        'scope':'OUTCOME: PARTIAL successors=1'}], None)
title len: 111
```

`handback.close_adjudication` (`handback.py:518-527`) parses `text` read from
`active/<branch>/<name>` — the spec — and refuses on `owes_successor(meta) and
not parsed`. `intake._disposition_drafts` (`intake.py:1164`) does the same on the
archived spec at the merge. The prompt is explicit
(`project-trajectory/prompts/adjudicate-disposition.template.md:42`): draft it
"as a fenced `toml` block under a `## Dispositions` heading in THIS SESSION'S OWN
SPEC — never in the verdict file".

**Key set and grammar — clean once relocated.** `_DRAFT_KEYS`
(`intake.py:217-243`) contains `title, workstream, buildtier, planmode,
safety_class, specref, sr_refs, needs, priority, bar, supersedes, open_item`;
`planmode` and `priority` are valid, `safety_class = "spine"` is in
`schedule.SAFETY_CLASSES`, `buildtier = "quick"` is in
`agent_route.TIER_ORDER = ("quick","medium","strong")`, and title is 111 chars
(under the 120-char `check_trajectory` WARN — WI-568's own title tripped it at
184). `supersedes = "WI-508"` is a free-text lineage cell (`intake.py:1409`)
plus the inbound-edge re-point (`_apply_supersede`); `grep -rn WI-508
docs/work/queued/ docs/work/active/` returns no hard `needs` edge, so the
re-point strands nothing. No mint refusal here.

**The scope prose is empty.** `parse_dispositions` takes the prose AFTER each
block (`intake.py:1092,1109`) and `_disposition_drafts` rides it verbatim into
the minted `## Context` (`intake.py:1196-1199`). The only text after the block is
the machine line, so `scope == 'OUTCOME: PARTIAL successors=1'`. The
"Disposition reasoning" section sits BEFORE the block and is not captured.

**Range on trunk — HOLDS.** `git merge-base --is-ancestor 6ba2711078 HEAD` -> yes.

**The round-10 APPROVE was superseded.** `git log --name-only --date=short --
docs/reviews/wi508-architectural-remap/` in chronological order:

```
899352b7 2026-08-30 05:47:16  010-REVIEW-A-b8d57e9.md   VERDICT: APPROVE findings=0
209773cf 2026-08-30 08:46:54  010-REVIEW-A-52faa5d.md   VERDICT: CHANGES-REQUESTED findings=1
fa3c99c4 2026-08-30 08:59:11  010-REVIEW-A-1cf170f.md   VERDICT: CHANGES-REQUESTED findings=3
```

`fa3c99c4` is the origin HELD tip and `WI-554`'s Context names its three MAJORs
as "Round 019". So the lane's LAST recorded verdict is CHANGES-REQUESTED, not
APPROVE. The four rows themselves did not move after the APPROVE, though:
`git diff --stat b8d57e9f 6ba2711078 -- docs/requirements/low-level-requirements.toml
docs/test/test-cases.toml` -> only `test-cases.toml | 6 +++---`, and the three
hunks are `evidence` cells of TC-050/TC-186/TC-193 re-pointed to
`tests/test_trace_interfaces.py` (the WI-521 split) — LLR-203/204 and
TC-199/200 are untouched.

**Decision 9 measured the BRANCH against ITSELF.**
`docs/decisions-for-review-2026-08-31.md:203`: "`intake.py --root . snapshot` **on
the lane** leaves the tree byte-identical". Live-vs-baseline drift, measured:

```
                    @6d3d9db4 (pre-merge trunk)     now (HEAD)
interfaces.toml       2269 diff lines                16
external.toml           14                            0
components.toml          4                            0
```

`head -18 docs/ratify/CURRENT.md` now reads "_Baseline: `docs/archive/last_approved`
— copied 2026-08-30 (`4824c0ba`)_" and an off-spine census of "1 changed, 0 added,
1 removed … ruling(s): WI-553", against `6d3d9db4:docs/ratify/CURRENT.md`'s
"132 changed, 30 added, 3 removed … OI-64, OI-65, OI-67, WI-522, WI-528, WI-530,
WI-531, WI-533, WI-534, WI-553". So a regeneration "at the successor's approval
commit" reproduces the branch bytes because trunk's live registries ARE the
absorbed content — it re-blesses the 132, it does not re-open them.

**Authority — the flip and the absorption are loop-legal.**
`docs/process.toml:116` `human_approval_through = "DevStg-Needs"`;
`agent_common.APPROVAL_RUNGS = {"external":"DevStg-Boundary",
"interfaces":"DevStg-Arch","components":"DevStg-Arch"}` and `human_approves`'
docstring: "At this repo's `DevStg-Needs` dial that is none." So no authority
breach — the defect is disclosure and judgement, not permission.

**Unrouted findings.** `010-REVIEW-A-5175065.md` returned 8 findings including two
BLOCKERs against `docs/plans/2026-08-25-blind-minimal-map-{brief,derivation}.md`
(both on trunk) and a Team-A census MINOR. `grep -rl 2026-08-25-blind-minimal-map
docs/requirements docs/work docs/status.md` -> only the archived WI-508 spec. No
OI, no WI, no status row owns them; the only trace is one sentence at
`docs/decisions-for-review-2026-08-31.md:228`.

**WI-543 / WI-554 complete — HOLDS.** Both present under
`docs/archive/work/complete/`, and `WI-554`'s Deliverable covers exactly two of
round 019's three MAJORs (the `Drafted`-labelled-approved cell split and the
truncated `Method` cell).

## Findings

- [BLOCKER] docs/reviews/wi-568-dispose-the-close-recorded-at/001-ADJUDICATE-4632f10.md:55 -> the `## Dispositions` block is placed in the VERDICT file; the ruling therefore cannot mint and the row cannot close -> `intake.parse_dispositions` on the WI-568 spec returns `([], None)` while `owes_successor(meta)` is `True`, so `handback.close_adjudication` (handback.py:521-527) refuses and `intake._disposition_drafts` (intake.py:1184) would refuse again at the merge; the prompt template line 42 says "in THIS SESSION'S OWN SPEC — never in the verdict file" -> move the fenced block verbatim into a `## Dispositions` section of `docs/work/active/wi-568-dispose-the-close-recorded-at/WI-568-dispose-the-close-recorded-at.md` and leave a pointer in the verdict; the defect cannot be made unrepresentable in the mint (the verdict file is not an input to any close path, so no code there can see the misplacement) — the cheapest guard is the recorder refusing a `## Dispositions` heading inside a `*-ADJUDICATE-*.md`, where such a heading is never legitimate -> @worker
- [BLOCKER] docs/reviews/wi-568-dispose-the-close-recorded-at/001-ADJUDICATE-4632f10.md:38 -> the ruling declares "not owner-owed / no `open_item`" without ever judging the `docs/archive/last_approved` restore-or-stand question that this row's own `## Context` named as owner-owed, so an owner-owed question is decided as "stand" by omission -> the spec's Context bullet 2 says "Restore trunk's baseline to the `6d3d9db4` bytes for `interfaces.toml` / `external.toml` / `components.toml`, or let the absorption stand — owner-owed; mint an OI through this row's `open_item` cell if the adjudicator judges it needs the owner"; the verdict's Basis, Findings and Disposition reasoning never mention `last_approved`, the 132->1 census collapse, or the nine rulings, and the successor's "regenerate at its own approval commit" makes the absorption permanent (live-vs-baseline is already 16/0/0 lines) -> either rule "stand" explicitly, on the record, with the reason and the disclosure cost stated, or draft `open_item = "restore trunk's docs/archive/last_approved off-spine bytes to the 6d3d9db4 anchor, or let the wi508 merge's absorption of 132 changed / 30 added / 3 removed interface rows across OI-64/65/67 and WI-522/528/530/531/533/534/553 stand?"`, which `_inject_open_item` lands in the successor's `needs` -> @owner
- [MAJOR] docs/reviews/wi-568-dispose-the-close-recorded-at/001-ADJUDICATE-4632f10.md:25 -> "Snapshot degradation risk … is null: OI-71 decision 9 measured `intake.py snapshot` reproducing the lane's snapshot byte-identical from live state" is a category error carried as the load-bearing basis for KEEP-all -> decision 9 (`docs/decisions-for-review-2026-08-31.md:203`) measured the snapshot ON THE LANE against the LANE's own live registries — branch-local self-consistency, and it predates the merge; it says nothing about trunk's pre-merge baseline, and the measurement it does license is the opposite of reassuring: interfaces live-vs-baseline was 2269 lines at `6d3d9db4` and is 16 now, i.e. trunk's live state IS the absorbed content, so regenerating at the successor's approval commit re-seals the 132 rather than re-opening them; round 005 said this in terms ("the loss is the AUTHORITY and the visibility, not the content") -> replace the "risk is null" sentence with the true scope of decision 9 and state that the reseal preserves rather than reviews the absorption; this cannot be made unrepresentable — it is a reading error about what a recorded measurement covered, and no check can bind a prose citation to its subject -> @worker
- [MAJOR] docs/reviews/wi-568-dispose-the-close-recorded-at/001-ADJUDICATE-4632f10.md:66 -> the successor as drafted is not executable: its minted `## Context` will carry no scope -> `parse_dispositions` captures only the prose AFTER the block (intake.py:1092,1109) and `_disposition_drafts` writes exactly that into the mint's Context (intake.py:1196-1199); the measured `scope` is `'OUTCOME: PARTIAL successors=1'`, because the "Disposition reasoning" paragraph — which names the rows, the command, and the verdict shape — sits BEFORE the block; the minted row would reach a worker as a 111-char title and nothing else -> move the Disposition-reasoning paragraph to sit between the fence and the `OUTCOME:` line, naming LLR-203/LLR-204/TC-199/TC-200, `python project-trajectory/scripts/intake.py --root . snapshot` in the approval commit, and the reviewer-round verdict shape owed; this is representable-but-empty by construction, so a guard would have to judge prose sufficiency — instead the fix is authorial placement -> @worker
- [MINOR] docs/reviews/wi-568-dispose-the-close-recorded-at/001-ADJUDICATE-4632f10.md:17 -> "This is the governing round-10 APPROVE state" overstates the lane's review record and contradicts the same verdict's own PARTIAL finding ("the lane never landed a clean confirming reviewer round on current trunk") -> the APPROVE (`899352b7`, 05:47) was followed by `209773cf` (08:46, CHANGES-REQUESTED findings=1) and `fa3c99c4` (08:59, CHANGES-REQUESTED findings=3, the HELD tip and WI-554's "Round 019"), so the lane's LAST verdict is CHANGES-REQUESTED; the narrower claim survives on evidence the verdict does not cite — `git diff b8d57e9f 6ba2711078` touches only three unrelated `evidence` cells, leaving LLR-203/204 and TC-199/200 byte-identical to the approved tree -> restate as "the four rows are byte-identical to the round-010-approved tree (`b8d57e9f`), verified by diff; the lane's standing verdict is round 019 CHANGES-REQUESTED, discharged by WI-543/WI-554" -> @worker
- [MINOR] docs/reviews/wi-568-dispose-the-close-recorded-at/001-ADJUDICATE-4632f10.md:60 -> `buildtier = "quick"` beside `safety_class = "spine"` under-tiers the worker that will re-approve spine rows and rewrite the approval baseline -> `agent_loop.claim_routing` pins the BUILD phase's model tier from `BuildTier` (agent_loop.py:548) and `quick` is the bottom of `agent_route.TIER_ORDER`; the predecessor consumed nineteen rounds at `strong`, the closed row's report suggested tier `strong`, and WI-568 itself is `strong` — "confirm and reseal" is precisely the shape where a cheap worker rubber-stamps -> raise to `medium`; the reviewer tier is set by phase and is unaffected, so this is a judgement call on the worker only, not a mechanizable rule -> @worker
- [MINOR] docs/reviews/wi-568-dispose-the-close-recorded-at/001-ADJUDICATE-4632f10.md:29 -> the ruling accounts for round 019's three MAJORs and stops, leaving round `5175065`'s two BLOCKERs and one MINOR unrouted by the disposition that was this thread's last chance to route them -> those findings target `docs/plans/2026-08-25-blind-minimal-map-{brief,derivation}.md`, which are on trunk (`ls docs/plans/`), and `grep -rl` over `docs/requirements`, `docs/work` and `docs/status.md` finds them named only in the archived WI-508 spec; decision 10 said they were "carried to the owner as findings against that record", but no OI or WI carries them -> add one sentence to the Basis noting they fall outside the close's range and file them as their own trunk-side row (or name them in the successor's scope) rather than letting the adjudication close over them silently -> @owner

VERDICT: CHANGES-REQUESTED findings=7
