+++
id = "WI-492"
title = "The recorded-correction verb: one sanctioned raising act for a mis-seeded watermark, and the one-time B=8/REL=4 correction (OI-47 ruled (e), 2026-08-20)"
specref = ""
workstream = "scripts"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

Full row, not a slice. `trace.py` gains the one-shot recorded-correction verb
(`correct_watermark`/`read_corrections`, wired behind `--correct-mark SPACE
NEW RULING`) beside the existing `bump_watermark`/`read_watermark` pair: a
NAMED mark raises to a NAMED value on a NAMED ruling's authority, recorded as
a `# correction: SPACE old -> new (ruling)` header comment `read_watermark`
already skips, and `_mark_history_findings` accepts a raise only when a
recorded correction matches the EXACT `(was, now)` transition — an
unrecorded raise, or a record for a different jump, is still refused, and a
lowered mark is refused unconditionally, before corrections are even
consulted. The verb refuses to run twice for the same space (one-shot).

The correction landed via the verb itself, not a hand edit: `docs/id-watermark`
now reads `B = 8` / `REL = 4`, both citing `OI-47`. `docs/requirements/
external.toml`'s SPENT IDS block shrank to a pointer at OI-47 — the mark now
carries the protection that prose used to state.

Tests extend `tests/test_id_watermark.py`: a recorded correction is accepted;
an unrecorded raise is still refused; a lowered mark is refused even with a
correction record present; the verb is one-shot and refuses to replay; a
non-raising value is refused; `bump_watermark` preserves an existing
correction across an ordinary regeneration; and the corrected-mark mint arm
(next B mint is B-09).

RESYNC entry: `project-trajectory/RESYNC_PACK.md` §3, "The id-watermark gains
a RULED-correction arm (OI-47 ruled (e))".

Code commit: `da4d3bcd`.

## Context

Executes OI-47's ruling — (e), the minimal recorded-correction act. The
row's option texts record why the alternatives died (the spent-id registry
as over-built, the census by measurement); do not rebuild them.

- **The verb:** `trace.py`'s watermark writer gains a one-shot correction
  act that raises a NAMED mark and records the authorizing ruling id in
  the watermark header. `_mark_history_findings` accepts a raise the
  header records; an unrecorded raise is still refused, and a mark still
  never falls. The header record must survive `read_watermark`'s parse —
  format is the session's call, compatibility with the shipped
  `id-watermark.template` kept.
- **The correction, same change:** B 7→8, REL 3→4, authorized by OI-47.
  From then on a mint counts from the corrected mark, so `B-08`/`REL-004`
  can never re-issue — the mark becomes the protection.
- **The retirement, same change or immediately after:** `external.toml`'s
  SPENT IDS block shrinks to a pointer at OI-47 — it was the interim
  protection, and its full prose outliving the fix would be a second home
  for a fact the mark now states.
- **Tests:** extend `tests/test_id_watermark.py` — recorded raise
  accepted, unrecorded raise still refused, lowering still refused, and
  the corrected-mark mint arm (next B mint is B-09).
- **RESYNC entry owed:** shipped integrity machinery gains an arm.
