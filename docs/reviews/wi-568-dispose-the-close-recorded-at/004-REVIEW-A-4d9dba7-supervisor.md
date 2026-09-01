### REVIEW-A — WI-568 — Round 004 — 2026-09-01 — supervisor-drawn verification at the closed tip (independent Opus)

Tree: `/Users/diytechy/Documents/ai-template-drive/wi-568-dispose-the-close-recorded-at`
@ `4d9dba7f` (`adjudicate: WI-568 -> complete/ (mechanical close)`), rework at
`d5dda201`. Python `/Users/diytechy/Documents/ai-template/.venv/bin/python`.
Hostile pass over the OWNER BRIEF's facts, since that block is what an owner
will rule from.

## What I verified

**(1) The close and the moved spec — CLEAN.** `docs/work/active/` no longer
exists; the spec is `docs/work/complete/WI-568-dispose-the-close-recorded-at.md`.
`grep -n '^## '` -> `11:## Deliverable`, `15:## Context`, `29:## Dispositions` —
Deliverable precedes Context, as `_adjudication_close_text` writes it, and
`specref` is cleared to `""`. The block survived the move byte-intact:

```
intake.parse_dispositions(<moved spec>) -> refusal: None ; n: 1
keys: ['buildtier','kind','open_item','planmode','priority','supersedes','title','workstream']
title len 111 ; tier strong ; kind spine ; sup WI-508 ; pm single ; pri 2
open_item len 512 ; scope chars 4950 ; 'OWNER BRIEF' in scope -> True
intake.owes_successor(meta)       -> True
intake._mint_shape_refusal(draft) -> None
```

`_disposition_drafts` reads exactly this path (`_terminal_hits(root,
"complete", …)`), so the mint will find it at the merge.

**(2) OWNER BRIEF facts — two of three right, one wrong.**
`git show 6d3d9db4:docs/ratify/CURRENT.md` renders the pre-merge census as
`interfaces.toml — 132 changed, 30 added, 3 removed … OI-64, OI-65, OI-67,
WI-522, WI-528, WI-530, WI-531, WI-533, WI-534, WI-553` and `components.toml —
1 changed, 0 added, 0 removed … WI-520`. Both the `open_item` cell and the
brief now split them correctly, and name `WI-520` — round 003's MINOR is
discharged. The `external.toml` claim does not hold; see the finding.
The RESTORE recommendation IS argued from the record, not asserted: it grants
that STAND is within authority (`DevStg-Needs` leaves the Arch and Boundary
rungs loop-approvable — matches `agent_common.APPROVAL_RUNGS` +
`human_approves`), and rests on a checkable fact — the rows "entered the
baseline as a side effect of a `partial` lane's handback merge, not as an
approval act", which `git log --oneline 6d3d9db4..HEAD --
docs/archive/last_approved/` confirms (`4824c0ba`, `580df781`, both wi508
BRANCH commits).

**(3) The Terra MAJOR — honestly answered within the lane's reach.** I read
`intake._mint_open_item` (intake.py:317-348): it writes `title` (clipped to
100), `status = "pending"`, `raised`, `one_line`, `wi_refs` — exactly the five
the finding names, and nothing else. The lane cannot widen that without editing
kit code, which an adjudication lane may not do. The rework's answer — carry
the brief in the successor's captured scope, which the OI row reaches through
`wi_refs`, and file the typed-`[open_item]`-table fix as a construction-first
kit finding so a thin card becomes unrepresentable — is the right shape and is
stated as such in the fragment.

**(4) Fragment claims vs the session record — MATCH.** `git log --grep="session
wi-568"`: `...-003 DESIGN-CHECK COMMITTED`, `...-004 ADJUDICATE COMMITTED`,
then `005 NO-COMMIT`, `006 ERROR`, `007 WAITING` — so "003 DESIGN-CHECK and 004
ADJUDICATE", "neither closed the row", and the C6 resume-cycle account are all
accurate. Both files carry exactly one `^OUTCOME:` line, `PARTIAL successors=1`,
concurring on PARTIAL / keep-all / one `strong` `single` successor /
owner-owed baseline. "Session 004 tidied the `open_item` text" checks out:
`git show 0d300eff` is the commit that replaced the bundled phrasing with the
split interfaces/components attribution. (Note only: the DESIGN-CHECK session's
artifact is filed as `003-ADJUDICATE-9d4fc41.md`; the fragment's prose is the
accurate record of the two.)

