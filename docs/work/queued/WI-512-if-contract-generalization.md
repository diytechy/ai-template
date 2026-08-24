+++
id = "WI-512"
title = "Interfaces `contract`: the staged (a) pass toward (b), the named-symbol tripwire, and `verified_by` (OI-61 ruled)"
specref = "docs/requirements/open-items.toml#OI-61"
workstream = "requirements"
needs = ["WI-455"]
buildtier = "strong"
safety_class = "spine"
priority = 3
+++

## Context

Executes `OI-61`'s ruling in full (owner, in session 2026-08-23, verbatim:
*"OI-61: I agree with the recommendation, let's see where it lands, and I
approve of the other spine changes surfaced in open-items.html"*). Record:
[../../log.d/2026-08-23-oi61-rule-and-spine-approval.md](../../log.d/2026-08-23-oi61-rule-and-spine-approval.md).
`buildtier = "strong"` deliberately, not `medium`: the row re-authors 27 cells
of a SHIPPED registry, adds a cell to its schema, and touches
`INTERFACES.template.md` / `registries/interfaces.template.toml` / `PROCESS.md`
§8's field list / `EXAMPLE.md` / `tests/test_dogfood_sync.py` parity + a
`RESYNC_PACK.md` entry — spine-touching and design-shaping on both counts.

**The ruling's four parts, in the order they execute.**

1. **(a), STAGED AND DECLARED AS THE FIRST STEP TOWARD (b).** The 27 `Provides`
   rows whose `contract` contains `CLI:` thin to the typed crossing statement —
   *"SR-xxx's obligation delivered as a CLI at `<module>`; crosses B-05"* —
   what crosses, who owns it, which boundary; flags and exit codes are read
   from the owner SR plus the module. The census the pass is measured against
   is on OI-61's row: 27 rows, all `Provides` (59% of that tier), 26 of them
   literally opening `<module>.py CLI:` (`IF-053` the exception), owner split 9
   `SR-###` / 18 `LLR-###`, seven tied to `B-05`; cell length min 128 / median
   180 / mean 273.5 / max 800, with four over the ruled 500-char ceiling
   (`IF-121` 587, `IF-015` 722, `IF-044` 788, `IF-103` 800). The short form is
   not an invention: `external.toml`'s `B-05` row already RULES these as
   package content in its own `carries` cell.
2. **(a) STEP TWO — THE GENERATED CLI REFERENCE**, derived from each module's
   argparse by stdlib introspection and spliced into a marker block, in the
   `gen_arch_map.scan_inventory()` harvest pattern. It rides this row rather
   than a separate one: same argparse surface, walk already exists, and
   "generated-not-hand-maintained" is the kit's own rule applied to its own
   registry.
3. **(d)'s NAMED-SYMBOL TRIPWIRE, SCOPED TO SURVIVING PROSE.** One warn-first
   rule in `trace.if_contract_advisories` reusing WI-502's AST grammar: a
   `SCHED_*` / `Foo.bar` / `CONSTANT_NAME` token in a `contract` must resolve
   under the declared source surface, and a named path must exist. Taken WITH
   (a), never instead of it. The bar it must clear: it would have caught
   `IF-055` on the day `SCHED_*` was deleted. It will NOT reach `IF-080`, whose
   rot is a true-looking English phrase naming nothing symbolic — that residue
   is (c)'s, deliberately.
4. **THE `verified_by` MECHANISM, SANCTIONED WARN-FIRST.** An optional cell on
   the IF row taking a TC id or an LLR id, empty meaning "verified in its own
   right", warn-first that the pointer resolves. It makes "verified by the
   parent functionality's tests, pointer recorded" sayable for a low-level
   seam, which today the `Verification` vocabulary cannot express at all (its
   only exemption is LLR-exemption for `Analysis`/`Inspection`/`Attest`, and IF
   rows carry no `Verification` cell).

**Sequencing, binding.** (a) runs AFTER `WI-455` item 1's `counterpart` →
`consumers` rename (`OI-60` ruled (a)) — hence the hard `needs` edge. That
rename is what makes `B-05` the declared consumer for the adopter-facing rows,
so the short form points at a real cell rather than a phrase.

**What this row must NOT do.** It does not re-decide the nine CLI rows that are
also in the twelve-row SR-owned `Provides` report
([../../plans/2026-08-23-sr-owned-provides-report.md](../../plans/2026-08-23-sr-owned-provides-report.md)):
ownership and contract content are separate judgements on the same rows, and
running them in one pass makes each one's evidence unreadable. It does not
execute (b) registry-wide, and it does not add the (c) hat.

**What this row OWES BACK, because (c)'s deferral is conditioned on it.** The
close must state the NUMBER the owner's "let's see where it lands" asks for:
how much of what those 27 cells said turns out to be missed by any reader once
it is gone, and what residual rot class (if any) survived both (a) and (d).
That measurement is the trigger to re-raise (c) — and the input to whether (b)
runs across the other 108 rows.
