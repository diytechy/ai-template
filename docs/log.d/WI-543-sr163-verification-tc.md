## 2026-08-31 — WI-543: SR-163's owner — the tolerant reference cell, the four-class checker warn-first, the direct TC (OI-72)

Re-scoped row per `OI-72`'s ruling (log.md 2026-08-31). SR-163's verification is
mechanism-first: ship the tolerant `MAPPING` reference cell, a checker that runs
the four finding classes over the real inventory, and a direct TC on SR-163 that
proves the checker catches each class on a scaffold — with the reference
burn-down begun, not finished.

### Build (in progress)

1. **Tolerant cell** — `bootstrap.py::MAPPING` rows may carry a requirement
   reference as an optional third element; a `mapping_entries()` reader
   normalizes every row to `(src, dst, ref|None)` so a bare pair keeps working
   and is by definition an unmapped-entry warning. All consumers (copy pass,
   dogfood walk, kit-path invariant, resync/profile tests) read tolerantly.
2. **The checker** — `<home TBD>` resolves each reference SR → stakeholder need,
   checks each destination, names every bare pair, and maps a generated output
   through its generator's row; the declared policy assigns warn vs gate per
   class (unresolved + unmapped start WARN; shipped default for unmapped stays
   warn-only; flip to gate is a reviewed commit at count zero).
3. **The direct TC on SR-163** (TC-204) plants each of the four classes on a
   scaffold and proves the checker reports it; its green over the real MAPPING
   is the standing every-file-maps evidence.
4. **Burn-down begun** — references filled where the justifying SR is
   unambiguous; remaining warn count recorded here as the baseline.

Baseline warn count (references still bare): TBD — recorded at close.
