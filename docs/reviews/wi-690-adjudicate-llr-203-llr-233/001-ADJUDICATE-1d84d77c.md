# ADJUDICATE — WI-690 — amendment at 1d84d77c

Independent adjudication of the two approved design rows WI-616 amended in
place under the coordinator's wave-5 grants: LLR-203 (Detail, Rationale) and
LLR-233 (Detail). The one question, per row: MEANING or CLARITY. Brief: the
kit's amendment brief rendered for this row (`adjudicate_brief.compose`, anchor
`docs/archive/last_approved` copied at 464dc7ac for the LLR registry), with the
caller's addition: each new text was checked against the code and tests it
names on this tree before it was blessed. I directed neither amendment and read
no session's account of it. HEAD stayed at 1d84d77c throughout; the worktree
was clean before this file was written.

The dial: `human_approval_through = "DevStg-Boundary"`, so the LLR rung is
released and a MEANING verdict is re-attested by this session in the one
snapshot act batch C shares.

- [MEANING] LLR-203 Detail, Rationale -> the shipped-file inventory row (MAPPING, its two exclusion carriers, the two dogfood arms) records that the resolver, the four finding classes and the warn-to-gate table are consumed mechanisms named by no design row's Module or CodeSymbol, so the parent's delivered half is traceable only through its test; the rationale calls recording that "no design row OWNS them" the load-bearing half -> the same inventory row records that those consumers are decomposed apart from it, LLR-276 owning the resolver, the classes and the table and LLR-275 the independent walk of the shipped tree, so the delivered half is traced through those two rows; the rationale now calls recording "which design rows OWN them" the load-bearing half and asks the next reviser to find "where its consumers are traced" rather than "which of its consumers is traceable at all" -> the obligation on the inventory itself is byte-identical (a builder of MAPPING and TC-199 act the same), but the row's recorded stopping boundary moved: which design rows own the mechanisms it names is the decomposition claim a reviewer reads SR-163's coverage from, and the old text's claim of an undischarged remainder is withdrawn. The brief says to fail toward meaning where the obligations differ at all, and a scope statement is one of its named kinds. Blessed: LLR-275 names `bootstrap.delivery_inventory` and LLR-276 names `gen_arch_map.mapping_purpose_findings`, `mapping_purpose_report`, `MAPPING_FINDING_POLICY` and `resolve_requirement_reference`, each of which exists as named; the "NOT DISCHARGED" clause about the unfilled reference cell stands unchanged and is still true (the warn class is `unmapped_file`); and the closing sentence is standing prose, not a receipt for the split.
- [MEANING] LLR-233 Detail -> an inputs entry is judged as a repository path, and one outside the repository (absolute, drive-qualified, or still climbing out with `..`) is a failure in the always-on integrity class -> an inputs entry is a repository path OR a registry row id (a tier prefix, a hyphen and digits, as SR-184), the id standing for the row's cells as the observation writer's digest reads them, inside the repository by construction and never judged as an escaping path; the failure set is otherwise unchanged -> a new legal input class with a stated digest semantic: a checker correct under the old text had no rule for an id, and a writer correct under it could have digested nothing for one. Blessed: `assumption_rules.input_escape` returns None for an id (no leading slash, no drive letter, no climb), `rejudge._support_paths` resolves `_ROW_ID` to the registry directories rather than to a file named after the id, and TC-276's `test_a_registry_row_id_is_a_legal_declared_input` plus `tests/test_registry_id_inputs.py` drive exactly the declaration, the support paths and the row-by-row digest (green, fast batch below). This closes WI-680's non-blocking finding 3, which said no cell of SR-198 or LLR-233 called an id a legal input.

## How the cells were read

- LLR-203's amendment is the coordinator's wave-5 ruling 11 grant made
  concrete; it is judged here on its text against the two rows it now names,
  which are themselves judged in WI-691. Whether they are approved does not
  change what LLR-203 claims: ownership is a fact about the registry, not
  about a Status cell.
- LLR-233's amendment is the WI-616 ruling-15 fix seen from the design tier;
  its test is TC-276, judged in WI-691.

Bar I produced (not claimed), on this tree with `python -m pytest -q -n 4 -p
no:cacheprovider`: the fast batch shared across batch C
(`tests/test_assumption_rules.py`, `tests/test_registry_id_inputs.py`,
`tests/test_mapping_purpose.py` among fourteen modules): **448 passed, 1
skipped in 16.80s** (the skip is `test_kitlib_secret_classes.py:214`, by
design); the slow batch (`tests/test_dogfood_sync.py`, `tests/test_snapshot_readers.py`,
`tests/test_intake.py` among eight modules): **372 passed, 1 skipped in
195.57s** (the skip is `test_dogfood_sync.py:189`, an empty parameter set,
unrelated to these rows). No failures, no errors.

## Dispositions

None owed: both rows are blessed and join the act's `--reattests`.

VERDICT: MEANING rows=2
