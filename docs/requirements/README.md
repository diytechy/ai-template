<!--
Contracts: IF-021, IF-033, IF-034, IF-051, IF-059 — the interface seams this
directory declares (process.md §8; rows of record in interfaces.toml).

Contract IF-021: the requirement spine as one joinable registry set. One
    id-keyed TOML file per tier, one table per row (`[requirement.SR-137]` and
    its siblings), where the id is the TABLE KEY — so a duplicate id is a decode
    error, a refs cell is a typed array rather than a split string, and an unset
    cell is an absent key rather than an empty one. Rows are handed back under
    the registries' own column names, and a `-000` example row is inert. The
    tiers join by id into the traceability graph, together with the off-spine
    registries kept beside them.
Contract IF-033: the same registries read as the source of a typed-concept
    export — one concept per row per tier plus a per-tier index, joined with the
    derived summaries of the process documents. Every tier is absent-tolerant, so
    a repo missing a registry contributes no concepts for it rather than failing.
Contract IF-034: the registries read as the release checklist's source — the
    stakeholder needs and their acceptance intent, the system requirements whose
    verification is a human method, the release-tier and manual test cases, the
    declared interface seams, and the performance budgets whose warn tier never
    fails a gate. Each optional registry is absent-tolerant and simply
    contributes no section.
Contract IF-051: the registries read as MATURITY evidence. Each SR, LLR and TC
    row offers its `status`, and the stakeholder needs offer their section
    state, and those together decide which ladder rung a row set stands at.
    `-000` example rows are dropped, and an ABSENT registry and an EMPTY one are
    deliberately different answers, so the applies-when flag travels with the
    rows it qualifies.
Contract IF-059: the two registries a planning brief may embed, and nothing
    else. The system requirements offer id, title and requirement text; the
    interface rows offer id, owner, far side, channel and data. Both are handed
    to a planner VERBATIM as authority, so each cell is written as a link list
    and never as narrative. The two-file read IS the redaction boundary: the
    status blackboard, the log and every self-assessment are unreachable from it
    by construction.
-->

# `docs/requirements/` — the requirement spine and its off-spine registries

One id-keyed TOML file per tier, hand-authored and machine-read. The spine is
[`stakeholder-needs.toml`](stakeholder-needs.toml) →
[`system-requirements.toml`](system-requirements.toml) →
[`low-level-requirements.toml`](low-level-requirements.toml), verified by the
test cases in [`../test/`](../test/). Beside it sit the off-spine registries:
the system frame ([`external.toml`](external.toml)), the seams
([`interfaces.toml`](interfaces.toml)), the components
([`components.toml`](components.toml) and its derived counterpart), the
perspectives ([`hats.toml`](hats.toml)), the owner decisions
([`open-items.toml`](open-items.toml)) and the performance budgets
([`performance-budgets.csv`](performance-budgets.csv)). Every row's id is the
table key, so a duplicate id cannot be written; a `-000` row is a permanent
inert example. What each field means and which check enforces it is in
[the registry machinery reference](../registry-machinery-reference.md).
