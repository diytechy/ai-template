## 2026-09-06 — Owner rulings: control admission, smoke budget, SN-036 scope

Three owner answers to the sitting's clarification list, recorded on the
owner's behalf.

**Control window admission.** The window measures the first WIs, so a route
that cannot report spend, or an aggregate that cannot be reserved, does not
stop admission. US$100 becomes a watched bound over reported spend with
missing figures recorded as missing; the eight-WI, two-day and twelve-hour
bounds are unchanged. Recorded as a dated re-ruling in the control decision's
owner section; the preflight's spend finding is now an accounting gap, not a
launch gate. The pause and its reviewed deletion remain the launch act.

**Smoke budget.** A smoke test is meant to be fast and thirty seconds is not
worth a standing exception. `[smoke-budget] seconds` is raised 60 → 90 in
`docs/stack.ini`; CLAUDE.md and the session-protocol skill (and its two
materialized copies) restate the new figure. `max-tests` is unchanged, no test
changed tier, and the prior per-commit timing exception is retired: the bar is
enforced as declared again.

**SN-036.** The owner asked whether re-pointing SR-161 also answers SN-036.
It does not by itself: a child may not narrow an Approved parent's acceptance
(the rule applied to SR-184 under SN-024), so SN-036's "machine-readable
record … a check reports" clause must be amended in the same act. That is
already act 1 of the [SN-036 ruling](2026-09-06-sn036-owner-ruling.md); no
further work is added.

**Adjudication queueing** of the Drafted amendments: the owner will review
shortly; nothing changes here.

Validation: the commit bar at this tip is pasted in the commit message.

Deferred open items: OI-82 — explained to the owner this sitting; awaiting a
one-word confirmation of option (a), not ruled here.
