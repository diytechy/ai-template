### REVIEW-A — WI-569 — cross-family round on the four SR-163 spine rows

**Subject: the four rows, not this lane's diff.** This is the ONE clean
cross-family reviewer round the WI-508 lane never landed — the "fresh reviewer
round on a refreshed tree" its own handback report lists under *Not delivered* —
drawn here on CURRENT trunk `2f660cb7`, before this lane had written anything to
the spine. It asks whether `LLR-203`, `LLR-204` (`Approved`), `TC-199` and
`TC-200` (`Drafted`) stand in the state they claim. The lane's OWN verdict is a
separate artifact (`docs/reviews/WI-569-REVIEW-A.md`) and is not this file.

Drawn on the cross-family strong route `OPENAI-SOL` (`docs/agents-enabled`), the
reviewer being a different model family from the author, per
`docs/agents.toml`'s "reviews get real family diversity". Brief: hostile,
read-only, told the rows' identity and the standing-claim rule and nothing about
what had changed on trunk — the reviewer found `WI-543`'s mechanisms itself.
Route command: `codex exec -c model_reasoning_effort=medium --model gpt-5.6-sol`,
prompt on stdin, return captured with `--output-last-message`.

The return follows VERBATIM, through its verdict line. The author's
re-verification of each finding is below it, marked as such.

---

Model: gpt-5.6-sol

I READ `docs/requirements/low-level-requirements.toml:2134-2155`, `docs/test/test-cases.toml:2014-2033`, and parent `docs/requirements/system-requirements.toml:779-789`. I traced the newer implementation through `bootstrap.mapping_entries` at `project-trajectory/scripts/bootstrap.py:2261`, `bootstrap.delivery_inventory` at `:2341`, `gen_arch_map.resolve_requirement_reference` at `project-trajectory/scripts/gen_arch_map.py:2032`, and `gen_arch_map.mapping_purpose_findings` at `:2085`. The requested read-only `git log --oneline -30 -- …/{gen_arch_map.py,bootstrap.py}` showed that WI-543 landed these mechanisms after the reviewed rows.

I DROVE all seven TC-199/TC-200 evidence node IDs with `PYTHONDONTWRITEBYTECODE=1 /Users/diytechy/Documents/ai-template/.venv/bin/python -m pytest -q -p no:cacheprovider …`; all seven passed in 1.99s. Their methods accurately describe the evidence at `tests/test_dogfood_sync.py:717-771`, `tests/test_bootstrap.py:1244-1269,1328-1405`, and `tests/test_gen_arch_map.py:606-633,742-769`. I also DROVE `gen_arch_map.py --mapping-purpose --root .`: it reported all four current classes, with `missing_file=0`, `stale_entry=0`, `unresolved_reference=0`, and 152 warn-class `unmapped_file` findings.

I READ `docs/test/report.md:1177-1182`: `sr_refs`, `verifies`, and `test_refs` join coherently, and CMP-009/CMP-006 correctly own `bootstrap.py`/`gen_arch_map.py` per `docs/requirements/components.toml:1-26`. The four cited legacy symbols exist, but the actual SR-163 mechanisms named by TC-204 are absent from every LLR `code_symbol` cell.

## Findings

- [MAJOR] docs/requirements/low-level-requirements.toml:2136 -> LLR-203's Approved title, detail, and rationale claim that MAPPING carries no purpose reference, no check resolves one, omitted kit files are outside every walk, and bootstrap's exclusion is only prose; current MAPPING has third-field references (`bootstrap.py:1721`), `mapping_entries` exposes them (`:2261-2271`), `delivery_inventory` independently walks physical sources (`:2341-2396`), `resolve_requirement_reference` performs the SR-to-need join (`gen_arch_map.py:2032-2046`), and `mapping-source-exclusions:19` records bootstrap for the mechanically read exclusion census -> Rewrite LLR-203 around the current `MAPPING/mapping_entries/delivery_inventory` design, replace every obsolete NOT-DISCHARGED assertion with the actual remaining condition, update `code_symbol`, bind the applicable TC-204 evidence, and re-review the row before retaining Approved.
- [MAJOR] docs/requirements/low-level-requirements.toml:2150 -> LLR-204 still names only the reverse-backlink symbols and asserts that this grammar and `backlink_coverage_min` are what SR-163's future join and policy would use; current SR-163 instead uses MAPPING's reference field, `MAPPING_FINDING_POLICY` (`gen_arch_map.py:2003-2008`), `resolve_requirement_reference`, `mapping_purpose_findings`, and `mapping_purpose_over_repo` (`:2188-2234`), none of which any design row owns, while TC-204 verifies SR-163 directly at `docs/test/test-cases.toml:2069-2076` -> Replace LLR-204's counterfactual backlink decomposition with design ownership of the delivered mapping-purpose resolver/checker/policy and link TC-204 to the owning LLRs, or mint equivalent design rows and re-parent that evidence; then re-review the changed design claim.

