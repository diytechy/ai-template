### REVIEW-A — WI-555 — Round 005 — 2026-09-01 — supervisor-drawn (independent Opus, hostile brief)

Tree: `/Users/diytechy/Documents/ai-template-drive/wi-555-wi508-partial-close`,
branch `wi-555-wi508-partial-close` @ `5c8a007a` (which now CONTAINS trunk
`contract_split` @ `551d1b2c`), so unlike rounds 002/004 the wi508 conversion is
visible in this working tree and every claim was checked against it and against
git history. Python: `/Users/diytechy/Documents/ai-template/.venv/bin/python`.
Worst failure classes hunted: a false record of an unfinished close, a silent
approval-authority move, and a state a successor cannot proceed from.

## What I verified

**Arm 4 / phantom head — HOLDS.** The shipped admission path, not a file probe:

```
integrate._claimed_specs(r,'wi508-architectural-remap') -> []
integrate.branch_outcomes(r,'wi508-architectural-remap') -> ({}, [])
integrate.finished_branches(r) -> ['wi-555-wi508-partial-close']
```

`ls docs/work/active/` -> `wi-555-wi508-partial-close` only. `schedule.py ready`
no longer lists WI-508 at all (head of frontier is `WI-568 exclusive rank=1 P0`);
`check_trajectory.py` exits 0 with no WI-508 row and no hold-by-rename WARN.
Scheduler and dispatcher agree.

**Arm 2 / merge and brief — HOLDS in substance.** `979c3e5f` reads
`integrate: merge wi508-architectural-remap (WI-508)` / `Outcomes (§A3):
WI-508=partial` / `bar PASS (11 steps, tier all)`. No verdict was owed.
`trace.py --approve modified --check` -> `trace: approval-check —
docs/ratify/CURRENT.md is current` (exit 0). `check.py --jobs 0` ->
`RESULT: PASS` (11 steps, `approval-immutable PASS`, `doc-navigability PASS`).
`trace.py --strict-integrity` -> `integrity=0 ... provenance-findings=1
paraphrase-advisories=3`, exit 0 (all pre-existing LLR-181/LLR-197/SR-168
advisories). `check_trajectory.py --strict` exits 1 on ONE error —
`cross-component import scripts/schedule (CMP-008) -> scripts/trace (CMP-006)
has no declared IF-### seam` — which is WI-552's, already owned by queued
WI-564; `git show 6d3d9db4:project-trajectory/scripts/schedule.py` carries the
same `import trace as _trace` at line 444, so it predates this lane.

**Arm 1 / the report and the range — mostly holds.** `docs/handbacks/WI-508-wi508-architectural-remap.md`
exists with `claimed_outcome = "partial"`, the reason, `commit_range =
"ff29fef8f9..6ba2711078"`, `split_decided_by = "adjudicator"`. The range is real
and non-empty: `git log --oneline ff29fef8f9..6ba2711078 | wc -l` -> `44`, and
`git merge-base 6d3d9db4 fa3c99c4` -> `ff29fef8f9de...`, i.e. the range base IS
the true merge base and `6ba27110`'s parent IS `fa3c99c4` = the origin HELD tip.
`git merge-base --is-ancestor 6ba2711078 HEAD` -> `YES`: nothing was discarded.
Deferring keep/discard to the adjudicator is sanctioned — OI-70 RULED the
adjudicator judges the handback with exactly two exits, and `render_report`'s own
text says the split "is therefore OWED".

**Arm 3 / the mint — HOLDS.** `551d1b2c` = `mint: WI-568 ... (WI-388 intake;
bookkeeping)`, i.e. `intake.intake_after_merge`, not a hand mint. `WI-568`
carries `specref = docs/work/partial/WI-508-architectural-remap-program.md`,
`brief = "disposition"`, `safety_class = "adjudication"`. No `needs` — correct
for a disposition row (WI-551, the WI-550 precedent, has none either).

**The spine rows — the arm's premise is wrong AND the state moved.**

```
git show 6d3d9db4:docs/requirements/low-level-requirements.toml | grep -A12 '^\[design.LLR-203\]'
  status = "Drafted"     (LLR-203)   status = "Drafted"  (LLR-204)
git show 551d1b2c:...
  status = "Approved"    (LLR-203)   status = "Approved" (LLR-204)
```

