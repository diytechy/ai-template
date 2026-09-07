+++
id = "WI-607"
title = "Refresh SN-036 record comments and add its perspective-coverage rubric anchor"
workstream = "process"
specref = "docs/reviews/2026-09-06-sn036-decomposition-structured-opus.md"
buildtier = "quick"
priority = 2
safety_class = "ordinary"
+++

## Context

F4 and F5 from the independent Opus review
(`docs/reviews/2026-09-06-sn036-decomposition-structured-opus.md`) are advisory
follow-up documentation work outside the named SN-036 amendment rows. The
amendment now discharges SN-036's perspective-coverage record through the
review path, but shipped explanatory prose still says that record is unbuilt,
and the change-review rubric has no direct SN-036 perspective-coverage anchor.

This item is documentation-only. It does not alter predicates, the hat roster,
registry schema, requirement values, checks, approval status, or snapshots.
The dogfood and template copies must remain structurally aligned.

## Done-when

1. Refresh the stale present-tense record-half comments in
   `project-trajectory/scripts/hats.py`, `docs/requirements/hats.toml`, and
   `project-trajectory/registries/hats.template.toml` so they describe the
   live SN-036 review-record route and do not claim the record is unbuilt.
2. Add one numbered, intent-derived anchor to
   `docs/rubrics/change-review-records.md` for SN-036's perspective-coverage
   obligation, covering applicable-perspective questions reaching the review
   record and keeping missing coverage visible. State that it is guidance, not
   a new gate or schema.
3. Keep all existing hat values and checking behavior unchanged; verify the
   dogfood/template structure and the rubric's anchor numbering.
4. Record the independent review and documentation scope in the session log.

Deferred open items: none.

The dogfood roster's owner-text designation protects its perspective definitions
and applicability decisions. This task synchronizes explanatory comments to the
already recorded owner ruling only: every hat table and field remains byte-identical.
If the correction would require a perspective/field change, return that part as
an owner proposal; do not infer authorization to edit the roster values.

The closure/Inspection advisory about the unexhibited brief-side failure may be
addressed in this same documentation follow-up by adding a bounded abnormal
sample to `docs/test/inspection-procedures.md`: the actual brief with one
applicable question omitted. Keep the existing obligation and Inspection method;
record its independent execution rather than claiming that a new example passed.
