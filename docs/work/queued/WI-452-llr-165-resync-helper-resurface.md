+++
id = "WI-452"
title = "Resurface LLR-165's carrier converter as the downstream-resync helper it now is (owner-ruled 2026-08-13, sitting decision 2.3): the 2.3 status lift treats SR-147/LLR-165/TC-160 as shipped one-shot migration machinery, but the owner's ruling adds a forward obligation — a downstream repo re-syncing onto this kit AFTER the carrier cutover still holds its registries on the old markdown/CSV carrier, and migrate_carrier.py's convert()/compare() (LLR-165) is exactly the proven, loss-refusing path for that conversion. Scope: (1) verify the resync surfaces (RESYNC_PACK.md's carrier entry, ADOPTING.md §6, the downstream-resync skill) actually NAME migrate_carrier.py as the adopter's conversion step with its refuse-on-loss contract, and wire the pointer where missing; (2) confirm the converter still runs against a pre-cutover scaffold (the throwaway-clone detector lesson: run it, don't read it) and that TC-159/TC-160 still exercise the path; (3) there is NO requirement that resync be mechanized end to end — helper functions are welcome, a one-command wrapper is optional and only if it stays stdlib and earns its place; do not build orchestration nobody asked for. LLR-165 stays a live row serving the resync effort, not spent history."
specref = "docs/plans/2026-08-13-sitting-2-boundary-and-context.md#01-the-sitting-pack-decisions-dispositioned"
workstream = "docs"
sr_refs = ["SR-147"]
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

**TC-159 is a `Draft` row — confirm, do not lift (correction ledger #8).**
Part (2) says *"confirm … that TC-159/TC-160 still exercise the path."* Live:
TC-159 `Draft` (verifies SR-147 + LLR-165), TC-160 `Planned`, LLR-165 `Planned`
with `test_refs = TC-159`. Pack §2.3 lifted TC-160 and never TC-159. **Lifting
TC-159 is a spine window and belongs to sitting 3 §2.2** — this row confirms
the path runs and records the chain gap; it does not flip a Status.

**The surface list is fed by two other programs — run last or scope to today.**
Part (1)'s surface list grows if/when `external.toml` lands (a new registry
earns a resync entry) and again when `docs/architecture.md` retires (D8 — a
scaffold-surface change is a declared re-sync entry). Either sequence this row
**after** both, or state explicitly that it covers only the surfaces live at
its start and that those two programs each carry their own resync entry.
(The old IF-103 tension is DISSOLVED — 13u retires `Stability`, so the
converter's maturity is not the frame's business. No action here.)

