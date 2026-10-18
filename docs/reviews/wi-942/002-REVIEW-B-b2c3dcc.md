Reviewed: b2c3dcccf971f5f81cd4af5bdb35a192f9c0ee1f

## REVIEW-B (Claude Opus, high) — WI-942 full lane, c58293d54...b2c3dccc

**Verified.** Failure classes hunted first, in this order: (1) fail-open, where a copy the floor used to refuse is now authorized when it should not be; (2) silent wrong content in the acted set that the scope, backing or held checks read; (3) a crash where the old code failed closed. On (1): the only newly authorized input is a ledger-named id (re-attested, or a ledger-only approval) that the head no longer holds. `_tier_of` maps it by prefix over `AMENDMENT_CSVS` (= `APPROVAL_ACT_CSVS`) to that tier's canonical path. `_registry_identity` folds every carrier back to the same path, so a CSV or markdown carrier keeps working. An id of an uncovered tier (STK, IF, lowercase or misspelt prefix) still maps to `None`, which `_copy_lines` drops, so its copy stays WIDENED (closed). The writer refuses an id that names neither a live row nor a recorded one, and it refuses a first approval of a row absent at HEAD. So the new authorization is reachable only for a genuine retirement. The scope, backing and held-rung checks still judge that retirement, and they read only the ids, which did not change. A ledger-only approval of an absent row now owes WITHOUT ITS ANCHOR where it owed nothing before: tighter, not looser. On (2): live flips keep the two-tree walk's registry, and every consumer of `acted[...]` (`_copy_lines`, `adjudication_approval_refusal`, `reattest_scope_refusal`, `backed_act_refusal` at acceptance_record.py:998) reads either the ids or the non-None registries. On (3): `reattested_between` and the ledger set both `str()` every id before `_tier_of` sees it, so `rid.startswith` cannot raise.

I drove the real path. The new tests run the real snapshot writer (`SNAP.copy_live(..., reattests=...)`) and the real `merge_approval_refusal`/`lane_acted_set` on scaffold git repos. To check red-before, I exported the reviewed tree to scratch and restored only the base `acceptance_record.py`. There, `test_a_retirement_alone_in_its_registry_merges` fails with "snapshot WIDENED to docs/requirements/system-requirements.toml without an approved row", and `test_the_acted_set_names_a_retired_rows_registry` fails with `{'reattest': {'SR-002': None}}`. The three new pins and `test_a_combined_act_copying_a_registry_neither_section_moved_is_widened` pass on the pre-fix code, as the spec requires.

**Done-when map.**
- Lone retirement merges, on a scoped lane and on an unscoped one: test_a_retirement_alone_in_its_registry_merges, red before.
- Acted set names the retired row's registry: test_the_acted_set_names_a_retired_rows_registry, red before.
- Pins, all passing before and after:
  - held rung, refused by row: test_a_lone_retirement_on_a_held_rung_is_refused_by_row;
  - outside the amendment scope, refused OUTSIDE: test_a_retirement_outside_the_amendment_scope_is_refused;
  - no accepted verdict rules it: test_a_retirement_no_accepted_verdict_rules_is_refused;
  - the WIDENED pin is unchanged.
- `_registries_holding` is gone. `git grep` at the reviewed commit finds it only in `docs/archive/last_approved/` (LLR-278's recorded copy, which the checkpoint act re-anchors) and in records.
- The recipes sentence is gone, and the three skill copies are byte-identical (`cmp`).
- Spine: LLR-278 and TC-278 carry the spec's text verbatim. The changed cells are LLR-278's detail and code_symbol, and TC-278's method, expected and evidence. No other cell moved and no Status flipped.
- RESYNC_PACK.md carries the entry.
- Landing-tip bar: check_trajectory --strict is clean on this commit. The smoke tier was not run (round facts), so the bar stays the landing's to show.

**Rubric.**
- K1: the LLR-278 insertion states what the code at acceptance_record.py:853-857 does.
- K2: no SN or SR row is touched.
- K3: `lane_acted_set`'s `Implements: SR-178, LLR-278` matches LLR-278's module and code_symbol, and the deleted symbol left code_symbol.
- K4: the entry is anchored `[since 396ff9f44]`, a trunk commit. It is not yet the landing's parent (c58293d54 is now trunk's tip). D-002 and the recipes' landing step ("RESYNC: anchor the entry at the landing's parent") own that re-anchor. It is noted here for the landing, not as a finding.
- `scripts/acceptance_record.py` is the only shipped file. coordinator-cycle is `scope: this-repo`, so it is rightly absent from the entry.

**Requirement/counterpart decisions.**
- LLR-278 changed (child). Its parents SR-178 (drift reported against the recorded copy) and SR-228 (on a held rung, re-attest only with CLARITY) are retained, because their text is neutral on how the floor resolves a registry. The held arm is unchanged and pinned.
- TC-278 carries the corresponding change.
- SR-207 and LLR-245 (the writer half) are retained. LLR-245 already counts a retired row as drift that `--reattests` clears, and the floor now agrees with it.
- IF-091 (the integrate-to-floor seam) is retained: no signature changed.
- No decomposition. The sweep of the amended rows against existing rows found no contradiction: no other row says the floor reads "the registry that holds it".

**Commands**
- `git rev-parse HEAD` -> b2c3dcccf971f5f81cd4af5bdb35a192f9c0ee1f
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../wi942-r1-opus/wi-942 tests/test_snapshot_readers.py tests/test_integrate_admission.py tests/test_acceptance_record.py` -> `135 passed in 532.57s (0:08:52)`
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (941 work item(s), 822 done (87%), 30 cancelled, graph acyclic).` (exit 0; WARN lines are pre-existing open-row overlaps, incl. the expected WI-942/WI-943 pair)
- `python project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=131 LLR=304 TC=318 orphans=0 integrity=0 ...` (lane worktree left clean)
- Red-before, in a scratch export with the base acceptance_record.py: `pytest tests/test_snapshot_readers.py -k "retirement or retired_rows_registry or widened"` -> `2 failed, 5 passed` (the two new behaviour tests fail with WIDENED / `None`; the pins pass)

**Findings**
- [MINOR] docs/test/test-cases.toml:2832 -> TC-278's added Expected clause says a retired row's re-attestation authorizes its registry's copy "whether or not another act moved that registry", but no test in its evidence drives a retirement beside another act in the same registry at the merge floor. The five new tests cover only the lone case, so the "another act moved" arm has no evidence (rubric K1: a TC cell should claim only what its evidence shows) -> add one floor test (a retirement plus a re-attestation or first approval of another row in the same registry, merging), or narrow the clause to the lone case -> @owner

VERDICT: APPROVE findings=1
