# Dispute 1: ruling (independent, Claude Opus) on WI-821 at `68b43fac`

Adjudicator: an independent Claude Opus session. I wrote none of WI-821's code
(Claude Opus builder), none of its rows (GPT Terra), and neither review (Codex
6.1 Sol, rounds 1 and 2). My calls are final (OI-103 Q3).

Ruled here: Sol's round-1 MAJOR 2 against D-001, the census baseline.
`docs/stack.ini [dupes-census]` was re-stamped from the committed 0/0/0 up to
2/2/32. Sol's round 2 left it for the adjudicator.

Read: CLAUDE.md; the WI-821 spec in full; `docs/decisions/wi-821.toml` (D-001
and D-009); `sol-review-r1.md` and `-r2.md`; `check_dupes_census.py` in full;
`docs/stack.ini` `[dupes-census]` and `[step:dupes-census]`; the WI-817 spec and
WI-788 design D6 row (`docs/plans/2026-10-04-wi788-design/1-state-evidence-recovery.md:238`).

## Basis (probed, not trusted)

- **Before and after readings.** I ran the census's own walk on `git archive`
  exports of trunk `b27ef5d1` (the lane's base) and lane `HEAD` `68b43fac`, both
  under `review-tmp/adj821/`. My `groups.py` walk is the same as the census and
  also lists each group's members.
  - `b27ef5d1`: **5/5/52.** The groups are `agent_policy.read_toml_text` and
    `kitlib/spine._toml_tables`; `human_approves` and `human_approves_spine`;
    the two `_is_docstring`s (`check_complexity`, `check_stubs`);
    `check_trajectory.read_rows` and `gen_release_checklist.load_csv`; and
    `frame_rules._entries` and `kitlib/spine.seam_endpoints`. The trunk census
    against its own 0/0/0 stamp prints `WARN - 5 group(s) / 5 redundant
    copy/copies / 52 redundant line(s) vs the stamped baseline 0 / 0 / 0 —
    duplication grew`.
  - `HEAD`: **2/2/32.** The groups are `human_approves`/`human_approves_spine`
    (26 lines) and `read_rows`/`load_csv` (6 lines). In the lane,
    `check_dupes_census.py --root .` prints `OK - 2 group(s) / 2 redundant
    copy/copies / 32 redundant line(s), unchanged from baseline.` and exits 0,
    with or without `--strict`.
- **The census code.** `main` prints one of three things: a WARN when any of
  the three numbers is above the stamp; an "improved, re-stamp downward" line
  when any is below; otherwise OK. It always returns 0 (D-7). The baseline is
  hand-maintained and "DOWNWARD-ONLY by convention (a reviewed re-stamp, reason
  in the log)". So the stamp is the census's only memory of which duplicates
  are already known.
- **What the spec says, both halves of it.**
  - Done-when 2: "`check_dupes_census.py --root .` reads 0/0/0, or the
    remaining deliberate groups only, and `docs/stack.ini [dupes-census]` is
    re-stamped down by hand with the before and after readings and the reason".
  - Context: "**The CSV-read pair waits on WI-817.** ... Take that group after
    WI-817, or drop it if WI-817 removes it, rather than merging code about to
    be deleted." Done-when 1 also keeps the `human_approves` pair "as the
    research judged it" (deliberate).
- **The two residuals are what the spec ordered left.** The `human_approves`
  pair is the deliberate one (research §7, D-009). The lane adds a by-value pin,
  `test_the_two_held_status_predicates_agree_by_value`, which passes. The CSV
  pair is the one the Context defers to WI-817. Neither residual is a duplicate
  the build failed to fold.

## Ruling: D-001 is ACCEPTED as it stands. No change is owed.

- **"Re-stamped down" can only mean the reading.** Done-when 2 allows a final
  reading of "the remaining deliberate groups only". It keeps the
  `human_approves` pair (26 lines) deliberate, so that reading is at least
  1/1/26. Against a 0/0/0 stamp, any stamp for that reading is a raise.
  Measured against the committed stamp, the clause could never be met. Measured
  against the readings it names ("with the before and after readings"),
  5/5/52 -> 2/2/32 is down. D-001 meets it on that reading.
- **The CSV pair is not "deliberate", but the spec orders it left.** The
  Context's specific order ("take that group after WI-817") governs the general
  Done-when line on this one pair. D-001 does not call the pair deliberate. It
  records it as "DEFERRED TO WI-817, not deliberate", with the reason, in the
  stamp's own comment. That is the honest label.
- **The downward-only convention is not broken in substance.** The convention
  stops a stamp from silently absorbing new duplication. Here nothing is
  absorbed:
  - The 0/0/0 stamp was already false at the lane's base. The census read
    5/5/52 there, so 0/0/0 described no tree this row started from.
  - The new stamp names each residual group, member by member, and the reason
    each is left.
  - The census is warn-only (D-7), so no gate is loosened either way.
- **The alternatives are worse.**
  - **Keep 0/0/0 with a standing WARN.** Every run would print "duplication
    grew" on a tree where duplication shrank, which is untrue. Worse, it blinds
    the sensor. A new duplicate arriving at 3/3/40 prints the same kind of WARN
    as today's 2/2/32, so the one signal the census exists to give, that a new
    duplicate appeared, is lost. At 2/2/32 a new duplicate WARNs, and the
    removal of either residual prints the re-stamp-down line.
  - **Merge the two held-status predicates now.** That overrides the research's
    judgement, which the spec keeps ("stays as the research judged it, unless
    the build finds otherwise"), and D-009. The build found no defect, so there
    is no ground to override it.
- **For the coordinator:** D-001's `review` field can record "ACCEPTED by the
  in-lane adjudicator, dispute-1-ruling.md". D-001 stays high-risk for the
  owner's look.

## A separate finding (not a dispute point; for the coordinator to file)

**Nothing on WI-817 owns the deferred CSV pair, and WI-817 may not remove it.**

- WI-817's spec does not mention `check_trajectory.read_rows` or
  `gen_release_checklist.load_csv`. Its one burn-down line is the bar
  vocabulary.
- `gen_release_checklist.load_csv`'s only caller reads
  `docs/requirements/performance-budgets.csv`
  (`gen_release_checklist.py:229`). That is the off-spine PB registry.
- WI-817's D6 retires the CSV and markdown *carriers beside TOML* and
  `agents.csv` (WI-788 design ch.1 D6). It names no off-spine CSV registry.
- So WI-817 may well remove `read_rows` and keep `load_csv`. In that case the
  census reads 1/1/26, prints its re-stamp-down line, and the pair is gone; it
  surfaces by itself. If WI-817 keeps both readers, the pair sits in the
  baseline with no owning row and no signal, forever.
- Owed: add one Done-when line to WI-817 (or file a small row after it): "the
  `check_trajectory.read_rows` / `gen_release_checklist.load_csv` census pair
  takes one home, or is recorded removed, and `docs/stack.ini [dupes-census]`
  is re-stamped down". This is filing work, not a change to D-001.

## Not verified

The stamp comment says the 0/0/0 stamp drifted because `[step:dupes-census]`
runs from DevStg-Impl, a stage the derived stage did not read while the groups
arrived. That is the builder's history claim. I did not need it for this ruling
and did not verify it.

RULING: D-001=ACCEPT change-owed=none separate-finding=1
