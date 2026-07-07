# ID blocks — per-track reservations

*Applies only under the parallel-tracks layer (process-options.md "Parallel
tracks"); a single-lane repo ignores this file.* When several development tracks
grow requirements **at the same time** as off-spine scope drafts, each draws
**new** `SN`/`SR` ids from a reserved hundreds-block so two drafts never mint the
same id before the integrator lands them. This is a **convention**, not a machine
check — `trace.py` still enforces integrity (no duplicate/malformed ids) across
the whole repo at landing; the blocks just keep concurrent drafts from colliding
in the first place. Registry rows land through the **integrator** at
ratification, so the human bottleneck is the final collision guard.

## Reservations

_(One row per track — edit for yours; the ranges below are examples.)_

| Track / owner | `SN` block | `SR` block |
| --- | --- | --- |
| **Shared / core** (integrator) | SN-000–099 | SR-000–099 |
| **`<track-a>`** | SN-100–199 | SR-100–199 |
| **`<track-b>`** | SN-200–299 | SR-200–299 |

## Notes

- **Rows predating the split keep their ids** — ownership is read from each row's
  `Area`/`Module` tag, not renumbered. Only **new** rows use the blocks above.
- **`LLR`/`TC` are integrator-allocated, sequentially, at G2 decomposition** —
  they are created when a scope draft lands (through the integrator), so parallel
  drafts never race for them. A draft may use placeholder ids (`LLR-D1`, `TC-D1`)
  in its off-spine text; the integrator assigns the final sequential ids at
  landing. No per-track LLR/TC block is needed.
- **Off-spine registries share one file each, track-associated by tag/owner:**
  `procurement.csv` (`PART-###`), `performance-budgets.csv` (`PB-###`),
  `interfaces.csv` (`IF-###` — cross-track seams), `assets.csv` (`ASSET-###`).
  These are integrity-only (off the joined spine) and integrator-managed; no
  hundreds-block split — a new row appends the next sequential id at landing.
