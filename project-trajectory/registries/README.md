<!--
Contracts: IF-039 — the interface seam this directory declares (process.md §8;
row of record in the adopting repo's interfaces registry).

Contract IF-039: the blank registry TEMPLATES a scaffold is built from — one
    `*.template.toml` or `*.template.csv` per tier, copied VERBATIM into the
    target repo's own registry paths. The copy is write-once: an existing
    destination is skipped rather than overwritten, so re-running the scaffold
    over a live repo never clobbers authored content. A force flag overrides
    that for every destination except the id watermark, whose whole content is
    history and which nothing in the tree could rebuild. Each template ships a
    `-000` example row, which every loader skips, so a freshly scaffolded
    registry reads empty and nothing gates on the example.
-->

# `registries/` — the blank forms a scaffold receives

One template per registry tier: the spine (stakeholder needs, system
requirements, low-level requirements, test cases), the off-spine registries
(interfaces, external, components, hats, open items, performance budgets) and
the optional ones (procurement, assets, repos, work items). They are **forms,
not data** — an adopting repo fills its own copies, and this kit's own filled
instance lives in `docs/requirements/` and `docs/test/`. Every template carries a
`-000` example row that every loader skips, so a fresh scaffold is vacuously
clean; a `*.template.*` file must produce something sensible the moment it is
copied and filled.
