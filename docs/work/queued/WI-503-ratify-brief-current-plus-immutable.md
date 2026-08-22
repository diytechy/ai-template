+++
id = "WI-503"
title = "The re-attestation brief splits: a regenerated CURRENT.md plus dated briefs that are immutable once minted"
specref = "docs/log.d/2026-08-21-wi498-stage-unification.md"
workstream = "scripts"
sr_refs = ["SR-178"]
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

Minted at the WI-498 program close from ROUND-OPUS finding 13, assessed
there as too large to fold into the close (it moves a gate that
deliberately fails CLOSED because a human is about to attest) and recorded
as a row rather than a deferral.

**The defect.** `docs/ratify/*.md` briefs are DATED and NAMED for the
sitting that minted them, and are read as the record of what was owed at
that moment — but `trace.py --ratify modified` regenerates the NEWEST brief
IN PLACE (`newest_ratify_brief` picks the newest by filename, and
`ratify_check` regenerates and byte-compares it). So a dated file keeps
being rewritten until a newer date is minted.

Measured: `docs/ratify/2026-08-13-wi444.md` is dated 2026-08-13 and named
for WI-444, and its content at the WI-498 close was the WI-498 drift —
`SR-049`/`SR-140`/`SR-170`/`SR-173` sections, a baseline stamped
`2026-08-20 (a5471e0f)` and an approval provenance of `1a7984ea
(2026-08-21)` — with nothing about WI-444 in it. `git log` on that path
shows **ten** rewrites; `c170da9f` alone added 77 lines to it.

This is pre-existing machinery behaviour, NOT something WI-498 introduced.
It is filed here because the program wrote into that file and because an
attestation record that is mutable until superseded cannot answer the one
question it exists for: *what was the human shown when they signed?*

**The design (Opus's, adopted as the spec).**

- `--ratify modified` regenerates an UNDATED `docs/ratify/CURRENT.md` — the
  live surface, always the working tree's answer, and the artifact the
  `ratify-fresh` freshness gate compares. That gate keeps its fail-closed
  posture and its reason: a stale brief is read by a human about to attest.
- A DATED brief is MINTED from `CURRENT.md` at a sitting and is IMMUTABLE
  once written. Regeneration never touches a dated file again.
- The immutability needs an enforcer, or it is a convention that rots like
  the byte baselines did: a check that refuses a commit whose diff modifies
  an existing `docs/ratify/<date>-*.md`, with the mint itself the one
  permitted writer.

**Surfaces this moves, so the size is not rediscovered mid-flight:**
`trace.newest_ratify_brief` / `ratify_check` / `reattest_lines`;
`check.py`'s `ratify-fresh` step; the `[generated]` census row
`docs/ratify/ = ratify` in `docs/stack.ini` (it declares a PREFIX, which
would now cover one regenerated file and N immutable ones — the
staged-divergence detector reads that same row); `gen_open_items`, which
renders the baseline/attestation-depth summary; `bootstrap.py` MAPPING and
`tests/test_bootstrap.py` file lists if the scaffold ships a seed brief;
the existing dated briefs, which stay exactly as they are (they are
history, and rewriting them is the defect); and a RESYNC_PACK entry,
because an adopter's `docs/ratify/` layout changes.

## Done-when

- `--ratify modified` writes `CURRENT.md`; no dated brief is ever rewritten
  by a regeneration, driven as a test.
- A test asserts the immutability enforcer REFUSES a modification to an
  existing dated brief and PERMITS the mint.
- `ratify-fresh` still fails closed on a stale `CURRENT.md`.
- `docs/stack.ini`'s `[generated]` row and the staged-divergence detector
  agree with the new layout.
- RESYNC_PACK entry written; `check_docs --stale` 0 broken.
