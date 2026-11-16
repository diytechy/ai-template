---
name: downstream-resync
description: Use when upgrading an adopted kit or rebuilding a stale requirements spine against the current template. Route full-kit migrations and scoped spine rebuilds through the target kit’s RESYNC_PACK.md, preserving project content and acceptance authority.
stacks: [python, node, powershell, go, rust, any]
domains: [any]
phases: [dev, release]
tags: [adopting, re-sync, kit-version, upgrade, migration]
scope: kit
---

# Downstream re-sync

Use the target kit's `project-trajectory/RESYNC_PACK.md` as the single procedure
home. Read it from the committed kit checkout being adopted, not an old copy in
the project: only the target carries the intervening migration entries.

## Choose the route before changing files

Start with **pack §0**. It distinguishes a full kit upgrade from a scoped spine
rebuild, and handles requests for both. For a rebuild, **§0.1** is the short
route from stakeholder outcomes through a reviewed design and code/test bindings.
For a full upgrade, work **§1** in order; it selects the necessary ownership
reviews, migrations and concept translations in §2–§4, and finishes with the
verification in §1.4.

The pack owns the steps and their completion conditions. Change those there;
use the spine-authoring skill where the pack calls for tier judgment.