`trace.py` corroborates: `drafts=11` in rounds 002/004 (pre-merge tree) vs
`drafts=9` now. TC-199/TC-200 are `Drafted` (verified in `docs/test/test-cases.toml`).
The flip came in with the merge from branch commit `580df781` (2026-08-30,
`Reviewer <reviewer@example.test>`), which states on its face: "Under the declared
dial (human_approval_through = DevStg-Needs) LLR/TC are loop-held, so this is a
reviewed-commit approval, not a human sitting." `docs/process.toml:116` confirms
`human_approval_through = "DevStg-Needs"`, so **machine approval of an LLR here
is permitted** — this is not an authority breach. But the Done-when arm's noun
phrase ("the four Drafted spine rows ... unflipped") is factually false of the
delivery, and so is the handback report's `## Delivered`.

**The snapshot — the material finding.** `docs/archive/last_approved/` on trunk
was rewritten by the merge:

```
git diff --stat 6d3d9db4 551d1b2c -- docs/archive/last_approved/
  README.md | 1 +, components.toml | 2 +-, external.toml | 12 +-,
  interfaces.toml | 1822 ++++----, low-level-requirements.toml | 42 +-,
  test-cases.toml | 43 +-       (6 files, 1029 insertions, 893 deletions)
git log --oneline 6d3d9db4..551d1b2c -- docs/archive/last_approved/
  4824c0ba  WI-508 rework: revert TC-199/TC-200 to Drafted ...
  580df781  WI-508: approve the four slice-1 spine rows and anchor the record
```

Both writers are wi508 BRANCH commits. Live-vs-baseline drift on trunk before
and after:

```
interfaces.toml   diff live vs last_approved @6d3d9db4 -> 2269 lines
                                             @551d1b2c ->   16 lines
external.toml     14 -> 0        components.toml  4 -> 0
```

