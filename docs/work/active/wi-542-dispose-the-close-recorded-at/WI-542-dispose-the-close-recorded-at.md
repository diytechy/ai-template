+++
id = "WI-542"
title = "dispose: the close recorded at docs/handbacks/WI-521-wi521-decomposition-debt-owner.md - cancel / defer / draft a successor / surface an open item (a disposition row never closes early; R3)"
workstream = "process"
specref = "docs/work/partial/WI-521-decomposition-debt-owner.md"
buildtier = "medium"
safety_class = "adjudication"
brief = "disposition"
+++

## Context

The closed spec is `docs/work/partial/WI-521-decomposition-debt-owner.md`.

Its per-close report is `docs/handbacks/WI-521-wi521-decomposition-debt-owner.md` — READ IT FIRST. The report is the close EVENT's own immutable record: what the lane claims it delivered and did not, the commit range, the keep/discard split, and the review tier it suggests. The lane's claimed outcome is a CLAIM under judgement here, not this row's premise.

Outcomes (R3): cancel / defer / draft a successor / surface an open item. Continuing the work MINTS A SUCCESSOR (drafted in THIS row's `## Dispositions` section, carrying `supersedes`), never a revival of the closed row — a closed row is never re-opened and a scope definition never changes to mean something else. An override moves the byte-identical spec to the corrected terminal folder; the report stays on record as the claim it was. An open item goes to docs/requirements/open-items.toml.

## Dispositions

The adjudication is recorded at
`docs/reviews/wi-542-dispose-the-close-recorded-at/001-ADJUDICATE-1058868.md`:
`WI-521`'s close is ruled **PARTIAL**, whole commit range **KEEP**, one
successor. The standing decomposition-debt owner role cannot ride a disposed
row, so it transfers here.

```toml
title = "The decomposition debt owner (cont.): three wide modules, check_trajectory's remaining fusion, and M-06's last two test monoliths"
workstream = "process"
buildtier = "strong"
safety_class = "ordinary"
priority = 2
specref = "docs/plans/2026-08-25-remap-alignment.md"
supersedes = "WI-521"
```

**Standing owner, not a one-sitting task** — same as its predecessor: claimable
one scoped slice at a time, closed only when the debt is paid or re-homed, and
**if it ever closes the `tests/test_module_size_ratchet.py` pointer moves in the
same commit** (the rule it inherits).

**Carried debt** (what `WI-521` left un-paid after slice 3):

- The three remaining fusion heads — `agent_loop`, `agent_common`, `bootstrap`
  — each re-measured against `WI-508`'s blind derivation before any split, and
  none a mandate to split (a slice may re-measure and leave a module, as
  `WI-483` left `check.steps`).
- The rest of `check_trajectory` (4,327 lines, ~5 fused pairs left, `main` at
  complexity 24).
- M-06's remaining monoliths: `test_trajectory_arch.py` (2,290) and
  `test_agent_loop.py` (1,640) — a standalone split is in scope (the `WI-483`
  ride-along rule does not bind here), by stable behaviour boundary not line
  count.

**NOT carried:** §3's sensor-gap / line-count-axis question — OI-68 (ruled
2026-08-30) re-homed it to `WI-537` (report-only) → `WI-538` (arm + re-base),
and `WI-538` amends that §3. Nothing on the sensor gap is owed here.

**First-commit obligation** (adjudication MAJOR finding): move the debt-owner
pointer in `tests/test_module_size_ratchet.py` — the module docstring, the
`"decompose (WI-521)"` finding message, and the baseline-entry comment
references — from `WI-521` to this successor's minted id, so the growth sensor
never names a terminal row.
