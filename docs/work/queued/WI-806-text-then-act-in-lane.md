+++
id = "WI-806"
title = "Spine text before the act, enforced on every lane commit"
workstream = "process"
specref = "docs/plans/2026-10-04-wi788-design/README.md#s788-text-then-act"
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand by the coordinator on 2026-10-04 from WI-788's approved design note
(OI-104, ruled 2026-10-04). This is S788-text-then-act (ch.4 §7, §11; risk 6). A
commit that writes under `docs/archive/last_approved/` must, against its first
parent, change no spine cell except `Status` and add or remove no row: text first,
the act second. By the owner's README Q-8 answer, one function over two trees
enforces it in the lane, at the pre-commit hook and again by the landing on each
lane commit (so a `--no-verify` commit is still refused); the landing's own squash
is exempt, and any other commit made directly on trunk is still checked at the hook
(README change 27). "Amend-plus-flip is approval" retires everywhere (change 13):
the allowance at `baseline_snapshot.py:851-853`, the refusal text, IF-129's
"re-attest it in this commit", and PROCESS.md:488. Flips and their copy stay one
commit (SR-140).

## Done-when

- A mixed commit is refused at pre-commit.
- A `--no-verify` lane commit is refused at the landing's per-commit check.
- The two-commit form is accepted.
- No refusal text offers amend-plus-flip.
- A direct trunk commit is checked at the hook like any commit.
- Each spine row the README matrix gives this row (LLR-173/178/245, TC-167/173,
  IF-129; a new separation row) is amended or added and passes adjudication of that
  row, on whichever adjudication path is the one path when this row lands.
- The row's test bar: its affected modules' tests (snapshot and acceptance) plus
  the smoke tier at `-n 2`; no extra bar is named.
- Review bar: A+B (REVIEW-A plus an independent REVIEW-B).
- RESYNC_PACK: an entry anchored at a trunk commit; the owner's held-rung approvals
  become two commits.
