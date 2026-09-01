+++
id = "WI-543"
title = "SR-163's owner: the tolerant requirement-reference cell, the four-class checker warn-first, the direct TC (OI-72)"
specref = ""
workstream = "requirements"
sr_refs = ["SR-163"]
needs = []
buildtier = "strong"
safety_class = "spine"
priority = 3
+++

## Deliverable

SR-163's verification shipped mechanism-first, all four done-when met:

1. **The tolerant cell** — `bootstrap.py::MAPPING` rows may carry a requirement
   reference as an optional third element; `bootstrap.mapping_entries()`
   normalizes every row to `(src, dst, ref|None)`, so a bare pair keeps working
   (by definition an unmapped-entry warning) with no flag day — the burn-down IS
   the migration. Every consumer (the copy pass, the dogfood walk, the kit-path
   invariant, the resync/profile tests) unpacks pairs and triples.
2. **The four-class checker** lands in `gen_arch_map.py` (LLR-204's module, the
   purpose-reference home) beside the back-link machinery:
   `mapping_purpose_findings` returns the four classes, `resolve_requirement_reference`
   is the SR → live-stakeholder-need join stated once, `load_spine_index` loads
   the repo's SR/SN registries, `mapping_purpose_report` computes the pass, and
   `MAPPING_FINDING_POLICY` is the one warn-vs-gate home (unmapped/unresolved
   WARN; missing/stale GATE — already delivered/zero via the dogfood+bootstrap
   checks). The stale arm honors the `LIFECYCLE:` marker the dogfood walk applies.
   The flip of a warn class to gate at count zero is a later reviewed commit.
3. **The direct TC on SR-163** — TC-204 (`tests/test_mapping_purpose.py`, Smoke
   tier, registered Drafted; approving it is the owner's act) plants one defect
   of each class on a synthetic scaffold plus a clean control and asserts each is
   reported, drives the checker over the real `bootstrap.MAPPING` + this repo's
   real spine and asserts no gate-class finding survives and every filled
   reference resolves — so the TC claims exactly what it exercises.
4. **The burn-down begun, not finished** — 20 references filled to unambiguous
   EXISTING SRs; no new SR needed (no filled file lacked a justifying
   requirement). **Baseline for the burn-down:** of 147 MAPPING rows, 20 carry a
   resolved reference and **127 remain bare** (unmapped_file WARN); 0 unresolved,
   0 missing, 0 stale over the real inventory. The 127 is the count the burn-down
   retires against; gating flips only at zero, per the ruling.

Harness kept green: the module-size ratchet (`bootstrap.py` +29 SLOC,
`gen_arch_map.py` +79 SLOC) and the smoke membership budget (max-tests 1440 →
1458, +17 in-process TC-204 tests) re-stamped as reviewed baseline edits naming
this WI. No new LLR, no new `stack.ini` step (`bootstrap.py` never ships
downstream, so the kit self-check home is TC-204, which runs the checker over
the real inventory on every suite run). Full design record in
`docs/log.d/WI-543-sr163-verification-tc.md`.

## Context

RE-SCOPED 2026-08-31 by `OI-72`'s ruling (record
`docs/log.d/2026-08-31-owner-rulings-oi70-71-72.md`, compiled into
`docs/log.md`), which also names this row `SR-163`'s OWNING row. The original
scope — author the whole file→requirement→need join before anything counts —
is replaced by mechanism-first: `SR-163`'s own text puts the warn-to-gate
dial in the requirement, so the honest minimal build ships the mechanism, a
direct TC that claims exactly what it exercises, and the reference authoring
as a visible warn-count burn-down rather than a precondition.

The state this row inherits: `SR-163` (Approved, `verification = "Test"`)
names four finding classes. Missing files and stale entries are delivered
(the dogfood walk and bootstrap checks — `TC-199`/`TC-200`'s evidence, rows
Drafted on the wi508 branch until `WI-555` lands them). UNRESOLVED REFERENCE
and UNMAPPED FILE cannot occur because `bootstrap.py::MAPPING` — the declared
inventory — is source→destination pairs with no place to record WHY a file
ships (the undischarged arm `LLR-203` records on-row).

## Done-when

1. **The tolerant cell:** a MAPPING row may carry a requirement reference as
   a third element; the reader accepts both pairs and triples — a bare pair
   is by definition an unmapped-entry WARNING, so downstream inventories keep
   working with no flag day and the burn-down IS the migration.
2. **The checker**, over the real inventory on every run: each reference
   resolves SR → stakeholder need, each destination exists, every bare pair
   is named; a generated output maps through its generator's row; the
   declared policy assigns warn versus gate per class — unresolved and
   unmapped start WARN here and the SHIPPED default for unmapped stays
   warn-only (ruled); the flip to gating is a reviewed commit at count zero.
3. **The direct TC on `SR-163`** proves the CHECKER catches each of the four
   classes on a scaffold (remove a file; plant a bogus reference; leave a
   bare pair; a stale entry) — the checker's green over the real MAPPING is
   the standing every-file-maps evidence, so the TC claims exactly what it
   exercises. Spine rows through the ordinary approval flow under the
   declared dial.
4. **The burn-down begun, not finished:** references filled where the
   justifying SR is unambiguous (most cite EXISTING SRs; a new SR is minted
   only where a shipped file has no justifying requirement — surfacing those
   is the point, per SN-038); the remaining warn count recorded in the close
   fragment as the baseline the burn-down retires against.
