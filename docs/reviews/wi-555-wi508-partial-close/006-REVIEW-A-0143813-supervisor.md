### REVIEW-A — WI-555 — Round 006 — 2026-09-01 — supervisor-drawn verification (independent Opus)

Tree: `/Users/diytechy/Documents/ai-template-drive/wi-555-wi508-partial-close` @
`01438132` (round-005 file committed at `ac5af23a`; the rework at `01438132`).
Python: `/Users/diytechy/Documents/ai-template/.venv/bin/python`. `git status
--porcelain` is empty. Scope: does each round-005 remedy routed to the LANE now
stand in the record, accurately? A correction that misstates a fact is a new
finding.

## What I verified

**The rework is record-only, as claimed.** `git show 01438132 --stat`:

```
 docs/archive/work/complete/WI-555-wi508-partial-close.md    |  32 ++++++-
 docs/log.d/WI-555-wi508-partial-close.md                    | 101 +++++++++++++
 docs/work/queued/WI-568-dispose-the-close-recorded-at.md    |   6 ++
 3 files changed, 135 insertions(+), 4 deletions(-)
```

`docs/handbacks/` and every registry untouched — correct, the report is immutable.

**MAJOR 1 (snapshot absorption) — DISCHARGED.** The Deliverable's "Corrected by
round 005 (2026-09-01)" paragraph and the fragment's new section both carry every
piece of evidence I asked for: the pre-merge anchor named as
`6d3d9db4:docs/archive/last_approved` "(last written at `13593db9`)" — matches
`git show 6d3d9db4:docs/ratify/CURRENT.md` -> "_Baseline: … copied 2026-08-24
(13593db9)_"; the branch writers `580df781` / `4824c0ba` — matches `git log
--oneline 6d3d9db4..551d1b2c -- docs/archive/last_approved/`; the census figures
"132 changed, 30 added, 3 removed" -> "1 changed, 0 added, 1 removed (WI-553)" —
verbatim from the two briefs; and the fragment quotes the two commands with the
`6 files changed, 1029 insertions(+), 893 deletions(-)` stat, which reproduces.
The spec at :44 now reads "The branch's `docs/archive/last_approved/` bytes,
however, already landed with the merge … what remains downstream is the ruling on
them" — the sentence round 005 called false is gone. Ownership is stated
correctly and in both places: "whether trunk's baseline is restored to the
`6d3d9db4` bytes or the absorption stands is the OWNER's ruling, carried as a
named part of WI-568's `580df781` keep/discard."

**The authority claim in the correction is TRUE, and I checked it rather than
taking it.** The fragment asserts the interfaces/components (Arch rung) and
external (Boundary rung) registries are loop-approvable at this dial:

```
agent_common.APPROVAL_RUNGS = {"external": "DevStg-Boundary",
                               "interfaces": "DevStg-Arch",
                               "components": "DevStg-Arch"}
agent_common.human_approves(Path('docs'), r) ->
  interfaces False   external False   components False
```

`docs/process.toml:78-95` puts `DevStg-Needs` one rung ABOVE `DevStg-Below` and
below Boundary/Arch, and `human_approves`' own docstring says "At this repo's
`DevStg-Needs` dial that is none." No authority breach — as stated.

**MAJOR 2 (the report's misstatement) — DISCHARGED.** The correction names the
sentence, the true split, and the corroborating artifact, and all three check
out: `docs/work/partial/WI-508-architectural-remap-program.md:24` does read "The
two **LLRs are `Approved`**; the two **TCs are `Drafted`**", and `git show
551d1b2c:docs/requirements/low-level-requirements.toml` gives LLR-203/LLR-204
`status = "Approved"`. It correctly leaves the immutable report alone and says
so. WI-568's Context repeats it as a named item.

**MAJOR 3 (arm 4) — DISCHARGED, and correctly routed.** The fragment states the
arm was false as written, attributes the premise to OI-72's own "four Drafted
rows" phrasing, cites `drafts` 11 -> 9, and routes stand-or-revert to WI-568 with
the OI-72 wording to the owner. WI-568's Context now carries: "the `580df781`
keep/discard explicitly includes the LLR-203 / LLR-204 `Drafted` -> `Approved`
flips: stand or revert … the flip is loop-permitted under
`human_approval_through = "DevStg-Needs"`, so the question is disposition, not
authority." Accurate.

**The `open_item` route WI-568's Context names is real** — I checked, because a
correction that invents a mechanism is worse than the defect.
`project-trajectory/scripts/intake.py:1476` `_inject_open_item` — "OI-73 exit
(B): where a draft names a human-owed `open_item`, mint a …", called from
`:1512`; `project-trajectory/prompts/adjudicate-disposition.template.md:44`
documents the cell. (OI-70's "exit (B) has no sanctioned path" has since been
built.) One nuance the adjudicator should know: that template says `open_item` is
"a TYPED DEPENDENCY of the successor, never a standalone exit", so the OI must
hang off the drafted re-land successor — which WI-568 will draft anyway.

**MINOR 4 (arm 1 wording) — FIXED.** Spec :30 now reads "renamed back" to match
the trunk claim "for the duration of the conversion, then unloaded after the
merge", and the correction paragraph adds the origin `-HELD-` ref as owner-owed
under `push = "human"`. Still true on this tree: `git for-each-ref | grep -i
wi508` -> one ref, `refs/remotes/origin/wi508-architectural-remap-HELD-for-owner-verdict fa3c99c4`.

**MINOR 5 (arm 2 wording) — FIXED.** Spec :41 now reads "regenerated on the
branch with the WI-554-fixed renderer (`d8848bf4`) and is current on trunk after
the trivial merge". Matches `git log --oneline 6d3d9db4..551d1b2c --
docs/ratify/CURRENT.md` -> `d8848bf4` only.

**MINOR 6a (the file-level declaration) — ACCEPTED BY THE CHECKER.**
`gen_open_items.py --root . --check` -> `gen_open_items: open-items view up to
date.` (exit 0). The line sits at `docs/log.d/WI-555-wi508-partial-close.md:11`,
in the top matter above the first `###`.

