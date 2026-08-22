+++
id = "WI-509"
title = "Pin the kit-path invariant and document where the machinery lives (OI-59 ruled (a)+(c), 2026-08-22)"
specref = "docs/requirements/open-items.toml#OI-59"
workstream = "scripts"
sr_refs = []
needs = []
buildtier = "quick"
safety_class = "ordinary"
priority = 2
+++

## Context

Executes OI-59 (a)+(c): bootstrap.py stays out of MAPPING (the bundle IS
the kit folder; the scaffold is the product), and the recurring defect
class — instructions addressing bootstrap/migration machinery at a
SCAFFOLD path the adopter does not have (the WI-498 slice-5 recovery hit
it live) — is made unrepresentable:

1. **The pin**: a test sweeps every shipped instructing surface
   (RESYNC_PACK, ADOPTING, KICKOFF, templates, docstrings the scaffold
   receives) for invocations of bootstrap/migration machinery and asserts
   each addresses the KIT path form, never a bare scaffold-relative one.
2. **The paragraph**: ADOPTING.md's "where the machinery lives" — the kit
   folder is the tool, the scaffold is the product, keep the tool; deleting
   the kit folder after init forfeits resync/migration, by design.
(b) — shipping a second installer copy into the scaffold — is DECLINED by
the ruling: version skew between two installers is the drift class the kit
exists to prevent.
