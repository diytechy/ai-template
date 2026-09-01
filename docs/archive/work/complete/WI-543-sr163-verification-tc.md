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
   **Wired to a delivered command (REVIEW-A rework):** `mapping_purpose_over_repo`
   assembles the real inventory, spine, and declared-absences ledger and grades
   them, exposed as the warn-first `gen_arch_map.py --mapping-purpose` REPORT MODE
   (the `--backlink-coverage` sibling). **Round-2 closure:**
   `bootstrap.delivery_inventory()` now enumerates the physical kit independently
   of MAPPING, partitioning each source across a static row, a conditional
   materialization, or the fail-safe reasoned
   `project-trajectory/mapping-source-exclusions` carrier, and separately names
   every fresh-scaffold generator output. The checker diffs that universe before
   grading purposes/destinations; an omitted shipped source is `missing_file`
   (GATE), a vanished or contradictory declaration is `stale_entry` (GATE), and
   generated outputs inherit their generator source's reference.
3. **The direct TC on SR-163** — TC-204 (`tests/test_mapping_purpose.py`, Smoke
   tier, registered Drafted; approving it is the owner's act) plants one defect
   of each class on a synthetic scaffold plus a clean control and asserts each is
   reported, proves a generated output inherits a resolving generator mapping,
   drives the checker over the real package + MAPPING + exclusions + spine, and
   asserts every physical source is classified, no gate-class finding survives,
   and every filled reference resolves. Its `_real_mapping_findings` runs the
   delivered `mapping_purpose_over_repo`; the separate slow CLI module drives the
   shipped command and removes the REAL `process.toml.template →
   docs/process.toml` row in a child process, requiring exit 1 plus a
   `missing_file` report naming the still-physical source.
4. **The burn-down begun, not finished** — 20 references filled to unambiguous
   EXISTING SRs; no new SR needed (no filled file lacked a justifying
   requirement). **Baseline for the burn-down:** of 147 MAPPING rows, 20 carry a
   resolved reference and **127 remain bare** (unmapped_file WARN); 0 unresolved,
   0 missing, 0 stale over the real inventory. The independent census additionally
   exposes 25 generated/materialized outputs whose generator/direct purpose cell
   is still bare, for 152 warn-class findings total and zero gate-class findings.
   The 127 remains the MAPPING-row burn-down baseline; gating flips only at zero,
   per the ruling.
   <!-- fig: cmd="python3 -c 'load bootstrap/gen_arch_map; count delivery_inventory and mapping_purpose_over_repo'" rev=this-worktree -->

Harness records the original ratchet changes plus the two review closures:
`bootstrap.py` 1600 → 1652 SLOC and `gen_arch_map.py` 1394 → 1433 SLOC for the
independent census/diff, with every function still below the C901 floor; smoke
membership stays within its existing 1458 ceiling. The affected 160-test slice
passed with one skip. Full unfiltered suite: 3204 passed, 24 skipped, and the one
known work-branch-only failure in
`test_this_repo_s_committed_stage_is_current` after TC-204 changed a declared
stage input; `docs/stage` is generated only by the trunk lane and is forbidden
on this worker branch, while the branch-aware freshness step skips it by design.
<!-- fig: cmd=".venv/bin/python -m pytest -q -n auto" rev=this-worktree -->
No new LLR or `stack.ini` step. Full design/verification record in
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

REWORK context (REVIEW-A round 2): wiring the checker to a CLI did not make an
inventory omission observable. `mapping_purpose_over_repo` still passed only
`bootstrap.mapping_entries()` to the pure checker, so the manifest defined its
own universe; removing the `process.toml.template → docs/process.toml` row in
memory returned no finding. The fix must enumerate the delivered kit package
independently, including generator-derived outputs, rather than add another
caller-side guard around the same circular input.

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
