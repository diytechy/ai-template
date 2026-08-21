# The batch is CLOSED — resume state for the next session

The iterate pass COMPLETED and is committed in three logical commits (see
`git log`: "review: bind the correction record to its ruling, keep a legacy
deny" → "review: close the thirteen MAJOR findings of the batch review" →
"review: sweep the seven MINOR findings"). All 22 WORKLIST items are
dispositioned — 21 FIXED, one (W-6's "seed baselines for the five kitlib
files" arm) REFUTED on measurement with the evidence in the close record.

Both Group-1 CRITICALs were proven against the reviewers' own executed
attacks, not against unit tests alone:

- **W-1** — the four forgeries against the recorded-correction verb were
  written as tests and run against the PRE-FIX `trace.py`: three returned
  `AssertionError: []` (the guard produced no findings for a hand-typed
  record, a chained second correction, and a record citing a ruling that does
  not exist) and the fourth showed the forged second record had ERASED the
  ruled first one from the parsed map. All six pass now, the sanctioned
  correction still passes every arm, and this repo's own two records
  (`B 7 → 8`, `REL 3 → 4` by OI-47) are green at `integrity=0` — including
  through a real `--bump-ids` regeneration taken during the close.
- **W-2** — verified with the real hook binary on a freshly bootstrapped
  scaffold: corrupt `process.toml` + legacy `deny` → `deny`, exit 2 (matching
  pre-WI-491); corrupt + no legacy → `ask`, exit 0; corrupt + legacy `off` →
  `ask`, exit 0.

Final verification (all foreground, on this box): **full suite 2749 passed,
14 skipped in 514.40 s**; smoke 1296 passed / 5 skipped at 59.4 s; `trace.py --strict-integrity` integrity=0;
`check_trajectory.py --strict` clean; `check_docs` 0 broken;
`gen_open_items --check` clean (six stale-deferral warnings → none).

## Next session, in order

1. **Nothing is owed from this batch by a worker.** The frontier is PROGRAMS
   only and unchanged in shape — the common-module lane, the decomposition
   lane, the wi455 interfaces lane, the gate-floor row, the component-view
   lane, the concurrency close. The generated frontier in `docs/status.md`
   carries the order; series discipline held.
2. **Two fresh owner rulings, both minted with recommendations attached:**
   - **OI-52** — what the 60 s smoke budget MEANS at the commit bar. The
     measurement half is done and landed (three warm runs 59.59 / 59.07 /
     59.98 s against a 60 s budget, replacing a justification that claimed
     ~7.5 s and ~5x headroom). What is owed is the protocol sentence: a worker
     reading "1296 passed" reports green while the declared seconds bar has
     failed. Recommendation: redefine 60 s as a CI target, then file the
     re-tiering as work. The budget VALUE is not on the table.
   - **OI-53** — the dozen stale Approved `CodeSymbol` cells the back-link
     campaign surfaced (LLR-175's `LaneState` is now `RoutingState`; LLR-011's
     `write` half names no real symbol; nine more skipped by the campaign for
     the same reason). Recommendation: one batch amendment sitting, plus a
     small row to mechanize the tag-vs-cell cross-check so the next campaign
     inherits a measurement rather than a memory.
   The four already-open items (OI-48, OI-49, OI-50, OI-51) are untouched by
   this close except OI-51's `blast_radius`, corrected to say the product
   floor's live set is EMPTY in every shipped configuration rather than
   "dormant for the three built-ins".
3. **Four queued topics that deliberately got NO row**, so the next session
   inherits them rather than re-discovering them:
   - **Q-1** collective-row back-link semantics (`Implements-part:`, or the
     full link on a facade symbol with constituent participation recorded
     separately). A shipped-GRAMMAR change; the current tags are honest, and
     the complaint is about the claim's grain.
   - **Q-2** the B-05 conversions keep their internal-consumer populations in
     prose only; a machine-readable consumer-set field is a registry-schema
     question.
   - **Q-5** IF-056/IF-077's expired deferral rationale — the 49-citation-clause
     deletion pass needs a tracked home in the wi455 lane spec.
   - **Q-6** the `external:git` endpoint convention against EXT-001's
     dissolution — a reader trap, and that lane's vocabulary to settle.
   Q-1/Q-2/Q-5/Q-6 all belong to the wi455 lane's own vocabulary work; filing
   them as owner rows now would ask for a ruling on a notation before the lane
   that owns it has a proposal.
4. **Standing owner acts this close did not take:** the branch is NOT pushed
   and NOT merged (`push = "human"`). Three commits sit on
   `requirements/ears-and-quality-characteristics` above `bd8fce68`.

## Deliberately declined — do not re-litigate silently

From the worklist's own declined block, plus one added by this pass:

- Re-fixing the six B-05 conversions wholesale (Sol 5's suggested schema) —
  Q-2 owns the design; the rows are honest per their notes today.
- Moving the smoke budget in either direction. Both reviewers agreed the 60 s
  number was not to move to fit the box that embarrasses it; OI-52 rules what
  it MEANS, never what it is.
- Editing OWNER-held Approved spine rows for the m-26 staleness class — that
  is exactly what OI-53 exists to decide.
- Seeding module-size baselines for the five `kitlib` files (W-6's second
  arm). Refused on measurement: they are 54–304 lines against a 1,500-line
  threshold, and a sub-threshold baseline entry would trip the ratchet's own
  "shrank below baseline" arm on the next commit. The blindness itself is
  fixed — the census recurses and keys by relative path, so a package module
  can now be seen AND can earn a baseline; a test names the package so the fix
  cannot rot quietly.

## One thing a reader of the diff should know

`W-3` narrows a shipped grammar: an `Implements:` declaration must now OPEN its
line. This repo's own coverage figure is unchanged (83/165 before and after),
but an adopter who wrote the tag after a summary sentence on the same line will
see their percentage fall. It is disclosed in `RESYNC_PACK.md` with the fix
(move the token to the start of its own line) rather than shipped silently.
