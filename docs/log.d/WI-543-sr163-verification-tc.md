## 2026-08-31 — WI-543: SR-163's owner — the tolerant reference cell, the four-class checker warn-first, the direct TC (OI-72)

Re-scoped row per `OI-72`'s ruling (log.md 2026-08-31). SR-163's verification is
mechanism-first: ship the tolerant `MAPPING` reference cell, a checker that runs
the four finding classes over the real inventory, and a direct TC on SR-163 that
proves the checker catches each class on a scaffold — with the reference
burn-down begun, not finished.

### Build

1. **Tolerant cell** — `bootstrap.py::MAPPING` rows may carry a requirement
   reference as an optional third element; `bootstrap.mapping_entries()`
   normalizes every row to `(src, dst, ref|None)` so a bare pair keeps working
   and is by definition an unmapped-entry warning. All consumers (the copy pass,
   the dogfood walk, the kit-path invariant, the resync/profile tests) unpack
   pairs and triples.
2. **The checker** — in `gen_arch_map.py` (LLR-204's module, the purpose-
   reference home), the forward direction beside the backlink machinery:
   `mapping_purpose_findings(entries, present, sr_by_id, sn_ids,
   declared_absences)` returns the four classes; `resolve_requirement_reference`
   is the SR → live-stakeholder-need join stated once; `load_spine_index` loads
   the repo's SR/SN registries; `mapping_purpose_report` computes the pass.
   `MAPPING_FINDING_POLICY` is the one home for warn-vs-gate: `unmapped_file` and
   `unresolved_reference` WARN, `missing_file` and `stale_entry` GATE (they are
   already delivered/zero via the dogfood+bootstrap checks). The stale arm
   honors the `LIFECYCLE:` marker, the same rule the dogfood walk applies. The
   flip of a warn class to gate at count zero is a later reviewed commit.
3. **The direct TC on SR-163** — TC-204 (`tests/test_mapping_purpose.py`, Smoke
   tier so it runs on every commit bar): plants one defect of each class on a
   synthetic scaffold plus a clean control and asserts each is reported; drives
   the checker over the real `bootstrap.MAPPING` + this repo's real spine and
   asserts NO gate-class finding survives (the standing every-file-maps
   evidence) and every filled reference resolves. Registered Drafted (SR-163 is
   Approved; approving TC-204 is the owner's act).
4. **Burn-down begun** — 20 references filled to unambiguous EXISTING SRs
   (`SR-049` derived stage, `SR-137` one policy home, `SR-146` prompts ×9,
   `SR-147` spine registries ×3, `SR-159` interfaces ×2, `SR-015` perf budgets,
   `SR-151` hosted CI, `SR-161` hats). No new SR needed yet — no filled file
   lacked a justifying requirement.

**Baseline (recorded for the burn-down):** of 147 MAPPING rows, 20 carry a
resolved reference and **127 remain bare (unmapped_file WARN)**; 0 unresolved, 0
missing, 0 stale over the real inventory. The 127 is the count the burn-down
retires against; gating flips only at zero, per the ruling.

### Design notes

- No new LLR: the ruling keeps the wi508 rows (LLR-203/204, TC-199/200) as they
  are and makes TC-204 a DIRECT test on SR-163. The checker's functions carry no
  `Implements:` tag / LLR — back-link coverage is warn-only, and the mechanism
  is verified by its direct TC.
- No new `stack.ini` step: `bootstrap.py` is excluded from its own MAPPING and
  never ships downstream, so a harness step over `bootstrap.MAPPING` would be
  dead in every adopter. The kit self-check home is the test, which runs the
  checker over the real inventory on every suite run — the "on every run"
  evidence the ruling asks for. An adopter with their own inventory can call the
  `gen_arch_map` functions directly.
