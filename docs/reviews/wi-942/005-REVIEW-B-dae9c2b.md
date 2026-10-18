Reviewed: dae9c2bda1fcc3cea2bfa55bfef24521d246bd37

Verified. I ran this in the convergence stance over the full-lane range 2268a9a8c..dae9c2bda, read from the reviewed checkout. `git rev-parse HEAD` printed the reviewed sha, and `git status` stayed clean throughout. I hunted three failure classes, worst first: (1) fail-open, where a copy is now authorized that should stay WIDENED; (2) a lost refusal for a held-rung, out-of-scope or unbacked retirement; (3) WITHOUT ITS ANCHOR drifting for ledger-only approvals.

The code change is at project-trajectory/scripts/acceptance_record.py:827-857. `lane_acted_set` now places ledger-approved and re-attested ids by `_tier_of(rid)[0]`, using the same prefix reader over `AMENDMENT_CSVS` (which is `APPROVAL_ACT_CSVS`) that `held_reattest_refusal` already uses. Live flips keep the walk's registry because of `- set(approve)`, and `_registries_holding` is deleted. Every id that reaches `_tier_of` has been through `str()`, both in `reattested_between` and in the ledger set, so no non-string id crashes it. A prefix outside the walk (STK, IF, CMP, misspelt) still yields None, which `_copy_lines` drops, so that copy stays WIDENED. The prefixes SR-/LLR-/TC-/SN-/DA-/SUR- are not ambiguous under `startswith`. Every carrier path resolves through `_registry_identity` to the same canonical rel the old search returned, so a row present at the head maps to the same registry as before. The one behavior change is for ids absent at the head. Its tighter side, where a ledger-only approval of an absent row now owes its anchor, is not reachable through the writer.

Pre-fix red check. I extracted the reviewed tree into my scratch directory (`git archive`), put back acceptance_record.py from 2268a9a8c, and ran the seven retirement tests plus the WIDENED pin. Result: 3 failed, 4 passed.
- test_a_retirement_alone_in_its_registry_merges failed pre-fix with "snapshot WIDENED to docs/requirements/system-requirements.toml without an approved row".
- test_the_acted_set_names_a_retired_rows_registry failed pre-fix with `{'SR-002': None}`.
- test_a_retirement_beside_another_act_in_its_registry_merges failed pre-fix on its acted-set assertion. Its merge half passes before and after, as "whether or not" implies.
- The three pins (held rung by row, OUTSIDE, no ACCEPTED verdict) and test_a_combined_act_copying_a_registry_neither_section_moved_is_widened, which the diff does not edit, all passed pre-fix and pass post-fix.

Reviewer probes, scratch only, run on the reviewed code:
- A stray hand-made copy of the LLR registry's record beside a lone SR retirement is still refused, on a scoped lane and on an unscoped one. No fail-open.
- A lone SN (needs) retirement is admitted, and its acted set reads `{'SN-002': 'docs/requirements/stakeholder-needs.toml'}`.

Done-when map:
- Lone retirement merges: test_a_retirement_alone_in_its_registry_merges (red before).
- Acted set names the registry: test_the_acted_set_names_a_retired_rows_registry (red before).
- Pins: test_a_lone_retirement_on_a_held_rung_is_refused_by_row, test_a_retirement_outside_the_amendment_scope_is_refused, test_a_retirement_no_accepted_verdict_rules_is_refused, and the WIDENED pin unchanged. All green before and after.
- `_registries_holding` gone: `git grep` finds it only in the recorded copy under docs/archive/last_approved and in records.
- Recipes sentence gone, copies byte-identical: md5 c04d88cd... for all three copies.
- Spine: LLR-278 detail and code_symbol, and TC-278 method/expected/evidence, carry the spec's text verbatim, and the evidence names all six new tests. That a sitting judged them is out of my reading scope. See the finding below for the act.
- RESYNC_PACK: the entry is present at project-trajectory/RESYNC_PACK.md:8682, anchored [since 2268a9a8c], which is the trunk base. It names scripts/acceptance_record.py. coordinator-cycle is `scope: this-repo`, so it is rightly absent from the entry.
- Landing-tip commit bar: not run here, by the round's instruction.

Requirement/interface counterparts:
- Changed side: LLR-278.
- Parents SR-178 and SR-228 are retained. SR-178 is the drift report; SR-228 is the held CLARITY rule, and its held refusal-by-row is pinned unchanged. The amended clause refines copy authorization under them without moving either one's normative text. SR-207's acceptance ("adding that row to the act ... as a re-attestation, clears the refusal") now holds on the floor side too, so no counterpart change is owed.
- TC-278 is the verifying counterpart, and it carries the corresponding change.
- IF-091's data contract (the `merge_approval_refusal` signature) is unchanged, so it is retained.

Rubric:
- K1: the new LLR and TC text matches the code.
- K2: the added cells name no implementation carrier. The detail's pre-existing function names are approved text, out of this diff.
- K3: `lane_acted_set` and `_tier_of` carry `Implements: SR-178, LLR-278` and both appear in LLR-278's code_symbol. No Status flips.

Disclosure: one of my `git grep` calls surfaced two lines from earlier round records under docs/reviews/wi-942. I did not open those files, and nothing in this verdict relies on them.

Commands:
- `git rev-parse HEAD` -> dae9c2bda1fcc3cea2bfa55bfef24521d246bd37
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/2026-10-18c/wi942-gate-opus/wi-942 tests/test_snapshot_readers.py tests/test_integrate_admission.py tests/test_acceptance_record.py` -> 136 passed in 499.83s (0:08:19). 0 gated skips; the posix-shell gate is unsatisfied but skipped nothing.
- `python project-trajectory/scripts/check_trajectory.py --strict` -> check_trajectory: clean (941 work item(s), 823 done (87%), 30 cancelled, graph acyclic). WARNs are advisory, and none comes from this diff's code.
- `python project-trajectory/scripts/trace.py --strict-integrity` -> Traceability: SN=31 SR=131 LLR=304 TC=318 orphans=0 integrity=0 ... interface-findings=0 (exit 0)
- Pre-fix run (scratch archive with acceptance_record.py from 2268a9a8c): `pytest tests/test_snapshot_readers.py -k "retirement or retired_rows or combined_act_copying_a_registry_neither"` -> 3 failed, 4 passed
- Probe (scratch archive, reviewed code): `pytest tests/test_zz_reviewer_probe.py` -> 2 passed (stray LLR copy refused; lone SN retirement admitted)
- `diff docs/archive/last_approved/<registry> <registry>` for the LLR and TC registries -> the only differences are LLR-278's code_symbol/detail and TC-278's method/expected/evidence

- [MINOR] docs/requirements/low-level-requirements.toml:2868 -> anchor K3. The lane amends approved cells: LLR-278 detail, and TC-278 method/expected at docs/test/test-cases.toml:2827. Yet the range carries no amendment act. docs/archive/last_approved still records the pre-amendment text, and LLR-278's recorded code_symbol still names `_registries_holding`. A sitting record exists in the lane (003-ADJUDICATE), but no `--reattests` act anchors its ruling. As landed, both rows read as SR-178 drift and would be routed to a fresh amendment adjudication on trunk. This fails closed, not open. -> Before landing, take the checkpoint's act turn in the lane (`intake.py snapshot --reattests LLR-278,TC-278` naming the accepted verdict, per the coordinator-cycle act turn). If the sitting's outcome owes no act, record why in the lane's decisions. -> @coordinator

VERDICT: APPROVE findings=1
