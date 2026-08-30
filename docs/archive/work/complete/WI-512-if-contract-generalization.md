+++
id = "WI-512"
title = "Interfaces `contract`: the staged (a) pass toward (b), the named-symbol tripwire, and `verified_by` (OI-61 ruled)"
specref = ""
workstream = "requirements"
needs = ["WI-455"]
buildtier = "strong"
safety_class = "spine"
priority = 3
+++

## Deliverable

`OI-61`'s ruling executed in full, in the order the ruling states. Record:
[../../../log.d/2026-08-24-wi512-contract-generalization.md](../../../log.md#2026-08-24--wi-512-the-interface--stops-restating-its-owner-and-two-new-warn-first-rules-read-what-the-old-four-could-not).

**The census, re-measured first.** `WI-455` moved the IF schema between this
brief's writing and its execution, so nothing was designed against the brief's
numbers. The row SET holds exactly — 135 live rows, the same 27 carrying `CLI:`,
the same owner split (9 `SR-###` / 18 `LLR-###`), the same seven `B-05` ties,
the same four over-ceiling breaches, the same length distribution. The row SHAPE
moved: `direction`/`this_project`/`counterpart` are gone, and `provider` survives
on only 9 of the 27. One brief figure was refuted rather than repeated — 22 of
27 open on a literal `<module>.py CLI:`, not 26.

**(a) THE NUMBER, which is what the row owed back.**

| | before | after |
|---|---|---|
| rows | 27 | 27 |
| total characters | **7,385** | **2,613** |
| min / median / mean / max | 128 / 180 / 273.5 / 800 | 54 / 70 / 96.8 / 220 |
| over the ruled 500-char ceiling | 4 | **0** |

**−4,772 characters, −64.6%.** Of the 2,613 surviving, 1,705 is the pure
crossing statement and **908 characters over 11 rows is the IRREDUCIBLE
REMAINDER** — a typed fact the owner row does not state. **Sixteen rows thinned
to the crossing statement with nothing left over.** Read as the owner's
question — how much of what those cells said is missed once it is gone —
**908 of 7,385 characters, 12.3%**; the other 87.7% was recoverable from the
owner row, the module, or the generated CLI reference. The reading: (b) is worth
running across the other 108 rows, with the same per-row review, because one row
in seven carried something real. The full per-row dossier (old chars, new text,
each displaced clause's home) is in the log fragment.

**(a) step two: the generated CLI reference LANDED** (the ruling puts it on this
row, not a later one). `gen_arch_map.py` gains `--cli-doc FILE` — an AST read of
every scanned module's `argparse` tree, never an import — rendering the module
summary, its declared `Contracts: IF-###` line and a flag/help table into a
`CLI REFERENCE` marker pair. Its own mode, needing no `--doc`, so adopting it
never re-commits the module map `WI-455` retired. Four things landed together:
`docs/cli-reference.md`, the `[generated]` row of kind `cli`, `check.py`'s
`cli-reference` step (built-in, hook floor, trunk-lane stand-down) and
`trunk_step.py --regen`'s table — the last two together, since standing a step
down on a branch is only honest when the trunk can regenerate it.

**(d)'s tripwire, scoped to the surviving prose.** A fifth warn-first rule in
`trace.if_contract_advisories`, reusing `gen_arch_map.implements_report` (the one
AST walk): a `SCHED_*` / `Foo.bar` / `CONSTANT_NAME` token must resolve in the
declared source surface, and a path whose first segment is a real directory must
exist. **The acceptance case passed against the live tree, unplanted** — the
first run reported `IF-055 Contract names SCHED_*`. Initial live count **7
findings over 5 rows** (`IF-055` real rot; `IF-038`, `IF-072`, `IF-061`,
`IF-132`, `IF-143` judgement calls), none among the 27 rewritten, all left
standing because re-authoring rows outside the CLI family is (b)'s pass. The
narrowing is the design and was measured: **39 → 7** as four false-positive
classes were declined outright, with `SCHED_*` surviving every one. Vacuous
where there is no surface, since an empty surface would report every name as
dead.

**`verified_by` sanctioned warn-first.** An optional IF cell taking a `TC-###`
or an `LLR-###`; empty means "verified in its own right". Only resolution is
checked. It makes sayable what the `Verification` vocabulary cannot state at all
for a low-level seam. No live row claims it — filling one would invent a per-row
judgement this row was not asked to make — and it ships documented in the
template, `INTERFACES.template.md`, `PROCESS.md` §8 and `EXAMPLE.md`.

**Adopter surfaces:** `registries/interfaces.template.toml` (the `verified_by`
key + the no-restatement instruction with its worked short form),
`INTERFACES.template.md`, `PROCESS.md` §8, `EXAMPLE.md`, `ADOPTING.md`, and a
`RESYNC_PACK.md` entry `[since 3cf43e2e]` carrying all four changes with their
migration order. `kitlib/spine.py`, `spine_carrier.py` and `migrate_carrier.py`
take the new key so nothing drops the cell on the way through a carrier.
Nothing here breaks a legacy registry: the cell is optional, both new rules are
warn-first, the reference is opt-in.

**Deferrals, stated rather than implied.** (c) is NOT re-raised: its condition is
three-clause, and (a) landing plus (d) reporting is two of them — the third,
*a residual rot class demonstrated that neither reached*, needs (d)'s findings
triaged first. `IF-080`'s class is still the standing candidate, still live, and
still unreached by anything shipped here.

## Context

Executes `OI-61`'s ruling in full (owner, in session 2026-08-23, verbatim:
*"OI-61: I agree with the recommendation, let's see where it lands, and I
approve of the other spine changes surfaced in open-items.html"*). Record:
[../../../log.d/2026-08-23-oi61-rule-and-spine-approval.md](../../../log.md#2026-08-23--oi-61-ruled-the-surfaced-spine-set-approved-and-nineteen-drafts-the-owner-surface-never-showed).
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
([../../../plans/2026-08-23-sr-owned-provides-report.md](../../../plans/2026-08-23-sr-owned-provides-report.md)):
ownership and contract content are separate judgements on the same rows, and
running them in one pass makes each one's evidence unreadable. It does not
execute (b) registry-wide, and it does not add the (c) hat.

**What this row OWES BACK, because (c)'s deferral is conditioned on it.** The
close must state the NUMBER the owner's "let's see where it lands" asks for:
how much of what those 27 cells said turns out to be missed by any reader once
it is gone, and what residual rot class (if any) survived both (a) and (d).
That measurement is the trigger to re-raise (c) — and the input to whether (b)
runs across the other 108 rows.
