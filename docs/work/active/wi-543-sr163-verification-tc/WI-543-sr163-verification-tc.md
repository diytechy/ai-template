+++
id = "WI-543"
title = "SR-163's owner: the tolerant requirement-reference cell, the four-class checker warn-first, the direct TC (OI-72)"
specref = "docs/requirements/system-requirements.toml#SR-163"
workstream = "requirements"
sr_refs = ["SR-163"]
needs = []
buildtier = "strong"
safety_class = "spine"
priority = 3
+++

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
