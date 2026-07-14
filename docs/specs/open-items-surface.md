# Campaign: open-items-surface — the owner decision surface + the status.md structure lint

**Owner-directed 2026-07-13** (the sitting that slimmed `docs/status.md` from
329 → 77 lines, commit `a7d187c`). Two asks: (1) open items must surface at the
top of `status.md` as a bulleted list, ratification blockers first, and stay
that way mechanically; (2) the *depth* of each pending owner decision — blast
radius, options with pros/cons, a recommendation — must live in **a single file
the owner reviews with all context**, without re-bloating `status.md`.

## Design

**The two-file split.** `status.md` stays the forward-only blackboard (short,
scannable); a new **`docs/open-items.md`** is the owner-review surface — one
section per pending decision (`## OI-N — <title>`), carrying the decision
statement, blast radius, options + pros/cons, and the driver's recommendation.
`status.md`'s Open-items bullets stay one-liners (id + one-line recommendation
+ link). Lifecycle: **a section lives in `open-items.md` only while the
decision is pending** — the ruling appends to `log.md`'s Decisions log and the
section is deleted. So the file is self-limiting: it only ever holds live
decisions.

This adds no third source of truth:

| surface | holds | direction |
|---|---|---|
| `work-items.csv` | what work exists (DAG, status, deps) | tracking |
| `docs/open-items.md` | **pending** owner decisions + their analysis | pre-ruling |
| `log.md` Decisions | ruled decisions | post-ruling, append-only |

**The lint (all warn-tier, in `check_docs.py`).** Content quality
(is the pros/cons real?) is Reviewer-class per the enforcement audit and is
**not** mechanized — only the self-proving structure is:

- **S-1 (budget):** `docs/status.md` exceeds its line budget — default **120**
  lines; `docs/status-lint` (run-phase idiom: comment lines + one value on the
  last line) overrides with an integer, or `off` disables S-1..S-3.
- **S-2 (order):** the Open-items marker must precede the `## Scope` heading
  (open items surface at the top, backward matter below); a `status.md` with a
  Scope section but no Open-items marker also warns.
- **S-3 (coherence):** with `docs/open-items.md` present — every `OI-N` token
  inside the **Needs \<human>** block of `status.md` has a `## OI-N` section in
  `open-items.md` (no undocumented owner ask), and every `## OI-N` section id
  appears somewhere in `status.md` (no orphan brief). Vacuous when
  `open-items.md` is absent — the surface is opt-in downstream. Extraction is
  best-effort over the template's mandated shape (the Needs-\<human> bullet and
  deeper-indented `OI-N` bullets); a custom layout misses warnings, never
  false-fails.

All three print as `check_docs: WARN — …` and never join the exit code —
matching the WI-129 stance (warn, don't gate, don't mutate).

**No new SR (ruling).** Checker features trace as SRs (SR-012/SR-037
precedent), but a Draft v3 SR drops the runnable derived gate to G1 for the
whole repo until the phase advances (derive_gate: `raw = min(...)`,
Draft ⇒ G0) — disproportionate ceremony for a warn-tier, non-gating lint plus
a template. The live precedent is **WI-129** (a warn-tier trace.py feature, no
SR). **Un-defer trigger:** if S-1..S-3 are ever promoted to a gating tier
(an exit-code failure or a `--strict` set), that promotion drafts the v3 SR.

## Slices

- **WI-130 — the meta's own `docs/open-items.md`** (OI-1..OI-7 briefs, content
  from the pre-slim `status.md` + `log.md`), `status.md` gains the link + the
  depth-pointer line. Done when: every Needs-\<human> `OI-N` has a section;
  `check_trajectory --strict` stays clean.
- **WI-131 — ship the surface**: `OPEN_ITEMS.template.md` (an `OI-1` example
  matching `STATUS.template.md`'s), `bootstrap.py` `MAPPING` +
  `docs/open-items.md` scaffold, `STATUS.template.md` guidance (ratification
  blockers head the Needs-\<human> list; depth lives in `open-items.md`),
  `project-trajectory/README.md` kit-contents row, `test_bootstrap.py` file
  lists. Done when: a fresh scaffold carries a coherent `open-items.md` and the
  bootstrap tests pass.
- **WI-132 — the lint**: `check_status_surface()` in `check_docs.py`
  (S-1/S-2/S-3 + the `docs/status-lint` policy file), tests
  (`test_check_docs.py`: budget over/under/override/off, order violation,
  coherence both directions, vacuous-absent), PROCESS_OPTIONS "Trajectory /
  work-items layer" gains the open-items subsection (the one home). Done when:
  the meta repo's own surfaces pass S-1..S-3 with zero warnings and the tests
  pin warn-only (exit 0 with findings).

Byte-budgeted files: none touched (PROCESS.md unchanged; the doc lands in
PROCESS_OPTIONS).