The kit's own brief names exactly what was absorbed. `git show
6d3d9db4:docs/ratify/CURRENT.md`:

> _Baseline: `docs/archive/last_approved` — copied 2026-08-24 (13593db9)_
> - `docs/requirements/interfaces.toml` — **132 changed, 30 added, 3 removed**
>   since the snapshot; ruling(s): OI-64, OI-65, OI-67, WI-522, WI-528, WI-530,
>   WI-531, WI-533, WI-534, WI-553.
> - `docs/requirements/components.toml` — 1 changed, 0 added, 0 removed;
>   ruling(s): WI-520.

`head -25 docs/ratify/CURRENT.md` (now):

> _Baseline: `docs/archive/last_approved` — copied 2026-08-30 (**4824c0ba**)_
> - `docs/requirements/interfaces.toml` — **1 changed, 0 added, 1 removed**
>   since the snapshot; ruling(s): WI-553.

So the off-spine approval backlog trunk was carrying — 132 changed / 30 added /
3 removed interface rows across nine rulings, plus a components.toml change — was
absorbed into the approved baseline by this merge, and the brief's "what a
re-seed will absorb" surface (the thing that would show a signer the debt) is now
empty. The baseline stamp on trunk cites `4824c0ba`, a commit on a lane whose
outcome is `partial`. `approval-immutable` still PASSes and the residual
live-vs-baseline diff is small, so the *bytes* are close to what a regeneration
would produce (consistent with OI-71's "Decision 9" measurement) — the loss is
the AUTHORITY and the visibility, not the content.

**Conventions.** `grep -n "Deferred open items" docs/log.d/WI-555-wi508-partial-close.md`
-> no match. `grep -c "fig:"` -> `0`; the fragment drives no figures, so only the
first is owed. `gen_open_items.py --check` -> `open-items view up to date`.
`check_trajectory` (default) -> exit 0, **53 WARNs**, including a new one this
close introduced: `WI-568 (184 chars)` over the 120-char Title bound.

**Hand-done work.** `git show 6ba2711078 --stat` is a pure rename,
`archive/work/complete/ -> work/active/wi508-architectural-remap/`, 0 insertions
— a bare `git mv`, not `spec_move.py`. `doc-navigability` PASSes, so no link was
stranded, and OI-71 explicitly sanctioned the manual special case. Everything
else went through a kit script: `09f88ca2` is `handback.close_partial`, `979c3e5f`
is `integrate.py integrate`, `551d1b2c` is `intake.intake_after_merge`.

**Trunk claims in the Deliverable.** `git rev-parse --short contract_split` ->
`551d1b2c`; `09f88ca2`, `979c3e5f`, `d8848bf4`, `e78b07c4`, `551d1b2c` all exist
with the described subjects. The "record-only lane" framing is sound and round
002's finding was indeed a base-cut artifact — round 004's false-positive call
stands.

## Findings

- [MAJOR] docs/archive/work/complete/WI-555-wi508-partial-close.md:44 -> the record says "The last_approved REGENERATION condition is that successor's job", implying the branch's snapshot bytes have not landed; they landed at this merge -> `git log --oneline 6d3d9db4..551d1b2c -- docs/archive/last_approved/` names only branch commits `580df781`/`4824c0ba`, and `docs/ratify/CURRENT.md`'s off-spine census fell from "132 changed, 30 added, 3 removed ... OI-64, OI-65, OI-67, WI-522, WI-528, WI-530, WI-531, WI-533, WI-534, WI-553" to "1 changed, 0 added, 1 removed ... WI-553", with the baseline stamp now citing branch commit `4824c0ba` — trunk's unsigned off-spine approval debt was absorbed into the approved baseline by a lane whose outcome is `partial`, and the surface that displayed that debt is now blank -> the LANE must state this in `docs/log.d/WI-555-wi508-partial-close.md` and in the Deliverable (what moved, which rulings' rows, and that the pre-merge anchor is `13593db9`/`6d3d9db4:docs/archive/last_approved`), and name it as an explicit item in WI-568's Context so the adjudicator judges it as part of the `580df781` keep/discard rather than inheriting it silently; whether trunk's baseline is restored to `6d3d9db4` bytes for the off-spine registries or the absorption stands is an approval-authority question the owner rules. Construction-first: this cannot be made unrepresentable by a check alone because the merge is a plain content merge — the durable fix is for `intake.py snapshot` to be the only writer of `docs/archive/last_approved/` reachable on trunk, i.e. for the integrator to regenerate the baseline from live state after a merge rather than accept a branch's copy, which removes the class instead of warning about it -> LANE (disclose + route), then OWNER (restore-or-stand), with WI-568 carrying the keep/discard.
- [MAJOR] docs/handbacks/WI-508-wi508-architectural-remap.md:22 -> the immutable report's `## Delivered` says "The four Drafted slice-1 spine rows for SR-163's DELIVERED arms", and this is the first document WI-568's adjudicator is told to read -> two of the four are not Drafted: `git show 551d1b2c:docs/requirements/low-level-requirements.toml` gives LLR-203 `status = "Approved"` and LLR-204 `status = "Approved"`, and the spec archived in the SAME commit contradicts the report at `docs/work/partial/WI-508-architectural-remap-program.md:24` — "The two **LLRs are `Approved`**; the two **TCs are `Drafted`**". The text is authored, not generated: `handback.close_partial(root, branch, reason, fields)` passes `fields` straight into `station.render_report`, so this sentence was supplied by the closing session -> the report is immutable and must stay as the claim it was; the LANE must add a correction line to `docs/log.d/WI-555-wi508-partial-close.md` naming the report's `## Delivered` sentence as inaccurate and stating the true 2-Approved/2-Drafted split, and repeat it in WI-568's Context. Construction-first: the class is unrepresentable if `render_report` DERIVES the delivered-rows census from the registry diff over `commit_range` instead of accepting free prose for a field anything downstream keys off -> LANE, then a kit row for the derived-census change.
- [MAJOR] docs/archive/work/complete/WI-555-wi508-partial-close.md:86 -> Done-when arm 4's clause "the four Drafted spine rows reach trunk unflipped" is false of the delivery -> LLR-203/LLR-204 were `Drafted` on trunk at `6d3d9db4` and are `Approved` at `551d1b2c` (quoted above); `trace.py` reports `drafts=9` where rounds 002/004 read `drafts=11`. The flip is NOT an authority breach — `docs/process.toml:116` sets `human_approval_through = "DevStg-Needs"`, leaving LLR/TC loop-held, and `580df781` says so on its face — and the arm's wrong premise is inherited from OI-72's own phrase "The wi508 branch's four Drafted rows stay honest as-is", written 2026-08-31 when two had been Approved since 2026-08-30. The lane did flag it honestly (fragment:95) and did not claim the arm -> no lane rework beyond finding 2's correction line; WI-568 must decide stand-or-revert on the LLR approvals as a named keep/discard over `580df781`, and the OWNER should correct OI-72's "four Drafted" wording so the next reader is not misled again -> WI-568 + OWNER.
- [MINOR] docs/archive/work/complete/WI-555-wi508-partial-close.md:73 -> arm 1's "The ref renamed back to `wi508-architectural-remap`" reads as a durable state and is not one -> `git branch -a | grep -i wi508` and `git for-each-ref` return exactly one ref, `refs/remotes/origin/wi508-architectural-remap-HELD-for-owner-verdict fa3c99c4`; the local ref was created and force-deleted, and origin still carries the `-HELD-` suffix OI-70 calls "a bypass of this flow". The arm's mechanical purpose (letting `lane_worktree`/`_claimed_specs` match) was served and the merge landed, so the substance holds -> the OWNER should rename or delete `origin/wi508-architectural-remap-HELD-for-owner-verdict` now the range is in trunk history (`push = "human"` puts it out of the lane's reach); the lane should say "renamed back for the duration of the conversion, then unloaded" rather than leaving a state claim -> OWNER + lane wording.
- [MINOR] docs/archive/work/complete/WI-555-wi508-partial-close.md:80 -> arm 2's "`docs/ratify/CURRENT.md` regenerated on trunk after the merge" is not literally what happened -> `git log --oneline 6d3d9db4..551d1b2c -- docs/ratify/CURRENT.md` returns only `d8848bf4`, a BRANCH commit made before `979c3e5f`; no trunk commit after the merge touches it. The intent is satisfied — `979c3e5f` records "trunk was already an ancestor of this branch, so ... its tree IS the branch tip's", and `trace.py --approve modified --check` on this tree returns "is current" -> reword the Deliverable to "regenerated on the branch with the WI-554-fixed renderer and current on trunk after the trivial merge" (it already says the second half at :39) -> LANE (wording).
- [MINOR] docs/log.d/WI-555-wi508-partial-close.md:1 and :89 -> two fragment-accuracy defects: no file-level `Deferred open items:` line (the WARN-level convention `gen_open_items.py` documents at :975-:1081), and "**Phantom head cleared**: `check_trajectory: clean`" overstates -> `grep -n "Deferred open items"` returns nothing; `check_trajectory.py` exits 0 but emits 53 WARNs, and `--strict` exits 1 on the WI-564 seam error -> add `Deferred open items: none` (or the true list) and narrow the claim to what was measured: the OI-70 hold-by-rename WARN is gone and no WI-508 row remains. No `fig:` finding — the fragment drives no figures -> LANE.
- [MINOR] git 6ba27110 -> the un-close moved a spec between status directories with a bare `git mv` rather than `spec_move.py`, whose docstring exists precisely because "a bare `git mv` of a probe spec took the broken-link count from 4 to 8" -> `git show 6ba2711078 --stat` is a single rename, 0 insertions; `check.py` reports `doc-navigability PASS`, so nothing was stranded this time, and OI-71 sanctioned the manual special case -> no lane rework. Construction-first: rather than a check for un-scripted moves, add the reverse `archive/work/complete -> active/<branch>` un-close as a fourth named move on `spec_move.move_spec`, so the only way to perform it is the link-safe one -> kit row (WI-568 may draft it, or a fresh row).
- [MINOR] docs/work/queued/WI-568-dispose-the-close-recorded-at.md:3 -> the minted Title is 184 characters and trips a bound this close introduced -> `check_trajectory: WARN - 2 open work item(s) carry a Title over 120 characters ... WI-568 (184 chars)` -> trim the Title and move the R3 vocabulary into the body; construction-first: `intake.py`'s derived-description path should truncate to the declared bound at mint rather than emit a row that immediately warns -> LANE or WI-568, plus a kit row for the mint path.
- [MINOR] docs/handbacks/WI-508-wi508-architectural-remap.md:34 -> the report asserts "The closing party could not judge this work — a dispatcher closing a lane whose worker exited or crashed has no view of it", which is false of this close: a supervised session executing a ruling closed it with full view and chose `split_decided_by = "adjudicator"` deliberately -> the sentence is `station.render_report` boilerplate keyed off `split_decided_by`, not authored, so it is a kit defect rather than a lane one -> route to a kit row: the boilerplate should state the deferral, not invent a reason for it -> kit row.

VERDICT: CHANGES-REQUESTED findings=9