**(5) Harness on this tree.**

```
gen_open_items.py --root . --check -> "open-items view up to date."   exit 0
check_trajectory.py                -> "clean (565 work item(s), 525 done (93%),
                                       21 cancelled, graph acyclic)"  exit 0
trace.py --root . --strict-integrity -> "integrity=0 … interface-findings=0
                                       provenance-findings=1
                                       paraphrase-advisories=3"       exit 0
```

The WI-568 active-row trailer WARN of round 003 is gone (the row is now done).
All three residual advisories are the pre-existing LLR-181/LLR-197/SR-168 ones.

## Findings

- [MAJOR] docs/work/complete/WI-568-dispose-the-close-recorded-at.md:82 -> the OWNER BRIEF's blast-radius states "external.toml is unaffected either way", which is false: its baseline WAS moved by the absorption, and the RESTORE branch the same brief recommends would revert a substantive correction -> `git log --oneline 6d3d9db4..HEAD -- docs/archive/last_approved/docs/requirements/external.toml` -> `580df781` (a wi508 BRANCH commit), and `git diff 6d3d9db4 HEAD -- <same>` -> `12 ++++++++----` (8 insertions, 4 deletions), the whole hunk inside the `status` field's header comment: the pre-merge bytes assert "At this repo's dial of 4 that means every value here is the OWNER'S to flip … No loop, no LLM verdict and no script may set one to `Approved`", and the absorbed bytes replace that with "READ THE DIAL, DO NOT ASSUME IT: this repo runs `DevStg-Needs`-held only, so DevStg-Boundary is NOT held and the predicate answers FALSE" — the correct statement, and the one the brief's own authority paragraph relies on. The scope prose's RESTORE branch instructs re-copying all three `6d3d9db4` files by name, so acting on the recommendation puts a claim the repo has since corrected back into the approved baseline, while the owner was told nothing changes -> narrow the RESTORE branch to `interfaces.toml` and `components.toml` (the two with a row-level census) and replace the blast-radius clause with "external.toml carries no row-level census, but its baseline comment WAS corrected by `580df781`; RESTORE must not revert it"; this cannot be made unrepresentable — the brief is free prose summarising a diff, and only re-deriving the diff catches a wrong summary, which is why the cell must quote the census and the file list must be derived from it -> @worker
- [MINOR] docs/work/complete/WI-568-dispose-the-close-recorded-at.md:97 -> "*Reversal cost.* … Neither loses anything" omits the one real interim cost of the recommended option -> `acceptance_record.py:775-781` reports a snapshot that is not byte-identical to live at the commit that last wrote it as a LANDED divergence ("the snapshot is the record of what a human blessed, so it may only ever be written by copying the live file (`intake.py snapshot`). This divergence has LANDED"); live `external.toml` and its baseline are byte-identical today (`diff` -> no output), so RESTORE deliberately creates that state — and this is not hypothetical: `docs/decisions-for-review-2026-08-31.md:222` records the wi508 lane trying exactly this restore and reverting it because `trace.py --strict-integrity` went red -> add one clause: "RESTORE leaves the snapshot deliberately non-byte-identical until the owner's explicit act and the reseal, a state `--strict-integrity` reports (tried and reverted on the lane, decision 10)"; not mechanizable for the same reason as above — a cost the prose omits is invisible to any check -> @owner

VERDICT: CHANGES-REQUESTED findings=2
