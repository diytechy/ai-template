+++
id = "WI-518"
title = "The snapshot re-seed absorbs off-spine registries with no owner surface — give the approval brief an off-spine census"
specref = ""
workstream = "requirements"
needs = []
buildtier = "medium"
safety_class = "attestation"
priority = 3
+++

## Deliverable

The approval brief now discloses off-spine drift the spine-only rendering
could never show. Record:
[../../../log.d/2026-08-24-wi518-offspine-census.md](../../../log.d/2026-08-24-wi518-offspine-census.md).

`trace.offspine_census_rows` (the data half) and `trace.offspine_census_lines`
(the markdown renderer, wired into `reattest_lines` right after the derived
stamp lines) plus `gen_open_items._offspine_census_block` (the HTML renderer,
wired into `render`'s header right after the Baseline line) walk the three
off-spine registries — `interfaces.toml`, `external.toml` (three id-keyed
tables in one file), `components.toml` — and report rows changed/added/removed
against the snapshot at FILE grain, each with a one-line pointer at the
`WI-###`/`OI-###` ruling(s) whose commits touched that file since the
snapshot (or `"none cited"`). A no-change tier renders nothing on either
surface — no heading, no line. `owes()` is untouched: this is a disclosure
surface, not a new gate.

Driven by tests, RED first (`tests/test_trace_briefs.py`,
`tests/test_gen_open_items.py`), against a fixture carrying this repo's own
seven real registries: an amended `IF-001` cell makes both surfaces name
`docs/requirements/interfaces.toml` with `1 changed, 0 added, 0 removed`
while staying silent for the untouched `external.toml`/`components.toml`
tiers, and a second pair of tests confirms total silence when nothing
off-spine changed.

`docs/open-items.html` was regenerated and is byte-identical to what was
already committed (no off-spine tier has drifted on the live repo right now).
Three ratchets re-stamped with reasons at each site:
`tests/test_module_size_ratchet.py` (`trace.py` 5678 -> 5817),
`tests/test_complexity_ratchet.py` (`reattest_lines` 11 -> 12),
`tests/test_generated_newlines.py` (the pinned non-literal-newline site in
`gen_open_items.py`, 1234 -> 1266).

Gates, full unfiltered suite (two foreground batches at the smoke/slow
boundary, both green, 0 failed) and the smoke-budget caveat (over budget on
this box BOTH with and without this change — a pre-existing, one-machine
load condition, not a regression) are in the log fragment above.

## Context

Found by the adversarial round on the 2026-08-24 OI-62 sitting (MAJOR-2 of
that review; record:
[../../log.d/2026-08-24-oi62-rule-and-spine-approval.md](../../../log.d/2026-08-24-oi62-rule-and-spine-approval.md)).
`intake.py snapshot` copies **all 7** snapshotted registries wholesale — the
off-spine tiers (`interfaces.toml`, `external.toml`, `components.toml`)
included — but `trace.py --approve modified` renders **one section per SR**:
the spine chains. An off-spine registry that changed since the last re-seed
therefore enters the signed baseline with **no owner-visible before/after at
all**. Measured at that sitting: the re-seed absorbed a **135-row, 797-line
`interfaces.toml` reshape** (the WI-455 `direction`→shape rename + the WI-512
`contract` thinning — each landed under its own ruling, so no content was
unblessed) while the brief the owner read showed only the 10 spine sections.

The risk is bounded today — every IF row reads `Drafted`, `is_drifted`
returns False below approval, so nothing mechanically treats the absorbed
copy as blessed — but the snapshot README's stamp says "refreshed under
approval ref" over all 7 files, and a reader of the stamp cannot tell the
spine (surfaced, ruled on) from the off-spine (absorbed, invisible). That is
a laundering-shaped hole in the SURFACE, independent of any sitting's
honesty.

**The fix shape, smallest first:** the approval brief (`reattest_lines` /
both renderers) gains an **off-spine census line** — per off-spine registry,
rows changed / added / removed since the snapshot, with a one-line pointer at
the ruling(s) that landed them (or "none cited") — so the signer SEES what
the re-seed will absorb even where no per-row rendering exists. A fuller
per-row off-spine diff is explicitly a possible follow-on, not this row's
bar. Whatever ships must not change what `owes()` gates on (off-spine tiers
carry their own approval machinery per the OI-30 D3 rung map); this is a
disclosure surface, not a new gate.

**Test shape:** a scaffold where an IF cell changes after a seed; assert the
regenerated brief names the interfaces registry in the census with the right
count, and that a no-change off-spine tier renders nothing (no standing
noise).