**Nothing regressed.** `check.py --jobs 0` -> `RESULT: PASS` (11 steps,
`doc-navigability PASS`, `approval-immutable PASS`). The Deliverable still parses:
`grep -n '^## '` -> `13:## Deliverable`, `77:## Context`, `95:## Done-when` — the
correction paragraph sits inside `## Deliverable`, above `## Context`, as
required.

## Findings

- [MINOR] docs/archive/work/complete/WI-555-wi508-partial-close.md:61 and docs/work/queued/WI-568-dispose-the-close-recorded-at.md:22 -> both corrections say the collapsed census spanned "across nine rulings"; it spans ten -> `git show 6d3d9db4:docs/ratify/CURRENT.md` lists `ruling(s): OI-64, OI-65, OI-67, WI-522, WI-528, WI-530, WI-531, WI-533, WI-534, WI-553` — ten ids (counted programmatically: `len(s.split(', ')) -> 10`). The error originated in round 005's own prose and was inherited faithfully; the fragment's own enumeration at the same point lists all ten correctly, so only the two summary sentences are wrong -> change "nine" to "ten" in both places (or drop the count and point at the enumerated list, which is what the fragment already does) -> LANE.
- [MINOR] docs/archive/work/complete/WI-555-wi508-partial-close.md:50 -> the Deliverable's numbered item 4 still asserts "`check_trajectory` is clean" and the "Corrected by round 005" paragraph, which covers the snapshot, the report, arm 1 and arm 2, does not narrow it -> the narrowing exists only in the fragment at :248 ("the '`check_trajectory: clean`' claim overstates … exits 0 with 53 WARNs, and `--strict` exits 1 on the pre-existing WI-564 seam ERROR"), which I re-confirmed on this tree. The spec is the surface a reader reaches first -> add one clause to the correction paragraph, or narrow item 4 in place to "no WI-508 row remains and the OI-70 hold-by-rename WARN is gone" -> LANE.
- [MINOR] docs/log.d/WI-555-wi508-partial-close.md:11 -> `Deferred open items: none` is arguably not `none`: this session defers an owner-owed question (restore-or-stand on trunk's baseline) -> the declaration's own trailing clause concedes it — "the restore-or-stand ruling is routed through WI-568's disposition adjudication, which mints an OI through its own `open_item` cell if the adjudicator judges it owner-owed; a lane may not allocate an OI id". The reasoning holds (`_inject_open_item` is the mint path and it runs at intake, not in a lane) and OI-70 named this exact hazard: "A sitting can honestly write `none` while holding a lane for the owner, and nothing contradicts it." Warn-level convention, explicit routing, so MINOR -> no rework required; construction-first: the declaration should be a two-valued field where "deferred to a named row" is a first-class value, so a session cannot be forced to choose between `none` and an id it may not allocate — which removes the class rather than checking prose -> kit row (WI-568 may draft it), not the lane.
- [MINOR] docs/work/queued/WI-568-dispose-the-close-recorded-at.md:3 -> the 184-character Title this close minted still trips `check_trajectory: WARN - … WI-568 (184 chars), WI-545 (129 chars)`; the rework routed it to a kit row and left the frontmatter untouched by design -> the WARN is still emitted on this tree. Leaving an intake-derived cell alone is a defensible call and the round-005 route offered it, so this is not rework owed -> WI-568 or a kit row for `intake.py`'s derived-Title truncation.
- [MINOR] docs/log.d/WI-555-wi508-partial-close.md:255-266 -> the three kit findings (the missing `spec_move.move_spec` un-close direction, `intake.py`'s untruncated derived Title, `station.render_report`'s invented `split_decided_by` reason) are recorded only in a log fragment that compiles into `docs/log.md`; no row on any work surface carries them -> `ls docs/work/queued/` shows no new row, and correctly so — a lane never mints a WI id (WI-388 R1), so the fragment was the only act available -> WI-568's `## Dispositions` should draft them (or the next trunk bookkeeping mint should), otherwise three named kit defects live only in the log -> WI-568.

No MAJOR or BLOCKER remains. All three round-005 MAJORs are discharged in the
record with the evidence asked for and no new misstatement of substance; the two
lane-owed MINOR wordings are fixed; the five findings above are one inherited
arithmetic slip, one place the narrowing did not reach, and three routing
observations that are not the lane's rework.

VERDICT: APPROVE findings=5
