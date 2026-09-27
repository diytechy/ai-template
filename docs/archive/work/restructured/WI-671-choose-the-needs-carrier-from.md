+++
id = "WI-671"
title = "Choose the needs carrier from the file in needs_from_text too, failing closed on an unparseable TOML needs file"
workstream = "scripts"
specref = "project-trajectory/scripts/spine_carrier.py"
buildtier = "quick"
safety_class = "ordinary"
priority = 4
needs = ["WI-660"]
+++

## Deliverable

Restructured into WI-651.

## Context

WI-660 made `spine_carrier.draft_ids_from_text` take the needs carrier from
its caller and refuse an unparseable `.toml` needs text instead of guessing
(arbitration ruling 6 of `docs/reviews/2026-09-26-wave3/ARBITRATION.md`).
Its builder and the codex review found the twin: `needs_from_text` still
decides between the TOML and markdown carriers by sniffing the text, so a
comment-only TOML needs file with an id in a comment can still be misread
on its callers' paths: `trace._sn_prose`, `check_docs.py`, and
`baseline_snapshot.py`'s needs readers (`_registry_needs`, `_needs_at`).

IN SCOPE: pass the carrier (the path or its suffix) through to
`needs_from_text` from every caller, dispatch strictly, and fail closed on an
unparseable `.toml` text the way `draft_ids_or_refuse` does. Test first: a
comment-only TOML needs file with an id in a comment yields no need on each
caller's path, and an unparseable one refuses by name.

## Done-when

- No caller of `needs_from_text` leaves the carrier to a text guess, and an
  unparseable `.toml` needs file refuses naming the file.
- The tests above were red first and pass; the commit bar passes.
