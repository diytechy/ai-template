## 2026-11-04 — WI-982: both adjudication routes widen a sitting's hats by the authoring work item's tags

Deferred open items: none.

The mint writes one new work-item cell, `AuthoringTags`, on the first-approval
and amendment rows a route that names an authoring item mints, and
`hats.context_from_work_item` reads a non-empty cell in place of the row's
`Workstream` and `SafetyClass`. A range sweep with no `--merged` names no author,
so the cell stays empty and the row widens by its own tags, as a minted row did
before. The routing `SafetyClass` stays `adjudication`.

- `intake.py` is bumped +18 (1872 -> 1890 SLOC): `_authoring_tags`, its one call,
  the two drafters' parameter and the `_draft_row` line. The plan's estimate was
  about 13; the formatted comprehensions took the rest.
- LLR-360 gained two sentences by addition, which the plan had not expected. The
  checkpoint's author stopped on finding that no row stated what TC-399 was to
  verify (wi-982 D-004). Sitting 003 returned the first wording as broader than
  the build, and sitting 004 blessed the narrowed one, with TC-399's text.
- Act seq 172 re-attested LLR-360 and TC-399. One counted round, then the gate:
  round 1 raised one MINOR, the checkpoint's own step, and the gate two MINORs,
  triaged in wi-982 D-008.
- REVIEW-B stood in as Claude Opus at high in both rounds (wi-982 D-001).
