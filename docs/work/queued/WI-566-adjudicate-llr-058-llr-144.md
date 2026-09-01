+++
id = "WI-566"
title = "adjudicate: LLR-058, LLR-144, LLR-198, TC-138, TC-147, TC-194 - approved/routed cell(s) amended on merged trunk a024e76..fa92323 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-058 `Detail`: 'Derives the dependency-ready frontier from the WI registry + dispatcher reservations (never prose), excludes blocked/de…' -> 'Derives the dependency-ready frontier from the WI registry + dispatcher reservations (never prose), excludes terminally…'
- LLR-144 `Detail`: "close_partial: commits the lane's work as-is, moves each claimed spec to the TERMINAL partial/ (nothing re-claims it, s…" -> "close_partial: commits the lane's work as-is, moves each claimed spec to the TERMINAL partial/ (nothing re-claims it, s…"
- LLR-198 `Detail`: 'The pending-owner-action derivation, in one module that renders no page and decides nothing about lanes. Its three comm…' -> 'The pending-owner-action derivation, in one module that renders no page and decides nothing about lanes. Its two commit…'
- TC-138 `Method`: 'Run the handback suite: a partial close moves each claimed spec to the terminal partial/ and writes its immutable per-c…' -> 'Run the handback suite: a partial close moves each claimed spec to the terminal partial/ and writes its immutable per-c…'
- TC-147 `Method`: "Run the intake suite against real git repos, red-then-green per trigger (trigger (b) keys on the close's immutable REPO…" -> "Run the intake suite against real git repos, red-then-green per trigger (trigger (b) keys on the close's immutable REPO…"
- TC-194 `Method`: 'Drive blocked rows, Drafted or drifted SRs, tracked pauses and malformed pauses through the facade that used to own the…' -> 'Drive Drafted or drifted SRs, tracked pauses and malformed pauses through the facade that used to own the derivation. A…'
- TC-194 `Verifies`: 'SR-168;LLR-198;IF-138' -> 'SR-168;LLR-198'

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
