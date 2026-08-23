+++
id = "WI-391"
title = "The remainder of concurrency-v2 §B2, split off from WI-384 and filed at its REVIEW-A round 1: mirror the SPECS-OF-RECORD onto the terminal folders. WI-384 made the work-item REGISTRY's state its folder (draft|queued|active|deferred|cancelled|complete) and, by giving each terminal its own directory, deleted the `disposition` attribute, its cross-check and both raise paths. §B2's second sentence asks the same of the spec-of-record home: a closed WI's spec moves to `docs/archive/specs/complete/` or `docs/archive/specs/cancelled/` rather than one flat `docs/archive/specs/`, so a spec's location answers shipped-or-cancelled without opening it. SCOPE HONESTLY STATED: this is NAVIGATION, not a constraint - unlike the registry half, `docs/archive/specs/` carries NO state attribute (its files are `<stem>.<date>.md`), so mirroring it deletes no machinery, closes no raise path and makes no bad state unrepresentable. That is exactly why WI-384's reviewer judged the split legitimate rather than a dropped half, and it is why this row must justify itself on the navigation benefit alone. THE COST IS A LINK MIGRATION, MEASURED 2026-08-01 (re-measured at review; an earlier figure of 109 was unreproducible and is superseded): a reference of the form `archive/specs/<name>.md` occurs 154 times repo-wide across 30 files (*.md/*.py/*.csv/*.html), of which 101 are MARKDOWN LINK TARGETS that a relocation must rewrite; `docs/log.md` alone holds 119 occurrences on 101 lines, 92 of them markdown link targets over 61 unique targets, and 111 files sit in `docs/archive/specs/`. WHY IT IS ITS OWN ROW AND NOT A CHUNK OF WI-384: the bulk of the rewrite lands in `docs/log.md`, which a work branch may not edit (WI-384 retargeted exactly four links there under a driven necessity argument and its reviewer accepted that as bounded; 92 is not bounded), and the tool that once did this mechanically - WI-288's `_relink_archived_specs`, which resolved each inline link by PATH relative to the file holding it, kept the link TEXT and redirected only the TARGET, carried `#fragment`s and preserved line endings - died with `agent_dispatch.py` at concurrency-restructure Phase 5. PROBABLE PREDECESSOR: rebuild that relinker as a kit script (or as part of the close ritual `integrate.py` already owns) before moving anything, because a hand-run 101-target rewrite across a record surface is the shape this repo has twice paid for. ALSO IN SCOPE once the move is made: `check_trajectory`'s `ARCHIVE_SPECS_DIR` (check_trajectory.py:156, used at :1789 and :1793) + `_own_spec`'s archived glob (check_trajectory.py:1770, the glob at :1791, two call sites), R-F's remedy text, and the `docs/specs/README.md` lifecycle prose - all of which currently name the one flat home. DECIDE FIRST whether a partial migration is acceptable: leaving the 111 existing files flat while filing new ones into the terminal subfolders produces THREE homes and answers shipped-or-cancelled for none of them, which is worse than either end state, so this row is all-or-nothing by construction."
workstream = "process"
buildtier = "medium"
safety_class = "ordinary"
+++

## Deliverable

CANCELLED 2026-08-01. Not built, and it will not be: under **both** options open
at OI-11 — strike §B2's spec-mirror sentence or restate it — this row's work does
not happen, so its own fate is settled even though the design text's is not. The
row was measured and prototyped first; an independent review confirmed the
refutation (`APPROVE findings=6`, `2a4c9642`) and a second round confirmed the
mechanics. What follows is the reason, which is the whole point of a cancelled
row.

**The mirror cannot be built correctly, on measurement rather than by analogy.**
A folder is derived data, so it needs a total function from state to location.
This one does not have one.

- **Not total.** Of 111 archived specs, **92** resolve to `complete`, **3** to
  `cancelled`, and **16** to nothing: 15 shared effort docs — a first-class shape
  under the `docs/specs/` README lifecycle, which archives a shared doc when its
  *last* open citer closes — plus `WI-300-sr052-binding.2026-07-26.md`, whose
  name does not match `_own_spec`'s own `WI-###.<date>.md` glob. A mapping whose
  own reader cannot name a file is not a mapping.
- **Contradictory for at least one file.** `research-knowledge.2026-07-29.md` is
  cited by WI-138 and WI-145 (`complete`) and by WI-158 (`cancelled`). Both
  folders are correct for it, so no placement is honest.
- **No regenerator.** `gen_trajectory.py` contains the string `archive` zero
  times, so nothing could gate the derived location for freshness. It would be
  hand-maintained derived data — the one shape the kit's
  generated-not-hand-maintained rule forbids.
- **Already answered by location.** For the 92 attributable specs,
  `docs/work/complete/` vs `docs/work/cancelled/` answers shipped-or-cancelled
  one directory over — the registry half WI-384 built. The split is 92/3, so the
  mirror answers "shipped" 97% of the time for a question one `ls docs/work/`
  already answers.
- **No consumer wants it.** `check_trajectory`'s `ARCHIVE_SPECS_DIR`, `_own_spec`
  and its glob, and the archived-spec glob in `tests/test_trajectory_specs.py`
  (line 511) would each have to **widen** to recurse: the required code change is
  to *ignore* the split. The `docs/archive/specs/*` entry in
  `docs/orphans-allow` (line 50) survives untouched only because fnmatch `*`
  spans separators.

**Cost was not the objection**, and was measured to remove that defence: the
one-time migration was prototyped as a dry run at about 70 lines, which also
settles the rebuild-a-relinker question — a one-time migration beats rebuilding
machinery for a move that happens once. The relocation is nevertheless larger
than the intake stated, because a relocation rewrites *resolved* links, not
matching strings: **124 inbound targets across 25 files** resolved by path (the
WI-288 rule) plus **91 outbound links across 43 of the 111 files** that a
one-level-deeper move rebases (the WI-353 defect) — about **215**, against the
intake's 101.

**On the intake's measurements**, stated as this row's own convention rather than
as agreement with anyone: the literal string `archive/specs/<name>.md` in
`*.md`/`*.py`/`*.csv`/`*.html` occurs **156 times across 31 files** at
`2a4c9642`, and **154 across 30** at `0b4774f0` — the delta is exactly this
row's own review file, one new file carrying two occurrences, which is a fair
demonstration that the reference surface accretes faster than a migration could
be scheduled. `docs/log.md` (untouched by this branch) holds **119 occurrences on
101 lines**, of which **92 are markdown link targets** covering **57 unique
targets by full-string key** (55 by basename, 55 fragment-stripped, 57
basename-plus-fragment — 57 is the maximum by any key). An earlier draft of this
row reported "61 unique targets" against those 92: that was **wrong**, and it was
argued for once before being withdrawn. 61 is the count of unique names among
`docs/log.md`'s **119 all-occurrences**, a different and larger population than
its 92 link targets. The correction is recorded here rather than quietly fixed,
because the wrong figure was at one point asserted as verified.

**Spawned, and both outlive this row:** **OI-11**, the owner's decision on §B2's
sentence (open, and deliberately not a decision about this row); and **WI-393**,
which rehomes the link-aware archival ritual WI-288 and WI-353 built and Phase 5
deleted — a confirmed live regression with driven evidence, and, unlike this row,
one with driving necessity.
