+++
id = "WI-518"
title = "The snapshot re-seed absorbs off-spine registries with no owner surface — give the approval brief an off-spine census"
specref = "docs/log.d/2026-08-24-oi62-rule-and-spine-approval.md"
workstream = "requirements"
needs = []
buildtier = "medium"
safety_class = "attestation"
priority = 3
+++

## Deliverable


## Context

Found by the adversarial round on the 2026-08-24 OI-62 sitting (MAJOR-2 of
that review; record:
[../../log.d/2026-08-24-oi62-rule-and-spine-approval.md](../../log.d/2026-08-24-oi62-rule-and-spine-approval.md)).
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
