# 072-REVIEW-A — WI-144 (final dashboard quality round)

Independent review of commit `a8a7ed1` (WI-144: harden the final dashboard
quality round), built session 071. Reviewed the diff against the spec-of-record
(`docs/specs/owner-intake-2026-07-13.md#v3-dashboard-ux`), the SR-052/053/054
Critique rows and their rubrics (`docs/rubrics/dashboard-{accessibility,
uniformity,usability}.md`), AGENTS/PROCESS discipline, and the registries. No
SN/SR/TC rows were added or changed, so no registry sweep applies. WI-144 stays
`active` (no browser backend for the required fresh critique) — that self-scope
is honest and correctly reflected in status.md / next-wi / run-state.

## Harness run (observed, not reported)

- `python project-trajectory/scripts/check.py --gate G2` → `RESULT: PASS`
  (derived-gate, traceability, privacy, doc-navigability, design-flows,
  trajectory all PASS; `check_trajectory --strict` clean, 166 WIs, graph acyclic).
- `python -m pytest tests/test_gen_trajectory.py -q` → `78 passed in 16.82s`
  (the 3 new TC-HARDEN included).
- `python -m pytest -q -n auto -m smoke` → `615 passed, 2 skipped in 56.17s`.

## Assessment

The mechanization is sound: the 3 TC-HARDEN compute the emitted contrast pairs,
assert the interactive controller selectors have live targets, and require the
When legend's palette/legend bijection. The queued-badge dark-ink fix, the focus/
`.hl` ring darkening (`#f59e0b`→`#b45309`, ≥3:1 vs both page backgrounds), the
`--small`/`--xsmall` U1 token consolidation, the `.blab` ellipsize with the full
label preserved in `data-label`/`<title>`, and the shared `.phaselegend` legend
idiom are all correct and verified against the regenerated `PROJECT_STATE.html`.

Three residual defects survived, all confirmed against the regenerated artifact.
Two are concrete regressions in the exact surfaces this round claims to fix (U4
detail-on-every-block; A4 interactive-block contrast) — a fresh critique will
bounce the round on them, so they should be fixed before that critique runs.

## Findings

- [MAJOR] project-trajectory/scripts/gen_trajectory.py:2035 -> the new grouping-block detail wiring passes `title:id` where `id` is the block's `data-label`, and `renderDetail` (line 1967) emits `<h3>` as `esc(id) + ' — ' + esc(d.title)`, so every phase/workstream/campaign block renders its label twice — the real artifact shows `<h3>capability-expansion-2026-07-11 — capability-expansion-2026-07-11</h3>`. This is the U4 "every block opens the detail aside" feature the round adds, wrong on its first interaction; no test exercises the rendered heading, so mechanization missed it -> in the `.block[data-node]:not([data-wi])` closure pass `title:null` (or the block's distinct `<title>`), not `title:id`, so the heading shows the label once -> @owner
- [MAJOR] project-trajectory/scripts/gen_trajectory.py:1676 -> the diff moved the workstream container stroke to `var(--muted)` (line 1715) and the default to `var(--muted)` (line 1504) for A4 boundary contrast, but the campaign container block still hardcodes `stroke="var(--border)"`; the regenerated dashboard renders workstream containers with `stroke="var(--muted)"` (#64748b ≈ 4.76:1 vs white) and campaign containers — equally interactive descend targets — with `stroke="var(--border)"` (#e2e8f0 ≈ 1.23:1 vs their white fill), below the 3:1 UI-boundary floor that the accessibility rubric's A4 anchor declares. This both fails the A4 floor the log claims "interactive block contrast now meet" and introduces a per-tier border non-uniformity (U3: a container of the same kind styled differently in the same drill) that the previous uniform `--border` did not have -> change line 1676 to `"stroke": "var(--muted)"` so both container tiers share one A4-passing boundary -> @owner
- [MINOR] project-trajectory/scripts/gen_trajectory.py:1239 -> the de-collided `PHASE_ACCENTS` palette (U5) collapses the former 8 distinguishable hues into a single rose/pink/fuchsia/purple family; the first five (the phases the current dashboard renders) are `#9f1239` rose-800, `#881337` rose-900, `#701a75` fuchsia-900, `#86198f` fuchsia-800, `#831843` pink-900 — adjacent phases 1–2 and 3–4 render as near-identical shades, weakening the "grouping-primary encoding" the accent exists for (SR-052 "no info by color alone" still holds via the legend labels, and U5 cross-vocabulary de-collision holds, so this is a quality regression for the pending fresh critique to weigh, not a hard violation) -> pick 700–800 shades across distinct hues (e.g. indigo/teal/violet/rose/amber-dark) that keep white-text ≥4.5:1 and avoid the status green/amber, restoring categorical separation; also re-check `#713f12` amber-900 against status `active` #b45309 -> @owner

VERDICT: CHANGES-REQUESTED findings=3
