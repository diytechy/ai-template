+++
id = "WI-452"
title = "Resurface LLR-165's carrier converter as the downstream-resync helper it now is (owner-ruled 2026-08-13, sitting decision 2.3): the 2.3 status lift treats SR-147/LLR-165/TC-160 as shipped one-shot migration machinery, but the owner's ruling adds a forward obligation — a downstream repo re-syncing onto this kit AFTER the carrier cutover still holds its registries on the old markdown/CSV carrier, and migrate_carrier.py's convert()/compare() (LLR-165) is exactly the proven, loss-refusing path for that conversion. Scope: (1) verify the resync surfaces (RESYNC_PACK.md's carrier entry, ADOPTING.md §6, the downstream-resync skill) actually NAME migrate_carrier.py as the adopter's conversion step with its refuse-on-loss contract, and wire the pointer where missing; (2) confirm the converter still runs against a pre-cutover scaffold (the throwaway-clone detector lesson: run it, don't read it) and that TC-159/TC-160 still exercise the path; (3) there is NO requirement that resync be mechanized end to end — helper functions are welcome, a one-command wrapper is optional and only if it stays stdlib and earns its place; do not build orchestration nobody asked for. LLR-165 stays a live row serving the resync effort, not spent history."
specref = "docs/plans/2026-08-13-sitting-2-boundary-and-context.md#55-wi-452--llr-165-resync-helper-resurface"
workstream = "docs"
sr_refs = ["SR-147"]
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++
