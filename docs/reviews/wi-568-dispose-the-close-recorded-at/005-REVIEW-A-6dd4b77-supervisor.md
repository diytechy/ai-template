### REVIEW-A — WI-568 — Round 005 — 2026-09-01 — supervisor-drawn verification (independent Opus)

Tree: `/Users/diytechy/Documents/ai-template-drive/wi-568-dispose-the-close-recorded-at`
@ `6dd4b77d` (record-only rework); round-004 file committed at `58e36852`.
Python `/Users/diytechy/Documents/ai-template/.venv/bin/python`.

## What I verified

**The draft still parses, and the long `one_line` survives the mint intact.**

```
intake.parse_dispositions(<closed spec>) -> refusal: None ; n: 1
keys: ['buildtier','kind','open_item','planmode','priority','supersedes','title','workstream']
title 111 ; tier strong ; kind spine ; scope 5559 chars ; 'OWNER BRIEF' -> True
owes_successor True ; _mint_shape_refusal -> None
open_item (one_line) len 809
intake._clip(q, 100) -> len 100, tail '…toml, and component…'
tomllib round-trip of the minted table -> title 100, one_line 809, one_line == q
trace.truncate_cell(q) -> len 809, truncated? False   (CELL_TRUNCATE_LIMIT = 1500)
```

`_mint_open_item` (intake.py:335-341) clips only the `title` — with the explicit
`…` marker `_clip` writes — and passes the full question to `one_line`; there is
no length refusal anywhere on that path. `gen_open_items`' HTML card renders
cells through `trace.truncate_cell`, whose limit is 1500, so at 809 chars the
question renders WHOLE, and had it exceeded the limit the cut would have been
labelled ("… [N more chars — read the registry row]"), never silent.

**The mirror-invariant claim is exactly right.**
`acceptance_record.committed_snapshot_findings` (acceptance_record.py:701-729)
asks "was it a copy of its live counterpart at the commit that last wrote it?",
pinned to the writing commit — its own docstring: "a legitimate copy stays green
forever and a forgery stays red forever." So writing the `6d3d9db4` bytes into
the snapshot at a new commit where live differs is red at that commit and stays
red; a later reseal does not clear the landed one. The lane's own record
confirms the measurement: `docs/decisions-for-review-2026-08-31.md:221` (under
"## 10.") — "Restoring the `580df781` snapshot beside a `Drafted` live row makes
`trace.py --strict-integrity` red … Both were tried, both reverted." The brief
cites both correctly.

**The external.toml correction is now right.** The question and the blast radius
name it as a comment correction, not a row, matching
`git diff 6d3d9db4 HEAD -- docs/archive/last_approved/docs/requirements/external.toml`
(12 ++/--, one hunk in the `status` header comment, written by `580df781`).
interfaces 132/30/3 with the ten rulings and components 1 changed (WI-520) still
match `git show 6d3d9db4:docs/ratify/CURRENT.md`.

**My round-004 MINOR is answered — by removal, not by patching.** The
integrity-red cost I asked to be disclosed belonged to RESTORE; RESTORE is gone,
and the new *Reversal cost* ("STAND then review later: any row can still be
amended live at any time and re-enters the brief … REVIEW-THEN-STAND: the
amendments are ordinary edits; the reseal is one `intake.py snapshot` commit")
is true of the two options that remain.

**Harness on this tree.** `gen_open_items.py --root . --check` -> "open-items
view up to date", exit 0. `check_trajectory.py` -> exit 0. `trace.py
--strict-integrity` -> `integrity=0 … interface-findings=0 provenance-findings=1
paraphrase-advisories=3`, exit 0 (the three pre-existing LLR-181/LLR-197/SR-168
advisories).

**Fragment.** The Round 004 section records both corrections accurately, quotes
the diff figures I measured, and notes honestly that the ADJUDICATE files still
read "STAND or RESTORE" as records of what each session ruled.

## Findings

- [MINOR] docs/work/complete/WI-568-dispose-the-close-recorded-at.md:64 -> "the amended row then drifts from the snapshot and returns to the re-attestation brief for an explicit act" overstates what an OFF-SPINE amendment arms -> `trace.py:3841-3857` is explicit that the off-spine tiers "never reach" `reattest_lines` and that the census "IS A DISCLOSURE SURFACE, NOT A NEW GATE — it changes nothing `owes()` tests", rendered "at FILE grain … not the fuller per-row diff"; `baseline_snapshot.is_drifted` is the spine predicate (it splits cells through `check_trajectory.split_changed_cells`) and `reattest_model` emits one section per SR, so an amended `interfaces.toml` row returns as a COUNT in `offspine_census_rows` ("N changed, M added, K removed; ruling(s): …") and arms no act at all — `docs/ratify/CURRENT.md`'s own title is "Re-attestation brief — **spine rows owing a human act**". The literal claim in the minted `one_line` ("returns it to the re-attestation brief") is true, since the census is a section of that document; only the scope prose's "for an explicit act" is wrong -> drop "for an explicit act" and say instead "the amended row re-enters the off-spine census as a changed-row count with its ruling pointer; off-spine rows arm no per-row attestation, so the owner's read of the diff IS the act"; not mechanizable — the sentence describes a surface's behaviour in prose, and no check can compare a claim about a renderer to the renderer -> @worker
- [MINOR] docs/work/complete/WI-568-dispose-the-close-recorded-at.md:36 -> the diff command the owner is told to run over-selects: it returns a spine registry alongside the three off-spine ones -> `git diff --stat 6d3d9db4 551d1b2c -- docs/archive/last_approved/docs/requirements/` -> `components.toml | 2 +-`, `external.toml | 12 +-`, `interfaces.toml | 1822 ++++----`, **and `low-level-requirements.toml | 42 +-`** (the LLR-203/204 approval snapshot — a separate, already-ruled KEEP decision), 990 insertions / 888 deletions over four files; the brief presents the command's output as the absorbed off-spine content while also stating "Nothing on the spine (LLR/TC) moves under either answer", so the owner meets 42 lines of spine snapshot the question does not cover -> name the three paths in the command: `git diff 6d3d9db4 551d1b2c -- docs/archive/last_approved/docs/requirements/interfaces.toml docs/archive/last_approved/docs/requirements/external.toml docs/archive/last_approved/docs/requirements/components.toml`; unmechanizable for the same reason — a pathspec inside a free-text owner card is prose, and the fix is to derive it from the census's own file list rather than from a directory -> @owner

VERDICT: APPROVE findings=2