VERDICT: CHANGES-REQUESTED findings=2

---

## The author's re-verification (WI-569)

A finding is not accepted because a reviewer asserted it. Every anchor above was
re-driven independently at trunk `2f660cb7`, and the round was drawn only after
the author had formed a separate reading — which it then corroborated without
having been shown it.

**Both MAJORs CONFIRMED.** The three LLR-203 assertions are false of the tree,
and each was falsified by driving, not by reading:

| the row's claim | what the tree does | how it was driven |
| --- | --- | --- |
| "no cell joins an inventoried file to a requirement id … no check resolves" | 21 of 148 MAPPING rows carry a third requirement cell; `resolve_requirement_reference` is the SR→need join | `gen_arch_map.py --mapping-purpose --root .` → `unresolved_reference — 0 finding(s) [WARN]`, i.e. all 21 resolve to a live need |
| "every arm above walks the DESTINATIONS the inventory declares, never the shipped tree" | `bootstrap.delivery_inventory()` walks the physical kit tree independently of MAPPING | called directly: 213 physical sources, 148 MAPPING sources, 31 exclusion rows, 34 sources in neither |
| "the installer is excluded … in prose at its module rather than as a row in the exclusion carrier" | it is a row | `project-trajectory/mapping-source-exclusions:19` — `scripts/bootstrap.py — installer/generator run from the kit; deliberately not scaffolded`, parsed by `_mapping_source_exclusions()` |

fig: driven="`/Users/diytechy/Documents/ai-template/.venv/bin/python project-trajectory/scripts/gen_arch_map.py --mapping-purpose --root .` at 2f660cb7 (missing_file 0 / stale_entry 0 / unresolved_reference 0 / unmapped_file 152), and `bootstrap.delivery_inventory()` called in-process at the same commit (213 / 148 / 31 / 34)"

The reviewer's LLR-204 reading also holds: the delivered join rides
`MAPPING_FINDING_POLICY` (`gen_arch_map.py:2003`) and the inventory's reference
cell, not `backlink_ids` or `read_backlink_min` — `read_backlink_min`'s only
call site is `gen_arch_map.py:1952`, inside the backlink report. The row's
closing sentence predicted the parent's join would ride this grammar and this
dial. It did not.

**One imprecision in finding 1, recorded rather than quietly dropped — and it
survives anyway.** The finding bundles LLR-203's *title* with its detail and
rationale as though the three made the same claim. They do not: the title said
"carrying no purpose reference", which is weaker and vaguer than the detail's
flat "no check resolves". But weaker is not true — the inventory does carry
purpose references now — so the title was corrected with the rest rather than
defended on the technicality. The finding is accepted on all three anchors.

**What TC-199 and TC-200 stand at: CONFIRMED, no finding.** All seven evidence
node ids exist and pass (re-driven: `7 passed in 2.80s`), their `verifies` cells
name the LLR arm and not `SR-163`, and their `expected` cells still say
truthfully that SR-163's complete join and shipped-file universe are not covered
by them. TC-199's claim that its two package-direction nodes are also TC-176's
evidence checks out exactly: the intersection of the two `evidence` sets is
those two nodes, and TC-176 (`Approved`) verifies `SR-166`/`LLR-181`. The two
rows stay `Drafted` by ruling and nothing here disturbs that.

**Disposition, and what this lane did NOT take.** The falsified sentences were
corrected in-lane at `33aee707`; `Status` stayed `Approved` on both rows,
because the approval act is the adjudicator's and an amendment to an approved
row is expressly not one. The DESIGN half of both remedies —
which row owns `resolve_requirement_reference` / `mapping_purpose_findings` /
`MAPPING_FINDING_POLICY`, whether LLR-203's `CodeSymbol` widens, and where
TC-204's evidence binds — is a chain-reading call and was deliberately left
undone here. It is not left on no queue: it is stated as the standing
NOT-DISCHARGED gap in LLR-203's own cell, and the amendment adjudication that
`intake` mints at this lane's merge is confirmed to list both rows
(`acceptance_record.staged_spine_amendments` over `2f660cb7..HEAD` returns
`LLR-203`, `LLR-204`), so the adjudicator reads the finding where they will
look for it.
