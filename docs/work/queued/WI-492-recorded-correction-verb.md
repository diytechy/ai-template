+++
id = "WI-492"
title = "The recorded-correction verb: one sanctioned raising act for a mis-seeded watermark, and the one-time B=8/REL=4 correction (OI-47 ruled (e), 2026-08-20)"
specref = "docs/requirements/open-items.toml#OI-47"
workstream = "scripts"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

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
