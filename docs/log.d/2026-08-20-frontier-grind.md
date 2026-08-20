## 2026-08-20 — The frontier grind, in series (owner directive): per-WI record

The owner's 2026-08-20 directive: grind the open frontier in series with
opus/sonnet workers, one large adversarial review (internal Opus +
cross-family Sol via codex) at the end, consolidated and iterated in one
action. One entry per WI as it closes; adjacent findings accumulate at the
bottom for the closing review.

### WI-474 — the hats→spine_carrier seam (opus worker) — CLOSED complete

IF-133 minted (carrier-consumption shape per IF-118/119/120/122; owner
LLR-166, carried_by IF-102, req_refs SR-147, CMP-008, Drafted); two
consumer-side contract tests added and driven negative; `Contracts: IF-133`
docstring line; watermark IF 132→133; snapshot re-taken byte-identical.
`check_trajectory --strict` EXITS 0 — the first all-green strict trajectory
run on record. Worker's full suite: 2592 passed / 13 skipped in 492.66s
(one environmental posix-shell gate re-run gated).
<!-- fig: cmd="python -m pytest -q -n auto" rev=6a6d866d -->

### Adjacent findings accumulating for the closing review

- (WI-474 worker) `check_vocab.py:71` declares `Contracts: IF-118`, which is
  NOT its row (IF-118 is gen_open_items→spine_carrier) — and the checker
  verifies only that a cited id EXISTS, never that the row names the citing
  module: a `Contracts:` line can cite any live IF id and be believed. Real
  checker hole.
- (WI-474 worker) LLR-168's detail/code_symbol omit hats.py's entire `audit`
  subcommand (~170 lines incl. the newly declared seam) — Approved row, so
  the coverage amendment is owner-adjacent.
- (WI-474 worker) IF-118/119/120 `notes` cite a retired CMP numbering
  ("this module is CMP-002...") — stale, reads authoritative.
- (step-7 worker) `intake._apply_flips` now writes nothing — whether any
  mechanical ratification authority returns is an owner policy call
  (docstring carries both candidates).
