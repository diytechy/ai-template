## 2026-09-01 — WI-568: the wi508 partial close adjudicated — keep-all, the LLR approvals kept, the baseline question minted for the owner

Deferred open items: none nameable from a lane — the owner-owed restore-or-stand question is DRAFTED as the `open_item` cell of this row's ## Dispositions block and is minted with its id at merge by intake._inject_open_item; a lane may not allocate an OI id.

### What was judged

The disposition of the WI-508 partial close recorded at
[`../handbacks/WI-508-wi508-architectural-remap.md`](../handbacks/WI-508-wi508-architectural-remap.md).
Verdict: **PARTIAL stands**, `keep=all` on the whole `ff29fef8f9..6ba2711078`
range (already on trunk via the sanctioned manual close WI-555 merged), and one
successor drafted. The verdict file is
[`../reviews/wi-568-dispose-the-close-recorded-at/001-ADJUDICATE-4632f10.md`](../reviews/wi-568-dispose-the-close-recorded-at/001-ADJUDICATE-4632f10.md).

Two judgements the row's own Context named are now on the record explicitly
rather than by omission: the `580df781` `LLR-203`/`LLR-204`
`Drafted` -> `Approved` flips are **KEPT** (loop-legal at this repo's
`DevStg-Needs` dial, and the rows are byte-identical to the round-010-approved
tree), with `TC-199`/`TC-200` staying `Drafted`; and the
`docs/archive/last_approved` restore-or-stand question is ruled **owner-owed**
and minted as an open item through the successor's `open_item` cell.

### The round-002 rework, and why each finding was real

[`../reviews/wi-568-dispose-the-close-recorded-at/002-REVIEW-A-8b75283-supervisor.md`](../reviews/wi-568-dispose-the-close-recorded-at/002-REVIEW-A-8b75283-supervisor.md)
returned CHANGES-REQUESTED findings=7. All four BLOCKER/MAJOR findings were real:

- **BLOCKER (misplaced block).** The `## Dispositions` block sat in the VERDICT
  file. `handback.close_adjudication` and `intake._disposition_drafts` both parse
  the SPEC, so `parse_dispositions` on the spec returned `([], None)` against
  `owes_successor -> True`: the close would have been refused and the successor
  never minted. The block now lives in the spec; the verdict says so in one line.
- **BLOCKER (owner-owed by omission).** The verdict declared the successor "not
  owner-owed" without ever judging the baseline question, while drafting a reseal
  that makes the absorption permanent. Now ruled: content keep-all, baseline
  question to the owner as a minted OI.
- **MAJOR (decision-9 miscitation).** OI-71 decision 9 measured `intake.py
  snapshot` **on the lane against the lane's own pre-merge live state** —
  branch-local self-consistency, pre-merge. It says nothing about trunk's
  absorbed off-spine rows. Round 002 measured the live-vs-baseline drift that
  does bear on it: 2269 / 14 / 4 diff lines for
  `interfaces.toml` / `external.toml` / `components.toml` at `6d3d9db4`, and
  16 / 0 / 0 now — trunk's live registries ARE the absorbed content, so a reseal
  re-blesses the 132 changed / 30 added / 3 removed rows rather than re-opening
  them.
- **MAJOR (unexecutable successor).** `parse_dispositions` captures only the
  prose AFTER the fence; the reasoning paragraph sat before it, so the mint's
  Context would have carried `OUTCOME: PARTIAL successors=1` and nothing else.
  The executable scope is now authored after the closing fence (3,027 chars),
  verified through `intake.parse_dispositions` / `intake._mint_shape_refusal`,
  both clean.

### The successor

Drafted in this row's `## Dispositions` section (a lane drafts, the merge mints):
same title, `workstream = "process"`, `safety_class = "spine"`,
`planmode = "single"`, `priority = 2`, `supersedes = "WI-508"`, and
`buildtier = "strong"` — the round-002 MINOR was right that `quick` under-tiers a
worker who re-confirms spine rows and rewrites the approval baseline. Its scope:
one clean cross-family reviewer round on current trunk over the four rows; then,
under the owner's ruling, either `intake.py snapshot` at its own approval commit
("stand") or a re-copy of the `6d3d9db4` off-spine snapshot bytes in a reviewed
commit ("restore"). It inherits OI-72's SR-163 ruling.

### The three MINORs

Two are folded into the re-issued verdict: the "governing round-10 APPROVE"
claim is corrected (rounds 011–019 re-opened it; the lane's standing verdict is
round 019 CHANGES-REQUESTED, discharged by WI-543/WI-554 — the narrower row-level
claim survives on a diff), and the tier raised to `strong`. The third is
discharged by routing: the two BLOCKERs of
[`../reviews/wi508-architectural-remap/010-REVIEW-A-5175065.md`](../reviews/wi508-architectural-remap/010-REVIEW-A-5175065.md)
against the on-trunk blind-map plan files are named as explicit items in the
successor's scope, so the adjudication does not close over them; its Team-A
census MINOR is explicitly left out of scope.

The verdict file was re-issued IN PLACE rather than appended to (the WI-566
precedent: the first `OUTCOME:` line governs and `docs/reviews/` carries no
immutability convention), and `OUTCOME: PARTIAL successors=1` remains its single
machine line.

### Round 002 (Terra, mechanized) — the thin open-item mint, answered in the record

After the rework the loop's resume scheduled a mechanized Terra round over the
train diff (`002-REVIEW-A-9d4fc41.md`): one MAJOR — the disposition's scalar
`open_item` mints an open-items row carrying only `title`, `status`, `raised`,
`one_line` and `wi_refs` (`intake._mint_open_item`), omitting the registry
contract's `decision`, `blast_radius`, `options` and `recommendation`, so the
owner would be handed a bare binary question. The lane cannot change the mint
(kit code is not an adjudication lane's to touch), so the brief is carried in
the record the OI row points at: an **OWNER BRIEF** block (blast radius under
each answer, both options, a recommendation — RESTORE — and the reversal
costs) now sits in the successor's captured scope, which the minted OI reaches
through its `wi_refs` -> the successor spec, and is summarised here.

Two further loop sessions (003 DESIGN-CHECK and 004 ADJUDICATE, both Sol under
the tripwire's family shift) re-adjudicated the same close and concurred on
every point (PARTIAL, keep-all, one strong-tier successor, the baseline
question owner-owed); session 004 tidied the `open_item` text to attribute the
interfaces/components census separately (round 003's MINOR). Neither closed
the row — the dispatcher resumed the finished lane in a cycle (the C6 shape)
until the supervisor stopped the loop and performed the mechanical close
through `handback.close_adjudication` by hand.

Kit findings for rows (construction-first): extend the disposition grammar
with a typed open-item table — `[open_item]` carrying `one_line`,
`blast_radius`, `options`, `recommendation` — that `_mint_open_item` writes
verbatim, so a thin owner card becomes unrepresentable rather than a thing a
reviewer must catch; and a DONE adjudication lane whose close is refused must
not be resumed as a fresh ADJUDICATE session — the refusal is the stop.
